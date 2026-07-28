# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Process-safe executors behind the structured ``opencli_execute`` tool."""

from __future__ import annotations

import asyncio
import json
import subprocess
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

from jiuwenswarm.agents.harness.common.opencli.contracts import (
    OpenCLICommandContract,
)
from jiuwenswarm.agents.harness.common.opencli.executors.launcher import (
    OpenCLILauncherError,
    resolve_opencli_launcher,
    resolve_opencli_package_version,
)

_PROCESS_TIMEOUT_SECONDS = 300.0
_MAX_STDOUT_CHARS = 20_000
_MAX_ERROR_DETAIL_CHARS = 4_000
_XIAOHONGSHU_EXECUTOR = "xiaohongshu_guarded_publish"
_GENERIC_READ_EXECUTOR = "generic_manifest_read"
_XIAOHONGSHU_RUNTIME_MODULE = (
    "jiuwenswarm.agents.harness.common.opencli.executors.xiaohongshu_publish"
)


class _InvalidJSON(ValueError):
    pass


class OpenCLIExecutionError(RuntimeError):
    """Typed failure before or during guarded executor dispatch."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        attempted: bool,
        fallback_allowed: bool,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.attempted = bool(attempted)
        self.fallback_allowed = bool(fallback_allowed) and not self.attempted


class OpenCLIExecutor:
    """Dispatch reviewed command contracts without exposing a shell to the model."""

    def __init__(
        self,
        *,
        process_runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
        timeout_seconds: float = _PROCESS_TIMEOUT_SECONDS,
        launcher_resolver: Callable[[], Sequence[str]] | None = None,
        launcher_version_probe: Callable[[Sequence[str]], str] | None = None,
    ) -> None:
        self._process_runner = process_runner or subprocess.run
        self._timeout_seconds = timeout_seconds
        self._launcher_resolver = launcher_resolver or resolve_opencli_launcher
        self._launcher_version_probe = (
            launcher_version_probe or resolve_opencli_package_version
        )

    async def execute(
        self,
        contract: OpenCLICommandContract,
        *,
        workspace_roots: Sequence[str | Path],
        payload_path: str | None = None,
        arguments: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Run one custom or manifest-bound executor without a command shell."""
        executor_name = str(getattr(contract, "executor", "") or "").strip()
        if executor_name == _GENERIC_READ_EXECUTOR:
            cwd = self.resolve_workspace_root(workspace_roots)
            argv = self._build_generic_argv(contract, arguments)
            result_kind = "generic"
        else:
            if arguments is not None:
                raise OpenCLIExecutionError(
                    "opencli_arguments_unsupported",
                    "The reviewed custom executor does not accept arguments",
                    attempted=False,
                    fallback_allowed=False,
                )
            resolved_payload = self.resolve_payload_path(
                str(payload_path or ""),
                workspace_roots,
            )
            cwd = resolved_payload.parent
            argv = self._build_custom_argv(contract, resolved_payload)
            result_kind = "custom"

        started = time.monotonic()
        process_task = asyncio.create_task(
            asyncio.to_thread(
                self._process_runner,
                argv,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                cwd=str(cwd),
                shell=False,
                timeout=self._timeout_seconds,
            )
        )
        try:
            # Do not orphan a possibly mutating subprocess when the Agent task is
            # cancelled. Shield the worker, wait for its bounded completion, then
            # propagate cancellation so the caller still sees an interrupted tool.
            completed = await asyncio.shield(process_task)
        except asyncio.CancelledError:
            try:
                await asyncio.shield(process_task)
            except Exception:
                # The caller is already cancelled. The important invariant is
                # that the bounded worker reached a terminal state, not which
                # process error it produced after cancellation.
                pass
            raise
        except subprocess.TimeoutExpired as exc:
            raise OpenCLIExecutionError(
                "opencli_executor_timeout",
                "The guarded OpenCLI executor timed out; the write outcome may be unknown",
                attempted=True,
                fallback_allowed=False,
            ) from exc
        except OSError as exc:
            raise OpenCLIExecutionError(
                "opencli_executor_start_failed",
                f"The guarded OpenCLI executor could not start: {type(exc).__name__}",
                attempted=False,
                fallback_allowed=True,
            ) from exc

        latency_ms = max(0, round((time.monotonic() - started) * 1000))
        if result_kind == "generic":
            return self._generic_result(
                contract,
                completed,
                latency_ms=latency_ms,
            )
        envelope = self._parse_envelope(completed.stdout)
        self._validate_custom_envelope(envelope, completed.returncode)
        return {
            "ok": bool(envelope.get("ok")) and completed.returncode == 0,
            "site": contract.site,
            "operation": contract.operation,
            "command": contract.command,
            "mode": envelope.get("mode", "unknown"),
            "attempted": True,
            "fallback_allowed": False,
            "result": envelope.get("result"),
            "error": envelope.get("error"),
            "exit_code": completed.returncode,
            "latency_ms": latency_ms,
        }

    @staticmethod
    def resolve_payload_path(
        payload_path: str,
        workspace_roots: Sequence[str | Path],
    ) -> Path:
        """Resolve a payload file while rejecting traversal and out-of-workspace reads."""
        raw_path = str(payload_path or "").strip()
        if not raw_path:
            raise OpenCLIExecutionError(
                "opencli_payload_path_missing",
                "payload_path is required",
                attempted=False,
                fallback_allowed=False,
            )

        roots: list[Path] = []
        for root in workspace_roots:
            try:
                resolved_root = Path(root).expanduser().resolve()
            except (OSError, RuntimeError, ValueError):
                continue
            if resolved_root not in roots:
                roots.append(resolved_root)
        if not roots:
            raise OpenCLIExecutionError(
                "opencli_workspace_unavailable",
                "No trusted workspace boundary is available for the payload",
                attempted=False,
                fallback_allowed=True,
            )

        candidate = Path(raw_path).expanduser()
        if not candidate.is_absolute():
            candidate = roots[0] / candidate
        try:
            resolved_candidate = candidate.resolve(strict=True)
        except (FileNotFoundError, OSError, RuntimeError) as exc:
            raise OpenCLIExecutionError(
                "opencli_payload_missing",
                "The OpenCLI payload file does not exist",
                attempted=False,
                fallback_allowed=False,
            ) from exc
        if not resolved_candidate.is_file():
            raise OpenCLIExecutionError(
                "opencli_payload_not_file",
                "The OpenCLI payload path must point to a regular file",
                attempted=False,
                fallback_allowed=False,
            )
        if not any(
            resolved_candidate == root or root in resolved_candidate.parents
            for root in roots
        ):
            raise OpenCLIExecutionError(
                "opencli_payload_outside_workspace",
                "The OpenCLI payload must stay inside the current trusted workspace",
                attempted=False,
                fallback_allowed=False,
            )
        return resolved_candidate

    @staticmethod
    def resolve_workspace_root(
        workspace_roots: Sequence[str | Path],
    ) -> Path:
        """Return the first existing trusted workspace directory."""
        for root in workspace_roots:
            try:
                candidate = Path(root).expanduser().resolve(strict=True)
            except (FileNotFoundError, OSError, RuntimeError, ValueError):
                continue
            if candidate.is_dir():
                return candidate
        raise OpenCLIExecutionError(
            "opencli_workspace_unavailable",
            "No trusted workspace boundary is available for OpenCLI",
            attempted=False,
            fallback_allowed=True,
        )

    def _build_custom_argv(
        self,
        contract: OpenCLICommandContract,
        payload_path: Path,
    ) -> list[str]:
        if (
            contract.executor != _XIAOHONGSHU_EXECUTOR
            or contract.site != "xiaohongshu"
            or contract.operation != "publishing"
            or contract.command != "publish"
        ):
            raise OpenCLIExecutionError(
                "opencli_executor_unsupported",
                "The disclosed command has no reviewed structured executor",
                attempted=False,
                fallback_allowed=True,
            )
        _, expected_version = self._resolve_bound_launcher(contract)
        return [
            sys.executable,
            "-E",
            "-I",
            "-m",
            _XIAOHONGSHU_RUNTIME_MODULE,
            "--payload",
            str(payload_path),
            "--expected-opencli-version",
            expected_version,
        ]

    def _build_generic_argv(
        self,
        contract: OpenCLICommandContract,
        arguments: Mapping[str, Any] | None,
    ) -> list[str]:
        from jiuwenswarm.agents.harness.common.opencli.executors.manifest import (
            render_manifest_command_argv,
        )

        if arguments is None:
            raise OpenCLIExecutionError(
                "opencli_arguments_invalid",
                "arguments must be provided for a generic manifest read",
                attempted=False,
                fallback_allowed=False,
            )
        command_argv = render_manifest_command_argv(contract, arguments)
        launcher, _ = self._resolve_bound_launcher(contract)
        return [
            *launcher,
            *command_argv,
        ]

    def _resolve_bound_launcher(
        self,
        contract: OpenCLICommandContract,
    ) -> tuple[list[str], str]:
        expected_version = getattr(contract, "opencli_version", None)
        try:
            raw_launcher = self._launcher_resolver()
            if isinstance(raw_launcher, (str, bytes)):
                raise TypeError("launcher argv must be a sequence of tokens")
            launcher = list(raw_launcher)
            if not launcher or any(
                not isinstance(token, str) or not token or "\x00" in token
                for token in launcher
            ):
                raise ValueError("launcher argv contains an invalid token")
            installed_version = self._launcher_version_probe(launcher)
        except (
            OpenCLILauncherError,
            OSError,
            RuntimeError,
            TypeError,
            ValueError,
        ) as exc:
            raise OpenCLIExecutionError(
                "opencli_catalog_drift",
                "The installed OpenCLI version cannot be bound to the reviewed catalog",
                attempted=False,
                fallback_allowed=True,
            ) from exc
        if (
            not isinstance(expected_version, str)
            or not expected_version
            or expected_version != expected_version.strip()
            or not isinstance(installed_version, str)
            or installed_version != expected_version
        ):
            raise OpenCLIExecutionError(
                "opencli_catalog_drift",
                "The installed OpenCLI version does not match the reviewed catalog",
                attempted=False,
                fallback_allowed=True,
            )
        return launcher, expected_version

    @classmethod
    def _parse_envelope(cls, stdout: str | None) -> dict[str, Any]:
        value = str(stdout or "")
        if len(value) > _MAX_STDOUT_CHARS:
            raise OpenCLIExecutionError(
                "opencli_executor_output_too_large",
                "The guarded OpenCLI executor returned an oversized response",
                attempted=True,
                fallback_allowed=False,
            )
        try:
            parsed = _strict_json_loads(value)
        except (json.JSONDecodeError, _InvalidJSON) as exc:
            raise OpenCLIExecutionError(
                "opencli_executor_output_invalid",
                "The guarded OpenCLI executor returned invalid JSON",
                attempted=True,
                fallback_allowed=False,
            ) from exc
        if not isinstance(parsed, dict):
            raise OpenCLIExecutionError(
                "opencli_executor_output_invalid",
                "The guarded OpenCLI executor response must be a JSON object",
                attempted=True,
                fallback_allowed=False,
            )
        return parsed

    @staticmethod
    def _validate_custom_envelope(
        envelope: dict[str, Any],
        return_code: int,
    ) -> None:
        ok = envelope.get("ok")
        mode = envelope.get("mode")
        attempted = envelope.get("attempted")
        fallback_allowed = envelope.get("fallback_allowed")
        if (
            not isinstance(ok, bool)
            or ok != (return_code == 0)
            or not isinstance(mode, str)
            or mode not in {"draft", "publish", "unknown"}
            or not isinstance(attempted, bool)
            or not isinstance(fallback_allowed, bool)
        ):
            raise OpenCLIExecutionError(
                "opencli_executor_output_invalid",
                "The guarded OpenCLI executor returned an inconsistent response",
                attempted=True,
                fallback_allowed=False,
            )
        if ok:
            if "result" not in envelope or envelope.get("error") is not None:
                raise OpenCLIExecutionError(
                    "opencli_executor_output_invalid",
                    "The guarded OpenCLI executor success is incomplete",
                    attempted=True,
                    fallback_allowed=False,
                )
            return
        error = envelope.get("error")
        if not isinstance(error, dict):
            raise OpenCLIExecutionError(
                "opencli_executor_output_invalid",
                "The guarded OpenCLI executor failure has no error object",
                attempted=True,
                fallback_allowed=False,
            )
        code = error.get("code")
        message = error.get("message")
        detail = error.get("detail")
        if (
            not isinstance(code, str)
            or not code.strip()
            or not isinstance(message, str)
            or not message.strip()
            or (detail is not None and not isinstance(detail, str))
        ):
            raise OpenCLIExecutionError(
                "opencli_executor_output_invalid",
                "The guarded OpenCLI executor failure is missing its code or message",
                attempted=True,
                fallback_allowed=False,
            )

    @classmethod
    def _generic_result(
        cls,
        contract: OpenCLICommandContract,
        completed: subprocess.CompletedProcess[str],
        *,
        latency_ms: int,
    ) -> dict[str, Any]:
        result: Any = None
        error: dict[str, str] | None = None
        if completed.returncode == 0:
            result = cls._parse_generic_json(completed.stdout)
        else:
            detail = cls._bounded_error_detail(
                completed.stderr or completed.stdout,
            )
            error = {
                "code": "opencli_failed",
                "message": "OpenCLI returned a non-zero exit code",
            }
            if detail:
                error["detail"] = detail
        return {
            "ok": completed.returncode == 0,
            "site": contract.site,
            "operation": contract.operation,
            "command": contract.command,
            "mode": "read",
            "attempted": True,
            "fallback_allowed": False,
            "result": result,
            "error": error,
            "exit_code": completed.returncode,
            "latency_ms": latency_ms,
        }

    @classmethod
    def _parse_generic_json(cls, stdout: str | None) -> Any:
        value = str(stdout or "")
        if len(value) > _MAX_STDOUT_CHARS:
            raise OpenCLIExecutionError(
                "opencli_executor_output_too_large",
                "OpenCLI returned an oversized JSON response",
                attempted=True,
                fallback_allowed=False,
            )
        try:
            return _strict_json_loads(value)
        except (json.JSONDecodeError, _InvalidJSON) as exc:
            raise OpenCLIExecutionError(
                "opencli_executor_output_invalid",
                "OpenCLI returned invalid JSON",
                attempted=True,
                fallback_allowed=False,
            ) from exc

    @staticmethod
    def _bounded_error_detail(value: str | None) -> str:
        text = str(value or "").strip()
        if len(text) <= _MAX_ERROR_DETAIL_CHARS:
            return text
        return f"{text[:_MAX_ERROR_DETAIL_CHARS]}…"


def _strict_json_loads(value: str) -> Any:
    return json.loads(
        value,
        object_pairs_hook=_unique_json_object,
        parse_constant=_reject_json_constant,
    )


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _InvalidJSON(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise _InvalidJSON(f"non-finite JSON number: {value}")


__all__ = [
    "OpenCLIExecutionError",
    "OpenCLIExecutor",
]
