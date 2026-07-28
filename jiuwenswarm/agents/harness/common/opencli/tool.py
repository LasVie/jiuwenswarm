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
    load_terminal_contract,
)
from jiuwenswarm.agents.harness.common.opencli.disclosure import (
    DisclosureReceiptStore,
)
from jiuwenswarm.agents.harness.common.opencli.executor import (
    OpenCLIExecutionError,
    OpenCLIExecutor,
)
from jiuwenswarm.agents.harness.common.opencli.preparation import (
    PayloadPreparationError,
    PreparedPayload,
    prepare_xiaohongshu_payload,
)
from jiuwenswarm.agents.harness.common.opencli.security import (
    load_skill_enabled_snapshot,
)

OPENCLI_EXECUTE_TOOL_NAME = "opencli_execute"
PathSource = str | Path | Callable[[], str | Path]
WorkspaceRootsSource = Sequence[str | Path] | Callable[[], Sequence[str | Path]]

_DESCRIPTIONS = {
    "cn": (
        "执行已由 opencli-web terminal 合同披露的 OpenCLI 网页操作。仅主 Agent "
        "可调用；调用前必须在当前会话中用 skill_tool 读取精确站点或 operation "
        "terminal 文件。"
    ),
    "en": (
        "Execute an OpenCLI website operation disclosed by an opencli-web "
        "terminal contract. Main Agent only: first read the exact site or "
        "operation terminal file with skill_tool in the current session."
    ),
}


