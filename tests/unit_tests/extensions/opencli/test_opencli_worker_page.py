# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""Worker page client: host protocol, hold enforcement, reset and serialisation."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace

import httpx
import pytest

from jiuwenswarm.extensions.opencli.worker_page import (
    AwaitingUser,
    HostBinding,
    HostClient,
    HostError,
    PageSlot,
)

BINDING = HostBinding(resolver="http://127.0.0.1:9999", token="tk", session_id="s/1", member_id="m")


def _action(request: httpx.Request) -> str:
    # raw_path keeps the percent-encoded session id in one segment.
    parts = request.url.raw_path.split(b"?")[0].decode().split("/")
    return parts[2] if len(parts) > 2 else ""


class FakeHost:
    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []
        self.awaiting = False
        self.fail_reset = False
        self.active = 0
        self.max_active = 0

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        assert request.headers["authorization"] == "Bearer tk"
        assert request.url.params["role"] == "opencli"
        action = _action(request)
        if action == "hold":
            return httpx.Response(200, json={"held": True})
        if action == "reset":
            return httpx.Response(500, json={"error": "boom"}) if self.fail_reset else httpx.Response(200, json={})
        if action == "confirm":
            body = json.loads(request.content)
            return httpx.Response(200, json={"decision": "approve" if body["command"] == "ok" else "reject"})
        if request.method == "POST":
            if self.awaiting:
                return httpx.Response(409, json={"error": "awaiting_user", "reason": "captcha", "instructions": "do it"})
            return httpx.Response(200, json={"webSocketDebuggerUrl": "ws://127.0.0.1:1/devtools/page/T"})
        return httpx.Response(200, json={"released": True})

    def actions(self) -> list[str]:
        return [_action(request) or request.method for request in self.requests]


@pytest.fixture
def host() -> FakeHost:
    return FakeHost()


def _slot(host: FakeHost) -> PageSlot:
    return PageSlot(HostClient(BINDING, transport=httpx.MockTransport(host.handler)))


async def test_acquire_release_and_request_shape(host: FakeHost) -> None:
    slot = _slot(host)
    async with slot.use() as endpoint:
        assert endpoint == "ws://127.0.0.1:1/devtools/page/T"
    acquire, release = host.requests
    assert acquire.url.raw_path.split(b"?")[0] == b"/s%2F1"
    assert acquire.url.params["member"] == "m"
    assert acquire.url.params["label"] == "OpenCLI · m"
    assert acquire.url.params["visibility"] == "sidebar"
    assert release.method == "DELETE" and release.url.params["lease"] == acquire.url.params["lease"]


async def test_awaiting_user_is_enforced_by_the_host(host: FakeHost) -> None:
    host.awaiting = True
    with pytest.raises(AwaitingUser) as raised:
        async with _slot(host).use():
            pytest.fail("the page must not be handed out while the user has not decided")
    assert (raised.value.reason, raised.value.instructions) == ("captcha", "do it")


@pytest.mark.parametrize("visibility", ["sidebar", "hidden"])
async def test_killed_command_resets_the_page_and_retries_a_failed_reset(host: FakeHost, visibility: str) -> None:
    binding = replace(BINDING, visibility=visibility)
    slot = PageSlot(HostClient(binding, transport=httpx.MockTransport(host.handler)))
    host.fail_reset = True
    async with slot.use():
        slot.mark_killed()
    assert host.actions() == ["POST", "DELETE", "reset"]
    for request in host.requests:
        assert request.url.params["label"] == "OpenCLI · m"
        assert request.url.params["visibility"] == visibility
    host.fail_reset = False
    host.requests.clear()
    async with slot.use():
        pass
    assert host.actions() == ["reset", "POST", "DELETE"], "a failed reset is retried before the next use"
    for request in host.requests:
        assert request.url.params["label"] == "OpenCLI · m"
        assert request.url.params["visibility"] == visibility


async def test_a_second_cancel_does_not_interrupt_page_cleanup(host: FakeHost, monkeypatch) -> None:
    slot = _slot(host)
    resetting = asyncio.Event()
    allow_reset = asyncio.Event()
    reset = slot.client.reset

    async def slow_reset():
        resetting.set()
        await allow_reset.wait()
        await reset()

    monkeypatch.setattr(slot.client, "reset", slow_reset)

    async def use():
        async with slot.use():
            slot.mark_killed()
            raise asyncio.CancelledError

    task = asyncio.create_task(use())
    await asyncio.wait_for(resetting.wait(), timeout=1)
    task.cancel()
    allow_reset.set()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert host.actions() == ["POST", "DELETE", "reset"]


async def test_cancel_during_acquisition_releases_the_late_host_lease(host: FakeHost, monkeypatch) -> None:
    slot = _slot(host)
    assigned = asyncio.Event()
    return_endpoint = asyncio.Event()
    acquire = slot.client.acquire

    async def delayed_acquire(lease_id):
        endpoint = await acquire(lease_id)
        assigned.set()
        await return_endpoint.wait()
        return endpoint

    monkeypatch.setattr(slot.client, "acquire", delayed_acquire)

    async def use():
        async with slot.use():
            pytest.fail("a cancelled acquisition must never yield its page")

    task = asyncio.create_task(use())
    await asyncio.wait_for(assigned.wait(), timeout=1)
    task.cancel()
    await asyncio.sleep(0)
    return_endpoint.set()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert host.actions() == ["POST", "DELETE"]
    assert host.requests[0].url.params["lease"] == host.requests[1].url.params["lease"]


async def test_hold_and_confirm(host: FakeHost) -> None:
    slot = _slot(host)
    block_id = await slot.mark_awaiting_user(reason="captcha", instructions="do it")
    hold = json.loads(host.requests[-1].content)
    assert hold["block_id"] == block_id and hold["ttl_s"] == 30 * 60
    assert await slot.confirm(command="ok", args=[], warnings=[], timeout_s=5) == "approve"
    assert await slot.confirm(command="no", args=[], warnings=[], timeout_s=5) == "reject"


async def test_calls_on_one_page_are_serialised(host: FakeHost) -> None:
    slot = _slot(host)
    order: list[str] = []

    async def use(name: str) -> None:
        async with slot.use():
            order.append(f"{name}-start")
            await asyncio.sleep(0.05)
            order.append(f"{name}-end")

    await asyncio.gather(use("a"), use("b"))
    assert order in (["a-start", "a-end", "b-start", "b-end"], ["b-start", "b-end", "a-start", "a-end"])


async def test_unreachable_host_is_a_host_error() -> None:
    def fail(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused", request=request)

    slot = PageSlot(HostClient(BINDING, transport=httpx.MockTransport(fail)))
    with pytest.raises(HostError):
        async with slot.use():
            pass
