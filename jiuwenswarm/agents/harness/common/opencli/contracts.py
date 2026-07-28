# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Load machine-readable execution metadata from OpenCLI operation contracts."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

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
    """One command authorized by an installed operation contract."""

    site: str
    operation: str
    command: str
    executor: str
    skill_root: Path
    operation_path: Path
    operation_relative_path: str
    operation_sha256: str


@dataclass(frozen=True, slots=True)
class OpenCLIOperationContract:
    """Validated machine-readable metadata for one operation document."""

    site: str
    operation: str
    commands: dict[str, str]
    skill_root: Path
    operation_path: Path
    operation_relative_path: str
    operation_sha256: str

    def command_contract(self, command: str) -> OpenCLICommandContract:
        normalized = _normalize_slug(command, "command")
        executor = self.commands.get(normalized)
        if executor is None:
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
        )


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
    if candidate != installed_skill_root and installed_skill_root not in candidate.parents:
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

    return OpenCLIOperationContract(
        site=normalized_site,
        operation=normalized_operation,
        commands=commands,
        skill_root=installed_skill_root,
        operation_path=candidate,
        operation_relative_path=relative_path,
        operation_sha256=hashlib.sha256(content_bytes).hexdigest(),
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
    "load_operation_contract",
    "operation_relative_path",
    "parse_operation_relative_path",
]
