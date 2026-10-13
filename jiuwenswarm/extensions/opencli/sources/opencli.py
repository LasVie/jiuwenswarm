# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""OpenCLI command source: pinned runtime, catalog and process execution.

This is the only module that knows OpenCLI's flags, environment variables,
exit codes and error envelope. The runtime is run with Electron's own Node
mode (``ELECTRON_RUN_AS_NODE=1``), so no system Node installation is needed.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import re
import signal
import subprocess
import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NoReturn

import yaml

from jiuwenswarm.common.playwright_mcp_runtime import (
    PlaywrightMcpRuntimeError,
    materialize_bundled_runtime,
)
from jiuwenswarm.common.utils import get_user_workspace_dir
from jiuwenswarm.extensions.opencli.catalog import ArgSpec, Catalog, CommandCancelled, CommandSpec, RunOutcome

logger = logging.getLogger(__name__)

SOURCE_ID = "opencli"
OPENCLI_VERSION = "1.8.8"
MINIMUM_NODE_VERSION = (20, 18, 1)
RUNTIME_NAME = "opencli"
STDOUT_LIMIT_BYTES = 16 * 1024 * 1024
STDERR_LIMIT_BYTES = 1024 * 1024
KILL_WAIT_S = 5.0
_RESOURCE_DIR = Path(__file__).resolve().parents[3] / "resources" / "runtime" / "opencli"
# Environment inherited by the CLI child; everything else is dropped.
_ENV_ALLOWLIST = (
    "PATH", "SYSTEMROOT", "SystemRoot", "WINDIR", "COMSPEC", "PATHEXT", "TEMP", "TMP", "TMPDIR",
    "LANG", "LC_ALL", "LC_CTYPE", "TZ", "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY",
    "http_proxy", "https_proxy", "no_proxy",
)
_EXIT_CATEGORIES = {0: "ok", 66: "empty", 2: "invalid_args", 77: "needs_user", 69: "env_unavailable",
                    78: "env_unavailable", 75: "timeout"}


class OpenCLIUnavailable(RuntimeError):
    """The pinned OpenCLI runtime or Electron Node cannot be used."""

    def __init__(self, state: str, detail: str) -> None:
        super().__init__(detail)
        self.state = state
        self.detail = detail


@dataclass(frozen=True)
class OpenCLIRuntime:
    cli_path: Path
    node_command: str
    node_version: str
    version: str
    catalog: Catalog
    home_dir: Path
    cache_dir: Path


def _load_opencli_manifest(resource_dir: Path) -> dict[str, object]:
    manifest_path = resource_dir / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PlaywrightMcpRuntimeError(f"invalid OpenCLI runtime manifest: {manifest_path}") from exc
    if not isinstance(manifest, dict) or manifest.get("version") != OPENCLI_VERSION:
        raise PlaywrightMcpRuntimeError(f"OpenCLI runtime manifest must describe version {OPENCLI_VERSION}")
    for key in ("archive", "archive_sha256", "cli_relative_path", "catalog", "catalog_sha256"):
        if not isinstance(manifest.get(key), str) or not str(manifest[key]).strip():
            raise PlaywrightMcpRuntimeError(f"OpenCLI runtime manifest is missing {key}")
    for key in ("archive", "catalog"):
        if Path(str(manifest[key])).name != manifest[key]:
            raise PlaywrightMcpRuntimeError(f"OpenCLI runtime manifest {key} must be a filename")
    return manifest


def _version_tuple(text: str) -> tuple[int, ...]:
    match = re.match(r"v?(\d+)\.(\d+)\.(\d+)", text.strip())
    return tuple(int(part) for part in match.groups()) if match else ()


