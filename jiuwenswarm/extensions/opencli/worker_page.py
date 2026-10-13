# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""Client for the OpenCLI worker page owned by the Electron host.

The worker page is a separate WebContents in the shared browser partition,
one per session/member. The Electron host is the source of truth for the
"awaiting user" hold: while the user has not clicked a decision button in the
sidebar, the host refuses to hand the page out (HTTP 409), so no automatic
task can navigate a captcha away. This client only serialises calls on one
page and resets the page after a cancelled command.
"""

from __future__ import annotations

import asyncio
import logging
import os
import threading
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Any, AsyncIterator
from urllib.parse import quote

import httpx

logger = logging.getLogger(__name__)

WORKER_ROLE = "opencli"
DEFAULT_HOLD_TTL_S = 30 * 60
_REQUEST_TIMEOUT_S = 20.0


class HostError(RuntimeError):
    """The Electron host could not provide or manage the worker page."""


class AwaitingUser(Exception):
    """The worker page still waits for the user's decision in the sidebar."""

    def __init__(self, reason: str, instructions: str) -> None:
        super().__init__(instructions or reason)
        self.reason = reason
        self.instructions = instructions


@dataclass(frozen=True)
class HostBinding:
    resolver: str
    token: str
    session_id: str
    member_id: str = ""
    visibility: str = "sidebar"

    @property
    def label(self) -> str:
        return f"OpenCLI · {self.member_id}" if self.member_id else "OpenCLI"

    @property
    def key(self) -> tuple[str, str, str]:
        return (self.resolver, self.session_id, self.member_id)


