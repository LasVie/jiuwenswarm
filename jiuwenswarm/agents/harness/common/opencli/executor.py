# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Process-safe executors behind the structured ``opencli_execute`` tool."""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
import time
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from jiuwenswarm.agents.harness.common.opencli.contracts import (
    OpenCLICommandContract,
)

_PROCESS_TIMEOUT_SECONDS = 300.0
_MAX_STDOUT_CHARS = 20_000
_SUPPORTED_EXECUTOR = "xiaohongshu_guarded_publish"


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
        self.attempted = attempted
        self.fallback_allowed = fallback_allowed


class OpenCLIExecutor:
    """Dispatch reviewed command contracts without exposing a shell to the model."""

    def __init__(
        self,
        *,
        process_runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
        timeout_seconds: float = _PROCESS_TIMEOUT_SECONDS,
    ) -> None:
        self._process_runner = process_runner or subprocess.run
        self._timeout_seconds = timeout_seconds

    async def execute(
        self,
        contract: OpenCLICommandContract,
        *,
        payload_path: str,
        workspace_roots: Sequence[str | Path],
    ) -> dict[str, Any]:
        """Validate the payload boundary and run the contract's guarded executor."""
        resolved_payload = self.resolve_payload_path(payload_path, workspace_roots)
        argv = self._build_argv(contract, resolved_payload)
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
                cwd=str(resolved_payload.parent),
                env={
                    **os.environ,
                    "PYTHONIOENCODING": "utf-8",
                },
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
        envelope = self._parse_envelope(completed.stdout)
        return {
            "ok": bool(envelope.get("ok")) and completed.returncode == 0,
            "site": contract.site,
            "operation": contract.operation,
            "command": contract.command,
            "mode": envelope.get("mode", "unknown"),
            "attempted": bool(envelope.get("attempted", completed.returncode == 0)),
            "fallback_allowed": bool(envelope.get("fallback_allowed", False)),
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
    def _build_argv(
        contract: OpenCLICommandContract,
        payload_path: Path,
    ) -> list[str]:
        if (
            contract.executor != _SUPPORTED_EXECUTOR
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
        wrapper = (
            contract.skill_root
            / "sites"
            / "xiaohongshu"
            / "scripts"
            / "publish.py"
        ).resolve()
        if (
            wrapper != contract.skill_root
            and contract.skill_root not in wrapper.parents
        ):
            raise OpenCLIExecutionError(
                "opencli_executor_path_invalid",
                "The guarded executor resolved outside the installed Skill",
                attempted=False,
                fallback_allowed=True,
            )
        if not wrapper.is_file():
            raise OpenCLIExecutionError(
                "opencli_executor_missing",
                "The guarded OpenCLI executor is not installed",
                attempted=False,
                fallback_allowed=True,
            )
        return [
            sys.executable,
            "-E",
            str(wrapper),
            "--payload",
            str(payload_path),
        ]

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
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
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


__all__ = [
    "OpenCLIExecutionError",
    "OpenCLIExecutor",
]
