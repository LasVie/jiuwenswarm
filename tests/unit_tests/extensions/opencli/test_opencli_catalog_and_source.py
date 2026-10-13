# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""Catalog validation and the OpenCLI source's argv, env and process handling."""

from __future__ import annotations

import asyncio
import json
import sys
import textwrap
from pathlib import Path

import pytest

from jiuwenswarm.extensions.opencli import catalog as catalog_module
from jiuwenswarm.extensions.opencli.catalog import ArgSpec, ArgumentValidationError, Catalog, CommandCancelled
from jiuwenswarm.extensions.opencli.sources import opencli as source_module
from jiuwenswarm.extensions.opencli.sources.opencli import (
    OpenCLIRuntime,
    OpenCLISource,
    build_argv,
    build_env,
    classify_exit,
    parse_error_envelope,
)

CATALOG = {
    "version": "1.8.8",
    "commands": [
        {
            "site": "demo", "command": "search", "description": "Search", "access": "read",
            "needs_browser": True, "columns": ["title", "url"],
            "args": [
                {"name": "query", "type": "str", "required": True, "positional": True},
                {"name": "limit", "type": "int", "default": 20},
                {"name": "sort", "type": "str", "choices": ["new", "top"]},
                {"name": "all", "type": "boolean"},
            ],
        },
        {"site": "demo", "command": "follow", "access": "write", "needs_browser": True,
         "args": [{"name": "uid", "type": "str", "required": True}]},
        {"site": "free", "command": "top", "access": "read", "needs_browser": False,
         "args": [{"name": "limit", "type": "int"}]},
    ],
}


@pytest.fixture
def catalog() -> Catalog:
    return Catalog.from_payload(CATALOG, source="opencli")


def test_arguments_are_validated_like_upstream(catalog: Catalog) -> None:
    spec = catalog.get("demo", "search")
    values = spec.normalize_args({"query": "gpu", "limit": 5, "sort": "top", "all": True})
    assert [(arg.name, text) for arg, text in values] == [
        ("query", "gpu"), ("limit", "5"), ("sort", "top"), ("all", "true")
    ]
    assert [text for _, text in spec.normalize_args({"query": "x", "all": "0"})] == ["x", "false"]
    for bad in ({"limit": 1}, {"query": "x", "limit": "3.5"}, {"query": "x", "limit": True},
                {"query": "x", "sort": "old"}, {"query": "x", "all": "maybe"}, {"query": "x", "window": "x"}):
        with pytest.raises(ArgumentValidationError):
            spec.normalize_args(bad)


def test_runtime_flags_cannot_be_injected(catalog: Catalog) -> None:
    spec = catalog.get("demo", "search")
    with pytest.raises(ArgumentValidationError, match="unknown argument"):
        spec.normalize_args({"query": "x", "site-session": "persistent"})


def test_catalog_filter_and_merge_priority(catalog: Catalog) -> None:
    assert catalog.sites() == ["demo", "free"]
    assert catalog.filter_sites(["free"]).sites() == ["free"]
    assert catalog.filter_sites(None) is catalog
    own = Catalog.from_payload(
        {"commands": [{"site": "demo", "command": "search", "description": "own", "needs_browser": False}]},
        source="own",
    )
    merged = Catalog.merge(own, catalog)
    assert merged.get("demo", "search").source == "own"
    assert merged.get("demo", "follow").source == "opencli"


def _runtime(tmp_path: Path, catalog: Catalog, cli: Path) -> OpenCLIRuntime:
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    return OpenCLIRuntime(
        cli_path=cli, node_command=sys.executable, node_version="24.0.0", version="1.8.8",
        catalog=catalog, home_dir=home, cache_dir=tmp_path / "cache",
    )


def test_skipping_an_earlier_optional_positional_is_rejected() -> None:
    spec = Catalog.from_payload(
        {"commands": [{"site": "chat", "command": "messages", "args": [
            {"name": "item_id", "positional": True}, {"name": "user_id", "positional": True}]}]},
        source="opencli",
    ).get("chat", "messages")
    assert [text for _, text in spec.normalize_args({"item_id": "i"})] == ["i"]
    with pytest.raises(ArgumentValidationError, match='"item_id" must also be given'):
        spec.normalize_args({"user_id": "u"})