def _input_schema(language: str) -> dict[str, Any]:
    descriptions = {
        "cn": {
            "site": "operation 合同声明的网站标识，例如 xiaohongshu。",
            "operation": "terminal 合同的逻辑 operation 名，例如 publishing。",
            "command": "terminal 合同明确声明的命令，例如 publish。",
            "arguments": "通用只读命令的结构化参数对象；键和类型必须匹配冻结 catalog。",
            "payload_path": "仅 custom executor 使用的可信工作区 UTF-8 JSON payload 路径。",
        },
        "en": {
            "site": "Site identifier declared by the terminal contract.",
            "operation": "Logical operation declared by the terminal contract.",
            "command": "Command explicitly declared by the terminal contract.",
            "arguments": "Structured generic-read arguments bound to the frozen catalog schema.",
            "payload_path": "Trusted-workspace UTF-8 JSON payload path for a custom executor only.",
        },
    }
    selected = descriptions.get(language, descriptions["cn"])
    return {
        "type": "object",
        "properties": {
            "site": {"type": "string", "description": selected["site"]},
            "operation": {
                "type": "string",
                "description": selected["operation"],
            },
            "command": {"type": "string", "description": selected["command"]},
            "arguments": {
                "type": "object",
                "description": selected["arguments"],
            },
            "payload_path": {
                "type": "string",
                "description": selected["payload_path"],
            },
        },
        "required": ["site", "operation", "command"],
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
        raw_payload_path = inputs.get("payload_path")
        payload_path = (
            str(raw_payload_path).strip() if raw_payload_path is not None else None
        )
        arguments = inputs.get("arguments")

        try:
            skills_root = Path(self._resolve_source(self._skills_root)).expanduser()
            enabled_snapshot = load_skill_enabled_snapshot(skills_root)
            if not enabled_snapshot.enabled:
                return self._failure(
                    enabled_snapshot.code,
                    "The global opencli-web Skill is disabled or has invalid state",
                    site=site,
                    operation=operation,
                    command=command,
                    attempted=False,
                    fallback_allowed=False,
                )
            operation_contract = load_terminal_contract(
                skills_root,
                site,
                operation,
            )
            command_contract = operation_contract.command_contract(command)
            workspace_roots = list(self._resolve_source(self._workspace_roots))
            if command_contract.execution_state not in {"enabled", "custom"}:
                return self._failure(
                    "opencli_command_disabled",
                    (
                        "The disclosed command is documented but has no "
                        "reviewed OpenCLI execution authority"
                    ),
                    site=site,
                    operation=operation,
                    command=command,
                    attempted=False,
                    fallback_allowed=(
                        command_contract.fallback.before_dispatch == "browser_agent"
                    ),
                )
            resolved_payload: Path | None = None
            if command_contract.execution_state == "custom":
                if arguments is not None:
                    raise OpenCLIExecutionError(
                        "opencli_arguments_unsupported",
                        "The custom executor accepts payload_path, not arguments",
                        attempted=False,
                        fallback_allowed=False,
                    )
                resolved_payload = self._executor.resolve_payload_path(
                    str(payload_path or ""),
                    workspace_roots,
                )
            else:
                if payload_path is not None:
                    raise OpenCLIExecutionError(
                        "opencli_payload_unsupported",
                        "The generic read executor accepts arguments, not payload_path",
                        attempted=False,
                        fallback_allowed=False,
                    )
                if not isinstance(arguments, dict):
                    raise OpenCLIExecutionError(
                        "opencli_arguments_invalid",
                        "arguments must be an object for a generic manifest read",
                        attempted=False,
                        fallback_allowed=False,
                    )
        except OpenCLIContractError as exc:
            return self._failure(
                exc.code,
                exc.message,
                site=site,
                operation=operation,
                command=command,
                attempted=False,
                fallback_allowed=self._contract_fallback_allowed(exc.code),
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

        if command_contract.manifest_backed:
            receipt = self._receipt_store.consume_bound(
                scope=self._scope,
                site=command_contract.site,
                operation=command_contract.operation,
                terminal_relative_path=(command_contract.terminal_relative_path),
                terminal_sha256=command_contract.terminal_sha256,
                policy_sha256=command_contract.policy_sha256,
                enabled_state_sha256=enabled_snapshot.state_sha256,
            )
        else:
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
                    "Read the exact terminal contract with skill_tool in the "
                    "same main Agent immediately before opencli_execute"
                ),
                site=site,
                operation=operation,
                command=command,
                attempted=False,
                fallback_allowed=False,
            )

        final_enabled_snapshot = load_skill_enabled_snapshot(skills_root)
        if (
            not final_enabled_snapshot.enabled
            or final_enabled_snapshot.state_sha256 != enabled_snapshot.state_sha256
        ):
            return self._failure(
                final_enabled_snapshot.code
                if not final_enabled_snapshot.enabled
                else "opencli_skill_state_changed",
                "The global opencli-web enabled state changed before dispatch",
                site=site,
                operation=operation,
                command=command,
                attempted=False,
                fallback_allowed=False,
            )

        prepared_payload: PreparedPayload | None = None
        result: dict[str, Any] | None = None
        preparation_failure: PayloadPreparationError | None = None
        execution_failure: OpenCLIExecutionError | None = None
        cleanup_failure: PayloadPreparationError | None = None
        try:
            execution_payload = (
                str(resolved_payload) if resolved_payload is not None else None
            )
            execution_workspace_roots = list(workspace_roots)
            if command_contract.execution_state == "custom":
                if (
                    command_contract.site != "xiaohongshu"
                    or command_contract.operation != "publishing"
                    or command_contract.command != "publish"
                ):
                    raise PayloadPreparationError(
                        "opencli_custom_payload_unsupported",
                        "No reviewed payload preparation is registered",
                    )
                prepared_payload = prepare_xiaohongshu_payload(
                    str(resolved_payload),
                    workspace_roots,
                )
                if prepared_payload.mode == "publish":
                    raise PayloadPreparationError(
                        "opencli_confirmation_untrusted",
                        (
                            "Public publishing is disabled until the runtime "
                            "can verify a scope- and payload-bound user "
                            "confirmation receipt"
                        ),
                    )
                prepared_payload.verify()
                execution_payload = str(prepared_payload.payload_path)
                execution_workspace_roots.append(prepared_payload.staging_directory)

            result = await self._executor.execute(
                command_contract,
                workspace_roots=execution_workspace_roots,
                payload_path=execution_payload,
                arguments=arguments if isinstance(arguments, dict) else None,
            )
        except PayloadPreparationError as exc:
            preparation_failure = exc
        except OpenCLIExecutionError as exc:
            execution_failure = exc
        finally:
            if prepared_payload is not None:
                try:
                    prepared_payload.cleanup()
                except PayloadPreparationError as exc:
                    cleanup_failure = exc

        if cleanup_failure is not None:
            attempted = bool(
                isinstance(result, dict) and result.get("attempted") is True
            )
            return self._failure(
                cleanup_failure.code,
                cleanup_failure.message,
                site=site,
                operation=operation,
                command=command,
                attempted=attempted,
                fallback_allowed=False,
            )
        if preparation_failure is not None:
            return self._failure(
                preparation_failure.code,
                preparation_failure.message,
                site=site,
                operation=operation,
                command=command,
                attempted=False,
                fallback_allowed=False,
            )
        if execution_failure is not None:
            return self._failure(
                execution_failure.code,
                execution_failure.message,
                site=site,
                operation=operation,
                command=command,
                attempted=execution_failure.attempted,
                fallback_allowed=execution_failure.fallback_allowed,
            )

        if not isinstance(result, dict):
            return self._failure(
                "opencli_executor_output_invalid",
                "The OpenCLI executor returned an invalid result envelope",
                site=site,
                operation=operation,
                command=command,
                attempted=True,
                fallback_allowed=False,
            )
        if (
            not isinstance(result.get("ok"), bool)
            or not isinstance(result.get("attempted"), bool)
            or not isinstance(result.get("fallback_allowed"), bool)
        ):
            return self._failure(
                "opencli_executor_output_invalid",
                "The OpenCLI executor returned an incomplete result envelope",
                site=site,
                operation=operation,
                command=command,
                attempted=True,
                fallback_allowed=False,
            )
        result = dict(result)
        result["fallback_allowed"] = (
            result["fallback_allowed"] and not result["attempted"]
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
    def _contract_fallback_allowed(code: str) -> bool:
        return code in {
            "opencli_command_not_disclosed",
            "opencli_contract_missing",
            "opencli_contract_not_executable",
            "opencli_contract_not_registered",
        }

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
        normalized_attempted = bool(attempted)
        data = {
            "ok": False,
            "site": site,
            "operation": operation,
            "command": command,
            "attempted": normalized_attempted,
            "fallback_allowed": (bool(fallback_allowed) and not normalized_attempted),
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
