# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""The main-Agent-only structured OpenCLI execution tool."""

from __future__ import annotations

import hashlib
from collections.abc import AsyncIterator, Callable, Sequence
from pathlib import Path
from typing import Any

from openjiuwen.core.foundation.tool import Tool, ToolCard
from openjiuwen.harness.tools import ToolOutput

from jiuwenswarm.agents.harness.common.opencli.contracts import (
    OpenCLIContractError,
    load_operation_contract,
)
from jiuwenswarm.agents.harness.common.opencli.disclosure import (
    DisclosureReceiptStore,
)
from jiuwenswarm.agents.harness.common.opencli.executor import (
    OpenCLIExecutionError,
    OpenCLIExecutor,
)

OPENCLI_EXECUTE_TOOL_NAME = "opencli_execute"
PathSource = str | Path | Callable[[], str | Path]
WorkspaceRootsSource = (
    Sequence[str | Path] | Callable[[], Sequence[str | Path]]
)

_DESCRIPTIONS = {
    "cn": (
        "执行已由 opencli-web operation 合同披露的 OpenCLI 网页操作。仅主 Agent "
        "可调用；调用前必须在当前会话中用 skill_tool 读取精确 operation 文件。"
    ),
    "en": (
        "Execute an OpenCLI website operation disclosed by an opencli-web "
        "operation contract. Main Agent only: first read the exact operation "
        "file with skill_tool in the current session."
    ),
}


def _input_schema(language: str) -> dict[str, Any]:
    descriptions = {
        "cn": {
            "site": "operation 合同声明的网站标识，例如 xiaohongshu。",
            "operation": "第三层 operation 合同名，例如 publishing。",
            "command": "operation 合同明确授权的命令，例如 publish。",
            "payload_path": "当前可信工作区内的 UTF-8 JSON payload 文件路径。",
        },
        "en": {
            "site": "Site identifier declared by the operation contract, such as xiaohongshu.",
            "operation": "Third-level operation contract name, such as publishing.",
            "command": "Command explicitly authorized by the operation contract, such as publish.",
            "payload_path": "Path to a UTF-8 JSON payload file inside the trusted workspace.",
        },
    }
    selected = descriptions.get(language, descriptions["cn"])
    return {
        "type": "object",
        "properties": {
            name: {"type": "string", "description": description}
            for name, description in selected.items()
        },
        "required": ["site", "operation", "command", "payload_path"],
        "additionalProperties": False,
    }


class OpenCLIExecuteTool(Tool):
    """Validate disclosure and dispatch one reviewed OpenCLI executor."""

    def __init__(
        self,
        *,
        scope: str,
        skills_root: PathSource,
        workspace_roots: WorkspaceRootsSource,
        receipt_store: DisclosureReceiptStore,
        language: str = "cn",
        agent_id: str | None = None,
        executor: OpenCLIExecutor | None = None,
    ) -> None:
        scope_digest = hashlib.sha256(scope.encode("utf-8")).hexdigest()[:12]
        owner = str(agent_id or "main")
        super().__init__(
            ToolCard(
                id=f"OpenCLIExecute_{owner}_{scope_digest}",
                name=OPENCLI_EXECUTE_TOOL_NAME,
                description=_DESCRIPTIONS.get(language, _DESCRIPTIONS["cn"]),
                input_params=_input_schema(language),
                parallel_safe=False,
                stateless=False,
            )
        )
        self._scope = scope
        self._skills_root = skills_root
        self._workspace_roots = workspace_roots
        self._receipt_store = receipt_store
        self._executor = executor or OpenCLIExecutor()

    async def invoke(self, inputs: dict[str, Any], **kwargs: Any) -> ToolOutput:
        del kwargs
        site = str(inputs.get("site") or "").strip()
        operation = str(inputs.get("operation") or "").strip()
        command = str(inputs.get("command") or "").strip()
        payload_path = str(inputs.get("payload_path") or "").strip()

        try:
            skills_root = Path(self._resolve_source(self._skills_root)).expanduser()
            operation_contract = load_operation_contract(
                skills_root,
                site,
                operation,
            )
            command_contract = operation_contract.command_contract(command)
            workspace_roots = list(self._resolve_source(self._workspace_roots))
            resolved_payload = self._executor.resolve_payload_path(
                payload_path,
                workspace_roots,
            )
        except OpenCLIContractError as exc:
            return self._failure(
                exc.code,
                exc.message,
                site=site,
                operation=operation,
                command=command,
                attempted=False,
                fallback_allowed=True,
            )
        except OpenCLIExecutionError as exc:
            return self._failure(
                exc.code,
                exc.message,
                site=site,
                operation=operation,
                command=command,
                attempted=exc.attempted,
                fallback_allowed=exc.fallback_allowed,
            )
        except (OSError, RuntimeError, TypeError, ValueError) as exc:
            return self._failure(
                "opencli_runtime_context_invalid",
                f"OpenCLI runtime context is invalid: {type(exc).__name__}",
                site=site,
                operation=operation,
                command=command,
                attempted=False,
                fallback_allowed=True,
            )

        receipt = self._receipt_store.consume(
            scope=self._scope,
            site=command_contract.site,
            operation=command_contract.operation,
            operation_sha256=command_contract.operation_sha256,
        )
        if not receipt.accepted:
            return self._failure(
                receipt.code,
                (
                    "Read the exact operation contract with skill_tool in the "
                    "main Agent immediately before calling opencli_execute"
                ),
                site=site,
                operation=operation,
                command=command,
                attempted=False,
                fallback_allowed=False,
            )

        try:
            result = await self._executor.execute(
                command_contract,
                payload_path=str(resolved_payload),
                workspace_roots=workspace_roots,
            )
        except OpenCLIExecutionError as exc:
            return self._failure(
                exc.code,
                exc.message,
                site=site,
                operation=operation,
                command=command,
                attempted=exc.attempted,
                fallback_allowed=exc.fallback_allowed,
            )

        if result["ok"]:
            return ToolOutput(success=True, data=result)
        error = result.get("error")
        error_mapping = error if isinstance(error, dict) else {}
        code = str(error_mapping.get("code") or "opencli_failed")
        message = str(
            error_mapping.get("message")
            or "OpenCLI returned a non-zero or unsuccessful result"
        )
        return ToolOutput(
            success=False,
            data=result,
            error=f"{code}: {message}",
        )

    async def stream(
        self,
        inputs: dict[str, Any],
        **kwargs: Any,
    ) -> AsyncIterator[ToolOutput]:
        del inputs, kwargs
        if False:
            yield ToolOutput(success=False)

    @staticmethod
    def _resolve_source(value: Any) -> Any:
        return value() if callable(value) else value

    @staticmethod
    def _failure(
        code: str,
        message: str,
        *,
        site: str,
        operation: str,
        command: str,
        attempted: bool,
        fallback_allowed: bool,
    ) -> ToolOutput:
        data = {
            "ok": False,
            "site": site,
            "operation": operation,
            "command": command,
            "attempted": attempted,
            "fallback_allowed": fallback_allowed,
            "error": {
                "code": code,
                "message": message,
            },
        }
        return ToolOutput(
            success=False,
            data=data,
            error=f"{code}: {message}",
        )


__all__ = [
    "OPENCLI_EXECUTE_TOOL_NAME",
    "OpenCLIExecuteTool",
]