def test_argv_uses_equals_options_and_positionals_after_separator(tmp_path: Path, catalog: Catalog) -> None:
    runtime = _runtime(tmp_path, catalog, tmp_path / "entry.mjs")
    spec = catalog.get("demo", "search")
    argv = build_argv(runtime, spec, spec.normalize_args({"limit": 3, "query": "-q", "sort": "top"}))
    assert argv[2:] == ["demo", "search", "--limit=3", "--sort=top", "-f", "json", "--trace", "off",
                        "--site-session", "ephemeral", "--", "-q"]
    free = catalog.get("free", "top")
    free_argv = build_argv(runtime, free, free.normalize_args({"limit": 1}))
    assert "--site-session" not in free_argv and "--" not in free_argv


def test_env_is_isolated_and_uses_electron_node(tmp_path: Path, catalog: Catalog, monkeypatch) -> None:
    monkeypatch.setenv("OPENCLI_PROFILE", "user-profile")
    monkeypatch.setenv("SECRET_TOKEN", "x")
    runtime = _runtime(tmp_path, catalog, tmp_path / "main.js")
    env = build_env(runtime, "ws://127.0.0.1:1/devtools/page/T")
    assert env["ELECTRON_RUN_AS_NODE"] == "1"
    assert env["HOME"] == env["USERPROFILE"] == str(runtime.home_dir)
    assert env["OPENCLI_SITE_SESSION"] == "ephemeral"
    assert env["OPENCLI_CDP_ENDPOINT"].startswith("ws://")
    assert "OPENCLI_PROFILE" not in env and "SECRET_TOKEN" not in env
    assert "OPENCLI_CDP_ENDPOINT" not in build_env(runtime, None)


def test_exit_codes_and_error_envelope() -> None:
    assert [classify_exit(code) for code in (0, 66, 2, 77, 69, 78, 75, 1, None)] == [
        "ok", "empty", "invalid_args", "needs_user", "env_unavailable", "env_unavailable",
        "timeout", "error", "error",
    ]
    stderr = "ok: false\nerror:\n  code: AUTH_REQUIRED\n  message: login first\n  help: sign in\n  exitCode: 77\n"
    assert parse_error_envelope(stderr) == ("AUTH_REQUIRED", "login first", "sign in")
    assert parse_error_envelope("plain failure") == ("", "plain failure", "")


FAKE_CLI = textwrap.dedent(
    """
    import json, os, sys, time
    site, command = sys.argv[1], sys.argv[2]
    if command == "ok":
        print(json.dumps([{"title": "a", "url": "u"}, {"title": "b", "url": "v"}]))
    elif command == "env":
        print(json.dumps({"cdp": os.environ.get("OPENCLI_CDP_ENDPOINT", ""),
                          "electron": os.environ.get("ELECTRON_RUN_AS_NODE", "")}))
    elif command == "empty":
        sys.stderr.write("ok: false\\nerror:\\n  code: EMPTY_RESULT\\n  message: nothing\\n")
        sys.exit(66)
    elif command == "auth":
        sys.stderr.write("ok: false\\nerror:\\n  code: AUTH_REQUIRED\\n  message: captcha needed\\n")
        sys.exit(77)
    elif command == "slow":
        time.sleep(60)
    elif command == "big":
        sys.stdout.write("x" * 5000)
        sys.stdout.flush()
        time.sleep(60)
    """
)


@pytest.fixture
def fake_source(tmp_path: Path) -> OpenCLISource:
    cli = tmp_path / "fake_cli.py"
    cli.write_text(FAKE_CLI, encoding="utf-8")
    commands = [
        {"site": "fake", "command": name, "access": "read", "needs_browser": False, "args": []}
        for name in ("ok", "env", "empty", "auth", "slow", "big")
    ]
    catalog = Catalog.from_payload({"commands": commands}, source="opencli")
    return OpenCLISource(_runtime(tmp_path, catalog, cli))


async def _run(source: OpenCLISource, command: str, *, timeout_s: float = 20, endpoint: str | None = None):
    spec = source.catalog().get("fake", command)
    return await source.run(spec, [], page_endpoint=endpoint, timeout_s=timeout_s, cwd=source.runtime.home_dir)


async def test_run_parses_rows_empty_and_user_action(fake_source: OpenCLISource) -> None:
    ok = await _run(fake_source, "ok")
    assert (ok.category, ok.exit_code, ok.started) == ("ok", 0, True)
    assert ok.rows[0]["title"] == "a"
    env = await _run(fake_source, "env", endpoint="ws://127.0.0.1:1/devtools/page/T")
    assert env.rows == {"cdp": "ws://127.0.0.1:1/devtools/page/T", "electron": "1"}
    empty = await _run(fake_source, "empty")
    assert (empty.category, empty.rows, empty.error_code) == ("empty", [], "EMPTY_RESULT")
    auth = await _run(fake_source, "auth")
    assert (auth.category, auth.error_code, auth.error_message) == ("needs_user", "AUTH_REQUIRED", "captcha needed")