class HostClient:
    """Thin async client for the worker-page routes of the target resolver."""

    def __init__(self, binding: HostBinding, *, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._binding = binding
        self._transport = transport

    def _url(self, action: str = "") -> str:
        base = f"{self._binding.resolver.rstrip('/')}/{quote(self._binding.session_id, safe='')}"
        return f"{base}/{action}" if action else base

    def _params(self, **extra: str) -> dict[str, str]:
        params = {
            "member": self._binding.member_id,
            "role": WORKER_ROLE,
            "label": self._binding.label,
            "visibility": self._binding.visibility,
        }
        params.update({key: value for key, value in extra.items() if value is not None})
        return params

    async def _request(
        self,
        method: str,
        action: str = "",
        *,
        params: dict[str, str] | None = None,
        payload: dict[str, Any] | None = None,
        timeout_s: float = _REQUEST_TIMEOUT_S,
    ) -> dict[str, Any]:
        headers = {"Authorization": f"Bearer {self._binding.token}"}
        try:
            async with httpx.AsyncClient(transport=self._transport, timeout=timeout_s, trust_env=False) as client:
                response = await client.request(
                    method, self._url(action), params=params or self._params(), json=payload, headers=headers
                )
        except httpx.HTTPError as exc:
            raise HostError(f"browser host unreachable: {exc}") from exc
        try:
            body = response.json()
        except ValueError:
            body = {}
        if response.status_code == 409 and body.get("error") == "awaiting_user":
            raise AwaitingUser(str(body.get("reason") or ""), str(body.get("instructions") or ""))
        if response.status_code >= 400:
            raise HostError(f"browser host returned HTTP {response.status_code}: {body.get('error', '')}")
        return body if isinstance(body, dict) else {}

    async def acquire(self, lease_id: str) -> str:
        body = await self._request(
            "POST",
            params=self._params(
                lease=lease_id,
                pid=str(os.getpid()),
            ),
        )
        endpoint = str(body.get("webSocketDebuggerUrl") or "")
        if not endpoint.startswith("ws://"):
            raise HostError("browser host returned no page endpoint")
        return endpoint

    async def release(self, lease_id: str) -> None:
        await self._request("DELETE", params=self._params(lease=lease_id, pid=str(os.getpid())))

    async def hold(self, *, block_id: str, reason: str, instructions: str, ttl_s: int) -> None:
        await self._request(
            "POST",
            "hold",
            payload={"block_id": block_id, "reason": reason, "instructions": instructions, "ttl_s": ttl_s},
        )

    async def reset(self) -> None:
        await self._request("POST", "reset")

    async def confirm(self, *, command: str, args: list[str], warnings: list[str], timeout_s: float) -> str:
        body = await self._request(
            "POST",
            "confirm",
            payload={"command": command, "args": args, "warnings": warnings, "timeout_s": int(timeout_s)},
            timeout_s=timeout_s + 10.0,
        )
        decision = str(body.get("decision") or "timeout")
        return decision if decision in {"approve", "reject", "timeout"} else "timeout"


@dataclass
class _SlotState:
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    needs_reset: bool = False


class PageSlot:
    """Serialises OpenCLI calls on one worker page."""

    def __init__(
        self, client: HostClient, *, hold_ttl_s: int = DEFAULT_HOLD_TTL_S, state: _SlotState | None = None,
    ) -> None:
        self._client = client
        self._hold_ttl_s = hold_ttl_s
        self._state = state or _SlotState()
        self._killed = False

    @property
    def client(self) -> HostClient:
        return self._client

    @asynccontextmanager
    async def use(self) -> AsyncIterator[str]:
        """Yield the page WebSocket endpoint for one command."""
        async with self._state.lock:
            if self._state.needs_reset:
                await self._client.reset()
                self._state.needs_reset = False
            lease_id = uuid.uuid4().hex
            acquisition = asyncio.create_task(self._client.acquire(lease_id))
            cancelled = False
            try:
                endpoint = await asyncio.shield(acquisition)
            except asyncio.CancelledError:
                # The host may have assigned the lease before its HTTP reply.
                # Wait for that request so release cannot race ahead of it.
                cancelled = True
                while not acquisition.done():
                    try:
                        await asyncio.shield(acquisition)
                    except asyncio.CancelledError:
                        continue
                    except (HostError, AwaitingUser):
                        break
                if acquisition.exception() is not None:
                    raise asyncio.CancelledError from None
                endpoint = acquisition.result()
            self._killed = False
            try:
                if cancelled:
                    raise asyncio.CancelledError
                yield endpoint
            finally:
                cleanup = asyncio.create_task(self._release(lease_id))
                interrupted = False
                while not cleanup.done():
                    try:
                        await asyncio.shield(cleanup)
                    except asyncio.CancelledError:
                        interrupted = True
                cleanup.result()
                if interrupted:
                    raise asyncio.CancelledError

    async def _release(self, lease_id: str) -> None:
        try:
            await self._client.release(lease_id)
        except HostError:
            logger.warning("[opencli] failed to release worker page lease", exc_info=True)
        if self._killed:
            # Scripts or requests dispatched by the adapter outlive the CLI.
            try:
                await self._client.reset()
            except HostError:
                self._state.needs_reset = True

    def mark_killed(self) -> None:
        self._killed = True

    async def mark_awaiting_user(self, *, reason: str, instructions: str) -> str:
        block_id = uuid.uuid4().hex
        await self._client.hold(
            block_id=block_id, reason=reason, instructions=instructions, ttl_s=self._hold_ttl_s
        )
        return block_id

    async def confirm(self, *, command: str, args: list[str], warnings: list[str], timeout_s: float) -> str:
        return await self._client.confirm(command=command, args=args, warnings=warnings, timeout_s=timeout_s)


_SLOTS: dict[tuple[str, str, str], _SlotState] = {}
_SLOTS_LOCK = threading.Lock()


def get_slot(binding: HostBinding) -> PageSlot:
    """Snapshot the task's binding while sharing page locks and reset state."""
    with _SLOTS_LOCK:
        state = _SLOTS.setdefault(binding.key, _SlotState())
        return PageSlot(HostClient(binding), state=state)
