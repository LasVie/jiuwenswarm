# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Load machine-readable execution metadata from OpenCLI operation contracts."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any

import yaml

from jiuwenswarm.agents.harness.common.opencli.manifest import (
    OPENCLI_RUNTIME_MANIFEST_FILENAME,
    OpenCLICommandManifest,
    OpenCLIFallbackManifest,
    OpenCLIManifestError,
    OpenCLIOperationManifest,
    OpenCLIRuntimeManifest,
    load_runtime_manifest,
)

OPENCLI_WEB_SKILL_NAME = "opencli-web"
_SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_OPERATION_PATH_PATTERN = re.compile(
    r"^sites/(?P<site>[a-z0-9][a-z0-9-]*)/"
    r"operations/(?P<operation>[a-z0-9][a-z0-9-]*)\.md$"
)


class OpenCLIContractError(ValueError):
    """An installed operation contract is missing, invalid, or unsupported."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True, slots=True)
class OpenCLICommandContract:
    """One command authorized by an exact terminal contract."""

    site: str
    operation: str
    command: str
    executor: str
    skill_root: Path
    operation_path: Path
    operation_relative_path: str
    operation_sha256: str
    terminal_kind: str
    terminal_path: Path
    terminal_relative_path: str
    terminal_sha256: str
    policy_sha256: str
    manifest_sha256: str | None
    manifest_backed: bool
    execution_state: str
    semantic_effect: str
    risk: str
    auth: str
    transport: str
    strategy: str
    browser: bool
    opencli_version: str
    access: str
    args: tuple[Mapping[str, Any], ...]
    confirmation: str
    fallback: OpenCLIFallbackManifest
    file_inputs: tuple[str, ...]
    file_outputs: tuple[str, ...]
    sensitive_output: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class OpenCLIOperationContract:
    """Validated executable metadata for one terminal Skill document.

    The historical class name remains public for compatibility. For
    manifest-backed sites, ``operation_*`` aliases the exact site- or
    operation-terminal fields so existing guarded executors continue to work.
    """

    site: str
    operation: str
    commands: Mapping[str, str]
    skill_root: Path
    operation_path: Path
    operation_relative_path: str
    operation_sha256: str
    terminal_kind: str
    terminal_path: Path
    terminal_relative_path: str
    terminal_sha256: str
    policy_sha256: str
    manifest_sha256: str | None
    manifest_backed: bool
    command_specs: Mapping[str, OpenCLICommandManifest]

    def command_contract(self, command: str) -> OpenCLICommandContract:
        normalized = _normalize_slug(command, "command")
        executor = self.commands.get(normalized)
        command_spec = self.command_specs.get(normalized)
        if executor is None or command_spec is None:
            raise OpenCLIContractError(
                "opencli_command_not_disclosed",
                (
                    f"Command '{normalized}' is not authorized by "
                    f"{self.operation_relative_path}"
                ),
            )
        return OpenCLICommandContract(
            site=self.site,
            operation=self.operation,
            command=normalized,
            executor=executor,
            skill_root=self.skill_root,
            operation_path=self.operation_path,
            operation_relative_path=self.operation_relative_path,
            operation_sha256=self.operation_sha256,
            terminal_kind=self.terminal_kind,
            terminal_path=self.terminal_path,
            terminal_relative_path=self.terminal_relative_path,
            terminal_sha256=self.terminal_sha256,
            policy_sha256=self.policy_sha256,
            manifest_sha256=self.manifest_sha256,
            manifest_backed=self.manifest_backed,
            execution_state=command_spec.execution_state,
            semantic_effect=command_spec.semantic_effect,
            risk=command_spec.risk,
            auth=command_spec.auth,
            transport=command_spec.transport,
            strategy=command_spec.strategy,
            browser=command_spec.browser,
            opencli_version=command_spec.opencli_version,
            access=command_spec.access,
            args=command_spec.args,
            confirmation=command_spec.confirmation,
            fallback=command_spec.fallback,
            file_inputs=command_spec.file_inputs,
            file_outputs=command_spec.file_outputs,
            sensitive_output=command_spec.sensitive_output,
        )


OpenCLITerminalContract = OpenCLIOperationContract


def operation_relative_path(site: str, operation: str) -> str:
    """Return the canonical nested operation path for two validated slugs."""
    normalized_site = _normalize_slug(site, "site")
    normalized_operation = _normalize_slug(operation, "operation")
    return f"sites/{normalized_site}/operations/{normalized_operation}.md"


def parse_operation_relative_path(relative_path: str) -> tuple[str, str] | None:
    """Parse only canonical ``sites/<site>/operations/<operation>.md`` paths."""
    normalized = str(relative_path or "").strip().replace("\\", "/")
    pure_path = PurePosixPath(normalized)
    if pure_path.is_absolute() or ".." in pure_path.parts:
        return None
    match = _OPERATION_PATH_PATTERN.fullmatch(pure_path.as_posix())
    if match is None:
        return None
    return match.group("site"), match.group("operation")


def load_operation_contract(
    skills_root: str | Path,
    site: str,
    operation: str,
) -> OpenCLIOperationContract:
    """Load and validate an installed OpenCLI operation contract."""
    relative_path = operation_relative_path(site, operation)
    installed_skill_root = (
        Path(skills_root).expanduser() / OPENCLI_WEB_SKILL_NAME
    ).resolve()
    candidate = (installed_skill_root / relative_path).resolve()
    if (
        candidate != installed_skill_root
        and installed_skill_root not in candidate.parents
    ):
        raise OpenCLIContractError(
            "opencli_contract_path_invalid",
            "Operation contract resolved outside the installed opencli-web Skill",
        )
    try:
        content_bytes = candidate.read_bytes()
        content = content_bytes.decode("utf-8")
    except FileNotFoundError as exc:
        raise OpenCLIContractError(
            "opencli_contract_missing",
            f"Operation contract is not installed: {relative_path}",
        ) from exc
    except (OSError, UnicodeError) as exc:
        raise OpenCLIContractError(
            "opencli_contract_unreadable",
            f"Operation contract cannot be read: {relative_path}",
        ) from exc

    metadata = _load_frontmatter(content, relative_path)
    raw_contract = metadata.get("opencli_contract")
    if not isinstance(raw_contract, dict):
        raise OpenCLIContractError(
            "opencli_contract_not_executable",
            f"Operation contract has no structured OpenCLI entry: {relative_path}",
        )
    if raw_contract.get("version") != 1:
        raise OpenCLIContractError(
            "opencli_contract_version_unsupported",
            f"Unsupported OpenCLI contract version in {relative_path}",
        )

    normalized_site = _normalize_slug(site, "site")
    normalized_operation = _normalize_slug(operation, "operation")
    if raw_contract.get("site") != normalized_site:
        raise OpenCLIContractError(
            "opencli_contract_site_mismatch",
            f"Operation contract site does not match its path: {relative_path}",
        )
    if raw_contract.get("operation") != normalized_operation:
        raise OpenCLIContractError(
            "opencli_contract_operation_mismatch",
            f"Operation contract name does not match its path: {relative_path}",
        )

    raw_commands = raw_contract.get("commands")
    if not isinstance(raw_commands, dict) or not raw_commands:
        raise OpenCLIContractError(
            "opencli_contract_commands_missing",
            f"Operation contract declares no executable commands: {relative_path}",
        )
    commands: dict[str, str] = {}
    command_specs: dict[str, OpenCLICommandManifest] = {}
    for raw_name, raw_spec in raw_commands.items():
        name = _normalize_slug(raw_name, "command")
        if not isinstance(raw_spec, dict):
            raise OpenCLIContractError(
                "opencli_contract_command_invalid",
                f"Command '{name}' has invalid metadata in {relative_path}",
            )
        executor = str(raw_spec.get("executor") or "").strip()
        if not executor:
            raise OpenCLIContractError(
                "opencli_contract_executor_missing",
                f"Command '{name}' has no executor in {relative_path}",
            )
        commands[name] = executor
        command_specs[name] = _legacy_command_manifest(name, executor)

    operation_sha256 = hashlib.sha256(content_bytes).hexdigest()
    return OpenCLIOperationContract(
        site=normalized_site,
        operation=normalized_operation,
        commands=MappingProxyType(commands),
        skill_root=installed_skill_root,
        operation_path=candidate,
        operation_relative_path=relative_path,
        operation_sha256=operation_sha256,
        terminal_kind="operation",
        terminal_path=candidate,
        terminal_relative_path=relative_path,
        terminal_sha256=operation_sha256,
        policy_sha256=operation_sha256,
        manifest_sha256=None,
        manifest_backed=False,
        command_specs=MappingProxyType(command_specs),
    )


def load_terminal_contract(
    skills_root: str | Path,
    site: str,
    operation: str,
) -> OpenCLITerminalContract:
    """Load an explicitly registered terminal or a legacy operation v1.

    Once a runtime manifest exists, it is authoritative: unregistered
    operation documents cannot fall back to the legacy frontmatter parser.
    Site-level terminals are supported only through this explicit manifest.
    """
    normalized_site = _normalize_slug(site, "site")
    normalized_operation = _normalize_slug(operation, "operation")
    installed_skill_root = _installed_skill_root(skills_root)
    manifest_path = installed_skill_root / OPENCLI_RUNTIME_MANIFEST_FILENAME
    if not _runtime_manifest_present(manifest_path):
        return load_operation_contract(
            skills_root,
            normalized_site,
            normalized_operation,
        )
    manifest = _load_manifest_as_contract(installed_skill_root)
    operation_manifest = manifest.operation(
        normalized_site,
        normalized_operation,
    )
    if operation_manifest is None:
        raise OpenCLIContractError(
            "opencli_contract_not_registered",
            (
                "OpenCLI operation is not registered in the runtime manifest: "
                f"{normalized_site}/{normalized_operation}"
            ),
        )
    return _manifest_terminal_contract(
        installed_skill_root,
        manifest,
        normalized_site,
        operation_manifest,
    )


def load_terminal_contract_by_path(
    skills_root: str | Path,
    relative_path: str,
) -> OpenCLITerminalContract:
    """Load only a terminal whose exact relative path is authorized."""
    normalized_path = _normalize_relative_path(relative_path)
    installed_skill_root = _installed_skill_root(skills_root)
    manifest_path = installed_skill_root / OPENCLI_RUNTIME_MANIFEST_FILENAME
    if _runtime_manifest_present(manifest_path):
        manifest = _load_manifest_as_contract(installed_skill_root)
        registered = manifest.operation_for_terminal(normalized_path)
        if registered is None:
            raise OpenCLIContractError(
                "opencli_contract_not_registered",
                (
                    "Skill path is not a terminal registered in the runtime "
                    f"manifest: {normalized_path}"
                ),
            )
        site, operation_manifest = registered
        return _manifest_terminal_contract(
            installed_skill_root,
            manifest,
            site,
            operation_manifest,
        )

    parsed = parse_operation_relative_path(normalized_path)
    if parsed is None:
        raise OpenCLIContractError(
            "opencli_contract_path_invalid",
            "Skill path is not a supported legacy operation terminal",
        )
    site, operation = parsed
    return load_operation_contract(skills_root, site, operation)


def _manifest_terminal_contract(
    installed_skill_root: Path,
    manifest: OpenCLIRuntimeManifest,
    site: str,
    operation_manifest: OpenCLIOperationManifest,
) -> OpenCLITerminalContract:
    terminal = operation_manifest.terminal
    candidate = (installed_skill_root / terminal.path).resolve()
    if (
        candidate != installed_skill_root
        and installed_skill_root not in candidate.parents
    ):
        raise OpenCLIContractError(
            "opencli_contract_path_invalid",
            "Terminal contract resolved outside the installed opencli-web Skill",
        )
    try:
        content_bytes = candidate.read_bytes()
    except FileNotFoundError as exc:
        raise OpenCLIContractError(
            "opencli_contract_missing",
            f"Terminal contract is not installed: {terminal.path}",
        ) from exc
    except OSError as exc:
        raise OpenCLIContractError(
            "opencli_contract_unreadable",
            f"Terminal contract cannot be read: {terminal.path}",
        ) from exc
    content_sha256 = hashlib.sha256(content_bytes).hexdigest()
    if content_sha256 != terminal.sha256:
        raise OpenCLIContractError(
            "opencli_contract_hash_mismatch",
            (
                "Terminal contract content hash does not match the reviewed "
                f"runtime manifest: {terminal.path}"
            ),
        )
    commands = {
        name: command.executor for name, command in operation_manifest.commands.items()
    }
    return OpenCLIOperationContract(
        site=site,
        operation=operation_manifest.name,
        commands=MappingProxyType(commands),
        skill_root=installed_skill_root,
        operation_path=candidate,
        operation_relative_path=terminal.path,
        operation_sha256=terminal.sha256,
        terminal_kind=terminal.kind,
        terminal_path=candidate,
        terminal_relative_path=terminal.path,
        terminal_sha256=terminal.sha256,
        policy_sha256=operation_manifest.policy_sha256,
        manifest_sha256=manifest.manifest_sha256,
        manifest_backed=True,
        command_specs=operation_manifest.commands,
    )


def _load_manifest_as_contract(
    installed_skill_root: Path,
) -> OpenCLIRuntimeManifest:
    try:
        return load_runtime_manifest(installed_skill_root)
    except OpenCLIManifestError as exc:
        raise OpenCLIContractError(exc.code, exc.message) from exc


def _installed_skill_root(skills_root: str | Path) -> Path:
    return (Path(skills_root).expanduser() / OPENCLI_WEB_SKILL_NAME).resolve()


def _runtime_manifest_present(manifest_path: Path) -> bool:
    try:
        manifest_path.lstat()
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise OpenCLIContractError(
            "opencli_manifest_unreadable",
            "OpenCLI runtime manifest entry cannot be inspected",
        ) from exc
    return True


def _normalize_relative_path(relative_path: str) -> str:
    normalized = str(relative_path or "").strip().replace("\\", "/")
    pure_path = PurePosixPath(normalized)
    if (
        not normalized
        or pure_path.is_absolute()
        or ".." in pure_path.parts
        or pure_path.as_posix() != normalized
    ):
        raise OpenCLIContractError(
            "opencli_contract_path_invalid",
            "Terminal path must be a canonical relative Skill path",
        )
    return normalized


def _legacy_command_manifest(
    name: str,
    executor: str,
) -> OpenCLICommandManifest:
    return OpenCLICommandManifest(
        name=name,
        executor=executor,
        execution_state="custom",
        semantic_effect="public_write",
        risk="high",
        auth="required",
        transport="browser_dom",
        strategy="ui",
        browser=True,
        opencli_version="",
        access="write",
        args=(),
        confirmation="structured_receipt",
        fallback=OpenCLIFallbackManifest(
            before_dispatch="browser_agent",
            after_failure="none",
        ),
        file_inputs=("images",),
        file_outputs=(),
        sensitive_output=(),
    )


def _normalize_slug(value: Any, field: str) -> str:
    normalized = str(value or "").strip().lower()
    if not _SLUG_PATTERN.fullmatch(normalized):
        raise OpenCLIContractError(
            f"opencli_{field}_invalid",
            f"{field} must contain only lowercase letters, digits, and hyphens",
        )
    return normalized


def _load_frontmatter(content: str, relative_path: str) -> dict[str, Any]:
    if not content.startswith("---"):
        raise OpenCLIContractError(
            "opencli_contract_frontmatter_missing",
            f"Operation contract has no YAML frontmatter: {relative_path}",
        )
    parts = content.split("---", 2)
    if len(parts) != 3:
        raise OpenCLIContractError(
            "opencli_contract_frontmatter_invalid",
            f"Operation contract frontmatter is incomplete: {relative_path}",
        )
    try:
        metadata = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        raise OpenCLIContractError(
            "opencli_contract_frontmatter_invalid",
            f"Operation contract frontmatter is invalid: {relative_path}",
        ) from exc
    if not isinstance(metadata, dict):
        raise OpenCLIContractError(
            "opencli_contract_frontmatter_invalid",
            f"Operation contract frontmatter must be a mapping: {relative_path}",
        )
    return metadata


__all__ = [
    "OPENCLI_WEB_SKILL_NAME",
    "OpenCLICommandContract",
    "OpenCLIContractError",
    "OpenCLIOperationContract",
    "OpenCLITerminalContract",
    "load_operation_contract",
    "load_terminal_contract",
    "load_terminal_contract_by_path",
    "operation_relative_path",
    "parse_operation_relative_path",
]