async def test_browser_command_never_runs_without_a_page_endpoint(tmp_path: Path, catalog: Catalog) -> None:
    source = OpenCLISource(_runtime(tmp_path, catalog, tmp_path / "missing_cli.py"))
    spec = catalog.get("demo", "search")
    outcome = await source.run(spec, spec.normalize_args({"query": "q"}), page_endpoint=None,
                               timeout_s=5, cwd=tmp_path)
    assert (outcome.started, outcome.category) == (False, "env_unavailable")


async def test_timeout_kills_the_process_tree(fake_source: OpenCLISource) -> None:
    outcome = await _run(fake_source, "slow", timeout_s=1)
    assert (outcome.category, outcome.killed, outcome.started) == ("timeout", True, True)


async def test_cancellation_stops_the_real_process_before_reporting_execution_facts(fake_source, monkeypatch) -> None:
    spawned = asyncio.Event()
    original_spawn = asyncio.create_subprocess_exec
    processes = []

    async def spawn(*args, **kwargs):
        process = await original_spawn(*args, **kwargs)
        processes.append(process)
        spawned.set()
        return process

    monkeypatch.setattr(source_module.asyncio, "create_subprocess_exec", spawn)
    task = asyncio.create_task(_run(fake_source, "slow"))
    await asyncio.wait_for(spawned.wait(), timeout=5)
    task.cancel()
    with pytest.raises(CommandCancelled) as caught:
        await task
    assert caught.value.outcome.started and caught.value.outcome.killed
    assert processes[0].returncode is not None


async def test_cancel_during_spawn_still_owns_and_stops_the_child(fake_source, monkeypatch) -> None:
    spawned = asyncio.Event()
    return_process = asyncio.Event()
    original_spawn = asyncio.create_subprocess_exec
    processes = []

    async def delayed_spawn(*args, **kwargs):
        process = await original_spawn(*args, **kwargs)
        if args[0] != "taskkill":
            processes.append(process)
            spawned.set()
            await return_process.wait()
        return process

    monkeypatch.setattr(source_module.asyncio, "create_subprocess_exec", delayed_spawn)
    task = asyncio.create_task(_run(fake_source, "slow"))
    await asyncio.wait_for(spawned.wait(), timeout=5)
    task.cancel()
    await asyncio.sleep(0)
    return_process.set()
    with pytest.raises(CommandCancelled) as caught:
        await task
    assert caught.value.outcome.started and caught.value.outcome.killed
    assert processes[0].returncode is not None


async def test_oversized_output_is_stopped(fake_source: OpenCLISource, monkeypatch) -> None:
    monkeypatch.setattr(source_module, "STDOUT_LIMIT_BYTES", 1024)
    outcome = await _run(fake_source, "big", timeout_s=20)
    assert outcome.output_too_large and outcome.killed
    assert outcome.category == "error"


def test_update_script_builds_website_only_catalog() -> None:
    from scripts import update_opencli_runtime as update

    manifest = [
        {"site": "web", "name": "read", "access": "read", "browser": True, "strategy": "cookie",
         "args": [{"name": "q", "type": "str", "required": True, "positional": True, "help": "query"}],
         "columns": ["title"], "domain": "web.example"},
        {"site": "web", "name": "local", "strategy": "local", "browser": False},
        {"site": "desktop-app", "name": "ask", "strategy": "ui", "browser": True},
        {"site": "api", "name": "post", "access": "write", "browser": False, "strategy": "public"},
    ]
    built = update.build_catalog(manifest, ["desktop-app"])
    assert [(c["site"], c["command"]) for c in built["commands"]] == [("api", "post"), ("web", "read")]
    assert built["excluded"] == {"electron_app_sites": ["desktop-app"], "local_strategy_commands": 1}
    read = next(c for c in built["commands"] if c["command"] == "read")
    assert read["needs_browser"] is True and read["args"][0]["positional"] is True
    loaded = Catalog.from_payload(built, source="opencli")
    assert loaded.get("api", "post").access == "write"


def test_bundled_catalog_matches_manifest() -> None:
    resources = Path(source_module.__file__).resolve().parents[3] / "resources" / "runtime" / "opencli"
    manifest = json.loads((resources / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["version"] == source_module.OPENCLI_VERSION
    bundled = Catalog.load(resources / manifest["catalog"], source="opencli")
    assert len(bundled) > 1000
    assert not ({"chatgpt-app", "discord-app", "doubao-app"} & set(bundled.sites()))
    assert isinstance(catalog_module.Catalog, type)