def _probe_node(node_command: str) -> str:
    env = {key: value for key, value in os.environ.items() if key in _ENV_ALLOWLIST}
    env["ELECTRON_RUN_AS_NODE"] = "1"
    try:
        result = subprocess.run(
            [node_command, "-p", "process.versions.node"],
            env=env,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise OpenCLIUnavailable("electron_node_unavailable", f"cannot run {node_command}: {exc}") from exc
    version = (result.stdout or "").strip()
    if result.returncode != 0 or not _version_tuple(version):
        raise OpenCLIUnavailable("electron_node_unavailable", f"cannot read Node version from {node_command}")
    if _version_tuple(version) < MINIMUM_NODE_VERSION:
        raise OpenCLIUnavailable(
            "electron_node_unavailable",
            f"Node {'.'.join(map(str, MINIMUM_NODE_VERSION))}+ is required; {node_command} provides {version}",
        )
    return version


_RUNTIME_CACHE: dict[tuple[str, str], OpenCLIRuntime] = {}
_RUNTIME_LOCK = threading.Lock()


def _load_catalog(resources: Path, manifest: dict[str, object]) -> Catalog:
    try:
        catalog_path = resources / str(manifest["catalog"])
        if hashlib.sha256(catalog_path.read_bytes()).hexdigest() != manifest["catalog_sha256"]:
            raise ValueError("catalog checksum mismatch")
        return Catalog.load(catalog_path, source=SOURCE_ID)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise OpenCLIUnavailable("runtime_missing", f"invalid OpenCLI catalog: {exc}") from exc


def inspect_runtime(
    node_command: str, *, node_version: str | None = None, resource_dir: Path | None = None,
) -> tuple[str, Catalog]:
    """Check files and host-reported Node version; never extract or start a process."""
    if not Path(node_command).is_file():
        raise OpenCLIUnavailable("electron_node_unavailable", "Electron executable is missing")
    if node_version and (_version_tuple(node_version) < MINIMUM_NODE_VERSION):
        raise OpenCLIUnavailable("electron_node_unavailable", "Electron's Node version is too old")
    resources = resource_dir or _RESOURCE_DIR
    try:
        manifest = _load_opencli_manifest(resources)
        archive = resources / str(manifest["archive"])
        if hashlib.sha256(archive.read_bytes()).hexdigest() != manifest["archive_sha256"]:
            raise PlaywrightMcpRuntimeError("OpenCLI archive checksum mismatch")
    except (PlaywrightMcpRuntimeError, OSError) as exc:
        raise OpenCLIUnavailable("runtime_missing", str(exc)) from exc
    return str(manifest["version"]), _load_catalog(resources, manifest)


def prepare_runtime(
    node_command: str,
    *,
    resource_dir: Path | None = None,
    user_workspace_dir: Path | None = None,
) -> OpenCLIRuntime:
    """Materialize the pinned runtime and verify Electron Node; cached per process."""
    resources = (resource_dir or _RESOURCE_DIR).resolve()
    key = (str(node_command), str(resources))
    with _RUNTIME_LOCK:
        cached = _RUNTIME_CACHE.get(key)
        if cached is not None:
            return cached
        workspace = (user_workspace_dir or get_user_workspace_dir()).expanduser()
        try:
            cli_path, manifest = materialize_bundled_runtime(
                resource_dir=resources,
                user_workspace_dir=workspace,
                runtime_name=RUNTIME_NAME,
                load_manifest=_load_opencli_manifest,
            )
        except (PlaywrightMcpRuntimeError, OSError) as exc:
            raise OpenCLIUnavailable("runtime_missing", str(exc)) from exc
        catalog = _load_catalog(resources, manifest)
        node_version = _probe_node(node_command)
        state_root = workspace / "runtime" / RUNTIME_NAME
        runtime = OpenCLIRuntime(
            cli_path=cli_path,
            node_command=str(node_command),
            node_version=node_version,
            version=str(manifest["version"]),
            catalog=catalog,
            home_dir=state_root / "home",
            cache_dir=state_root / "cache",
        )
        runtime.home_dir.mkdir(parents=True, exist_ok=True)
        runtime.cache_dir.mkdir(parents=True, exist_ok=True)
        _RUNTIME_CACHE[key] = runtime
        return runtime


def build_argv(runtime: OpenCLIRuntime, spec: CommandSpec, values: list[tuple[ArgSpec, str]]) -> list[str]:
    """``--name=value`` options, fixed flags, then ``--`` and positionals in declared order.

    The ``=`` form and the ``--`` separator keep values that start with ``-``
    (a query such as ``-foo``) from being parsed as options.
    """
    argv = [runtime.node_command, str(runtime.cli_path), spec.site, spec.command]
    argv.extend(f"--{arg.name}={text}" for arg, text in values if not arg.positional)
    argv.extend(["-f", "json", "--trace", "off"])
    # Upstream registers --site-session only for browser commands; passing it
    # to a browser-free command is an "unknown option" error.
    if spec.needs_browser:
        argv.extend(["--site-session", "ephemeral"])
    positionals = [text for arg, text in values if arg.positional]
    if positionals:
        argv.append("--")
        argv.extend(positionals)
    return argv


def build_env(runtime: OpenCLIRuntime, page_endpoint: str | None) -> dict[str, str]:
    env = {key: value for key, value in os.environ.items() if key in _ENV_ALLOWLIST}
    env.update(
        {
            "ELECTRON_RUN_AS_NODE": "1",
            "HOME": str(runtime.home_dir),
            "USERPROFILE": str(runtime.home_dir),
            "OPENCLI_CACHE_DIR": str(runtime.cache_dir),
            "OPENCLI_CONFIG_DIR": str(runtime.home_dir / ".opencli"),
            "OPENCLI_SITE_SESSION": "ephemeral",
            "NO_COLOR": "1",
        }
    )
    if page_endpoint:
        env["OPENCLI_CDP_ENDPOINT"] = page_endpoint
    return env


async def _read_capped(stream: asyncio.StreamReader, limit: int) -> tuple[bytes, bool]:
    chunks: list[bytes] = []
    size = 0
    while True:
        chunk = await stream.read(64 * 1024)
        if not chunk:
            return b"".join(chunks), False
        if size + len(chunk) > limit:
            chunks.append(chunk[: max(0, limit - size)])
            return b"".join(chunks), True
        chunks.append(chunk)
        size += len(chunk)


async def _kill_tree(process: asyncio.subprocess.Process) -> None:
    if process.returncode is not None:
        return
    try:
        if sys.platform == "win32":
            killer = await asyncio.create_subprocess_exec(
                "taskkill", "/T", "/F", "/PID", str(process.pid),
                stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL,
            )
            await killer.wait()
        else:
            os.killpg(process.pid, signal.SIGKILL)
    except (OSError, ProcessLookupError):
        pass
    try:
        await asyncio.wait_for(process.wait(), timeout=KILL_WAIT_S)
    except asyncio.TimeoutError:
        logger.warning("[opencli] process %s did not exit after kill", process.pid)


async def _cancel_command(process: asyncio.subprocess.Process | None) -> NoReturn:
    """Finish shutdown despite repeated cancellation, then report start facts."""
    if process is not None:
        cleanup = asyncio.create_task(_kill_tree(process))
        while not cleanup.done():
            try:
                await asyncio.shield(cleanup)
            except asyncio.CancelledError:
                continue
        cleanup.result()
    raise CommandCancelled(RunOutcome(
        started=process is not None, category="error", killed=process is not None,
        error_code="CANCELLED", error_message="command was cancelled",
    )) from None


def parse_error_envelope(stderr: str) -> tuple[str, str, str]:
    """Return (code, message, help) from upstream's YAML error envelope."""
    try:
        payload = yaml.safe_load(stderr)
    except yaml.YAMLError:
        payload = None
    if isinstance(payload, dict) and isinstance(payload.get("error"), dict):
        error = payload["error"]
        return (
            str(error.get("code") or ""),
            str(error.get("message") or "").strip(),
            str(error.get("help") or "").strip(),
        )
    return "", stderr.strip()[-2000:], ""


def classify_exit(exit_code: int | None) -> str:
    return _EXIT_CATEGORIES.get(exit_code if exit_code is not None else -1, "error")


class OpenCLISource:
    """Command source backed by the pinned OpenCLI runtime."""

    id = SOURCE_ID

    def __init__(self, runtime: OpenCLIRuntime) -> None:
        self._runtime = runtime

    @property
    def runtime(self) -> OpenCLIRuntime:
        return self._runtime

    def catalog(self) -> Catalog:
        return self._runtime.catalog

    async def run(
        self,
        spec: CommandSpec,
        values: list[tuple[ArgSpec, str]],
        *,
        page_endpoint: str | None,
        timeout_s: float,
        cwd: Path,
    ) -> RunOutcome:
        if spec.needs_browser and not page_endpoint:
            # Without a page endpoint upstream falls back to its daemon and
            # Chrome extension, i.e. the user's own browser. Never allow that.
            return RunOutcome(started=False, category="env_unavailable",
                              error_message="browser command requires a worker page endpoint")
        argv = build_argv(self._runtime, spec, values)
        kwargs: dict[str, Any] = {}
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | getattr(subprocess, "CREATE_NO_WINDOW", 0)
        else:
            kwargs["start_new_session"] = True
        spawn = asyncio.create_task(
            asyncio.create_subprocess_exec(
                *argv,
                cwd=str(cwd),
                env=build_env(self._runtime, page_endpoint),
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                **kwargs,
            )
        )
        try:
            # Keep ownership of a process created while a stop request arrives.
            process = await asyncio.shield(spawn)
        except asyncio.CancelledError:
            while not spawn.done():
                try:
                    await asyncio.shield(spawn)
                except asyncio.CancelledError:
                    continue
                except OSError:
                    break
            try:
                process = spawn.result()
            except OSError:
                process = None
            await _cancel_command(process)
        except OSError as exc:
            return RunOutcome(started=False, category="env_unavailable", error_message=f"cannot start OpenCLI: {exc}")

        stdout_task = asyncio.create_task(_read_capped(process.stdout, STDOUT_LIMIT_BYTES))
        stderr_task = asyncio.create_task(_read_capped(process.stderr, STDERR_LIMIT_BYTES))
        killed = False
        too_large = False
        try:
            done, _ = await asyncio.wait({stdout_task}, timeout=max(1.0, timeout_s))
            if stdout_task in done and stdout_task.result()[1]:
                too_large = True
            if not done or too_large:
                killed = True
                await _kill_tree(process)
            else:
                await asyncio.wait_for(process.wait(), timeout=max(1.0, timeout_s))
        except asyncio.TimeoutError:
            killed = True
            await _kill_tree(process)
        except asyncio.CancelledError:
            # Task cancellation must still end the whole process tree before
            # the caller releases the worker page.
            killed = True
            await _cancel_command(process)
        finally:
            if killed:
                for task in (stdout_task, stderr_task):
                    if not task.done():
                        task.cancel()

        stdout = stdout_task.result()[0] if stdout_task.done() and not stdout_task.cancelled() else b""
        stderr = stderr_task.result()[0] if stderr_task.done() and not stderr_task.cancelled() else b""
        if not stderr_task.done():
            try:
                stderr, _ = await asyncio.wait_for(stderr_task, timeout=1.0)
            except asyncio.TimeoutError:
                stderr = b""
            except asyncio.CancelledError:
                await _cancel_command(process)
        stderr_text = stderr.decode("utf-8", errors="replace")

        if too_large:
            return RunOutcome(
                started=True, category="error", killed=True, output_too_large=True,
                error_code="OUTPUT_TOO_LARGE",
                error_message="command output exceeded the 16 MiB limit; narrow the query (for example a smaller limit)",
            )
        if killed:
            return RunOutcome(started=True, category="timeout", killed=True, error_code="TIMEOUT",
                              error_message=f"command did not finish within {timeout_s:.0f}s")

        exit_code = process.returncode
        category = classify_exit(exit_code)
        if category in {"ok", "empty"} and exit_code == 0:
            text = stdout.decode("utf-8", errors="replace").strip()
            if not text:
                return RunOutcome(started=True, category="empty", rows=[], exit_code=exit_code)
            try:
                rows = json.loads(text)
            except json.JSONDecodeError:
                return RunOutcome(started=True, category="error", exit_code=exit_code,
                                  error_code="INVALID_OUTPUT", error_message=text[-2000:])
            empty = rows is None or rows == [] or rows == {}
            return RunOutcome(started=True, category="empty" if empty else "ok", rows=rows, exit_code=exit_code)
        code, message, help_text = parse_error_envelope(stderr_text)
        return RunOutcome(
            started=True,
            category=category,  # type: ignore[arg-type]
            rows=[] if category == "empty" else None,
            exit_code=exit_code,
            error_code=code,
            error_message=message,
            error_help=help_text,
        )
