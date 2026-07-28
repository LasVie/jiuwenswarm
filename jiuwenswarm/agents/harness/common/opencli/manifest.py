# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Strict loader for the reviewed OpenCLI runtime manifest."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any

OPENCLI_RUNTIME_MANIFEST_FILENAME = "opencli-runtime.json"
_MAX_MANIFEST_BYTES = 16 * 1024 * 1024
_SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")

_TOP_LEVEL_KEYS = {
    "schema_version",
    "generator_version",
    "catalog",
    "sites",
}
_CATALOG_KEYS = {
    "opencli_version",
    "source_sha256",
    "canonical_sha256",
    "command_count",
}
_SITE_KEYS = {
    "display_name",
    "policy_sha256",
    "terminal",
    "operations",
}
_OPERATION_KEYS = {
    "purpose",
    "terminal",
    "policy_sha256",
    "commands",
}
_TERMINAL_KEYS = {"kind", "path", "sha256"}
_COMMAND_KEYS = {
    "executor",
    "execution_state",
    "semantic_effect",
    "risk",
    "auth",
    "transport",
    "strategy",
    "browser",
    "opencli_version",
    "access",
    "args",
    "confirmation",
    "fallback",
    "file_inputs",
    "file_outputs",
    "sensitive_output",
}
_FALLBACK_KEYS = {"before_dispatch", "after_failure"}
_ARGUMENT_KEYS = {
    "name",
    "type",
    "required",
    "help",
    "default",
    "positional",
    "valueRequired",
    "choices",
    "constraints",
}
_ARGUMENT_REQUIRED_KEYS = {"name", "type"}
_CONSTRAINT_KEYS = {
    "minimum",
    "maximum",
    "pattern",
    "max_length",
}

_TERMINAL_KINDS = {"site", "operation"}
_EXECUTION_STATES = {"enabled", "disabled", "quarantined", "custom"}
_SEMANTIC_EFFECTS = {
    "public_read",
    "private_account_read",
    "private_content_read",
    "auth_session_change",
    "local_write",
    "reversible_remote_write",
    "public_write",
    "message_send",
    "destructive_or_admin",
    "quota_consumption",
    "financial_write",
    "arbitrary_execution",
}
_RISKS = {"low", "medium", "high", "critical"}
_AUTH_MODES = {"none", "optional", "required", "interactive"}
_TRANSPORTS = {
    "public_http",
    "browser_dom",
    "browser_cookie",
    "browser_intercept",
    "local",
    "mixed",
}
_EXECUTORS = {
    "generic_manifest_read",
    "xiaohongshu_guarded_publish",
    "none",
}
_CONFIRMATIONS = {
    "none",
    "interactive_user",
    "structured_receipt",
    "unsupported",
}
_FALLBACK_ACTIONS = {"browser_agent", "none"}
_ACCESS_MODES = {"read", "write"}


class OpenCLIManifestError(ValueError):
    """The runtime manifest is absent, malformed, or internally inconsistent."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True, slots=True)
class OpenCLICatalogManifest:
    """Catalog fingerprint bound into one generated runtime manifest."""

    opencli_version: str
    source_sha256: str
    canonical_sha256: str
    command_count: int


@dataclass(frozen=True, slots=True)
class OpenCLIFallbackManifest:
    """Reviewed browser fallback policy around one OpenCLI dispatch."""

    before_dispatch: str
    after_failure: str


@dataclass(frozen=True, slots=True)
class OpenCLICommandManifest:
    """Reviewed immutable metadata for one manifest command."""

    name: str
    executor: str
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
class OpenCLITerminalManifest:
    """Exact generated Skill path and content fingerprint for an operation."""

    kind: str
    path: str
    sha256: str


@dataclass(frozen=True, slots=True)
class OpenCLIOperationManifest:
    """One logical operation registered in the runtime manifest."""

    name: str
    purpose: str
    terminal: OpenCLITerminalManifest
    policy_sha256: str
    commands: Mapping[str, OpenCLICommandManifest]


@dataclass(frozen=True, slots=True)
class OpenCLISiteManifest:
    """Reviewed runtime metadata for one website adapter."""

    slug: str
    display_name: str
    policy_sha256: str
    terminal: str
    operations: Mapping[str, OpenCLIOperationManifest]


@dataclass(frozen=True, slots=True)
class OpenCLIRuntimeManifest:
    """Validated runtime manifest plus its exact file fingerprint."""

    schema_version: int
    generator_version: str
    catalog: OpenCLICatalogManifest
    sites: Mapping[str, OpenCLISiteManifest]
    manifest_path: Path
    manifest_sha256: str
    terminals: Mapping[str, tuple[str, str]]

    def operation(
        self,
        site: str,
        operation: str,
    ) -> OpenCLIOperationManifest | None:
        site_manifest = self.sites.get(site)
        if site_manifest is None:
            return None
        return site_manifest.operations.get(operation)

    def operation_for_terminal(
        self,
        relative_path: str,
    ) -> tuple[str, OpenCLIOperationManifest] | None:
        key = self.terminals.get(relative_path)
        if key is None:
            return None
        site, operation = key
        operation_manifest = self.sites[site].operations[operation]
        return site, operation_manifest


class _DuplicateManifestKey(ValueError):
    pass


def load_runtime_manifest(
    skill_root: str | Path,
) -> OpenCLIRuntimeManifest:
    """Read and strictly validate ``opencli-runtime.json`` from a Skill root."""
    resolved_skill_root = Path(skill_root).expanduser().resolve()
    manifest_path = (resolved_skill_root / OPENCLI_RUNTIME_MANIFEST_FILENAME).resolve()
    if (
        manifest_path != resolved_skill_root
        and resolved_skill_root not in manifest_path.parents
    ):
        raise OpenCLIManifestError(
            "opencli_manifest_path_invalid",
            "OpenCLI runtime manifest resolved outside the installed Skill",
        )
    try:
        if manifest_path.stat().st_size > _MAX_MANIFEST_BYTES:
            raise OpenCLIManifestError(
                "opencli_manifest_too_large",
                "OpenCLI runtime manifest exceeds the supported size",
            )
        content_bytes = manifest_path.read_bytes()
        if len(content_bytes) > _MAX_MANIFEST_BYTES:
            raise OpenCLIManifestError(
                "opencli_manifest_too_large",
                "OpenCLI runtime manifest exceeds the supported size",
            )
    except FileNotFoundError as exc:
        raise OpenCLIManifestError(
            "opencli_manifest_missing",
            "OpenCLI runtime manifest is not installed",
        ) from exc
    except OpenCLIManifestError:
        raise
    except OSError as exc:
        raise OpenCLIManifestError(
            "opencli_manifest_unreadable",
            "OpenCLI runtime manifest cannot be read",
        ) from exc

    try:
        content = content_bytes.decode("utf-8")
        raw = json.loads(
            content,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_json_constant,
        )
    except (UnicodeError, json.JSONDecodeError, _DuplicateManifestKey) as exc:
        raise OpenCLIManifestError(
            "opencli_manifest_invalid",
            "OpenCLI runtime manifest is not strict UTF-8 JSON",
        ) from exc
    root = _require_mapping(raw, "runtime manifest")
    _require_exact_keys(root, _TOP_LEVEL_KEYS, "runtime manifest")
    if root["schema_version"] != 1 or isinstance(root["schema_version"], bool):
        raise OpenCLIManifestError(
            "opencli_manifest_schema_unsupported",
            "OpenCLI runtime manifest schema_version must be 1",
        )
    generator_version = _require_nonempty_string(
        root["generator_version"],
        "runtime manifest generator_version",
    )
    catalog = _parse_catalog(root["catalog"])
    sites = _parse_sites(root["sites"], catalog)
    command_count = sum(
        len(operation.commands)
        for site in sites.values()
        for operation in site.operations.values()
    )
    if command_count != catalog.command_count:
        raise OpenCLIManifestError(
            "opencli_manifest_command_count_mismatch",
            (
                "Runtime manifest command count does not match the catalog: "
                f"{command_count} != {catalog.command_count}"
            ),
        )

    terminals: dict[str, tuple[str, str]] = {}
    for site, site_manifest in sites.items():
        for operation, operation_manifest in site_manifest.operations.items():
            path = operation_manifest.terminal.path
            if path in terminals:
                raise OpenCLIManifestError(
                    "opencli_manifest_terminal_duplicate",
                    f"Runtime manifest registers terminal path twice: {path}",
                )
            terminals[path] = (site, operation)

    return OpenCLIRuntimeManifest(
        schema_version=1,
        generator_version=generator_version,
        catalog=catalog,
        sites=MappingProxyType(sites),
        manifest_path=manifest_path,
        manifest_sha256=hashlib.sha256(content_bytes).hexdigest(),
        terminals=MappingProxyType(terminals),
    )


def _parse_catalog(value: Any) -> OpenCLICatalogManifest:
    raw = _require_mapping(value, "runtime manifest catalog")
    _require_exact_keys(raw, _CATALOG_KEYS, "runtime manifest catalog")
    command_count = raw["command_count"]
    if (
        not isinstance(command_count, int)
        or isinstance(command_count, bool)
        or command_count < 0
    ):
        raise OpenCLIManifestError(
            "opencli_manifest_catalog_invalid",
            "Runtime manifest catalog command_count must be a non-negative integer",
        )
    return OpenCLICatalogManifest(
        opencli_version=_require_nonempty_string(
            raw["opencli_version"],
            "runtime manifest catalog opencli_version",
        ),
        source_sha256=_require_sha256(
            raw["source_sha256"],
            "runtime manifest catalog source_sha256",
        ),
        canonical_sha256=_require_sha256(
            raw["canonical_sha256"],
            "runtime manifest catalog canonical_sha256",
        ),
        command_count=command_count,
    )


def _parse_sites(
    value: Any,
    catalog: OpenCLICatalogManifest,
) -> dict[str, OpenCLISiteManifest]:
    raw_sites = _require_mapping(value, "runtime manifest sites")
    if not raw_sites:
        raise OpenCLIManifestError(
            "opencli_manifest_sites_missing",
            "Runtime manifest declares no sites",
        )
    sites: dict[str, OpenCLISiteManifest] = {}
    for raw_site, value in raw_sites.items():
        site = _require_slug(raw_site, "runtime manifest site")
        raw = _require_mapping(value, f"runtime manifest site '{site}'")
        _require_exact_keys(
            raw,
            _SITE_KEYS,
            f"runtime manifest site '{site}'",
        )
        terminal_kind = _require_enum(
            raw["terminal"],
            _TERMINAL_KINDS,
            f"runtime manifest site '{site}' terminal",
        )
        operations = _parse_operations(
            site,
            terminal_kind,
            raw["operations"],
            catalog,
        )
        if terminal_kind == "site" and len(operations) != 1:
            raise OpenCLIManifestError(
                "opencli_manifest_site_terminal_ambiguous",
                (
                    f"Site-terminal manifest '{site}' must register exactly "
                    "one logical operation"
                ),
            )
        sites[site] = OpenCLISiteManifest(
            slug=site,
            display_name=_require_nonempty_string(
                raw["display_name"],
                f"runtime manifest site '{site}' display_name",
            ),
            policy_sha256=_require_sha256(
                raw["policy_sha256"],
                f"runtime manifest site '{site}' policy_sha256",
            ),
            terminal=terminal_kind,
            operations=MappingProxyType(operations),
        )
    return sites


def _parse_operations(
    site: str,
    site_terminal_kind: str,
    value: Any,
    catalog: OpenCLICatalogManifest,
) -> dict[str, OpenCLIOperationManifest]:
    raw_operations = _require_mapping(
        value,
        f"runtime manifest site '{site}' operations",
    )
    if not raw_operations:
        raise OpenCLIManifestError(
            "opencli_manifest_operations_missing",
            f"Runtime manifest site '{site}' declares no operations",
        )
    operations: dict[str, OpenCLIOperationManifest] = {}
    seen_commands: set[str] = set()
    for raw_operation, value in raw_operations.items():
        operation = _require_slug(
            raw_operation,
            f"runtime manifest site '{site}' operation",
        )
        label = f"runtime manifest operation '{site}/{operation}'"
        raw = _require_mapping(value, label)
        _require_exact_keys(raw, _OPERATION_KEYS, label)
        terminal = _parse_terminal(
            site,
            operation,
            site_terminal_kind,
            raw["terminal"],
        )
        commands = _parse_commands(
            site,
            operation,
            raw["commands"],
            catalog,
        )
        duplicates = seen_commands.intersection(commands)
        if duplicates:
            duplicate = sorted(duplicates)[0]
            raise OpenCLIManifestError(
                "opencli_manifest_command_duplicate",
                (
                    f"Runtime manifest site '{site}' registers command "
                    f"'{duplicate}' in more than one operation"
                ),
            )
        seen_commands.update(commands)
        operations[operation] = OpenCLIOperationManifest(
            name=operation,
            purpose=_require_nonempty_string(
                raw["purpose"],
                f"{label} purpose",
            ),
            terminal=terminal,
            policy_sha256=_require_sha256(
                raw["policy_sha256"],
                f"{label} policy_sha256",
            ),
            commands=MappingProxyType(commands),
        )
    return operations


def _parse_terminal(
    site: str,
    operation: str,
    site_terminal_kind: str,
    value: Any,
) -> OpenCLITerminalManifest:
    label = f"runtime manifest terminal '{site}/{operation}'"
    raw = _require_mapping(value, label)
    _require_exact_keys(raw, _TERMINAL_KEYS, label)
    kind = _require_enum(raw["kind"], _TERMINAL_KINDS, f"{label} kind")
    if kind != site_terminal_kind:
        raise OpenCLIManifestError(
            "opencli_manifest_terminal_kind_mismatch",
            f"{label} kind does not match the site terminal mode",
        )
    path = _require_canonical_relative_path(raw["path"], f"{label} path")
    expected_path = (
        f"sites/{site}/SKILL.md"
        if kind == "site"
        else f"sites/{site}/operations/{operation}.md"
    )
    if path != expected_path:
        raise OpenCLIManifestError(
            "opencli_manifest_terminal_path_mismatch",
            (f"{label} terminal path must be '{expected_path}', not '{path}'"),
        )
    return OpenCLITerminalManifest(
        kind=kind,
        path=path,
        sha256=_require_sha256(raw["sha256"], f"{label} sha256"),
    )


def _parse_commands(
    site: str,
    operation: str,
    value: Any,
    catalog: OpenCLICatalogManifest,
) -> dict[str, OpenCLICommandManifest]:
    label = f"runtime manifest operation '{site}/{operation}' commands"
    raw_commands = _require_mapping(value, label)
    if not raw_commands:
        raise OpenCLIManifestError(
            "opencli_manifest_commands_missing",
            f"Runtime manifest operation '{site}/{operation}' has no commands",
        )
    commands: dict[str, OpenCLICommandManifest] = {}
    for raw_name, value in raw_commands.items():
        name = _require_slug(raw_name, f"{label} command")
        command_label = f"runtime manifest command '{site}/{operation}/{name}'"
        raw = _require_mapping(value, command_label)
        _require_exact_keys(raw, _COMMAND_KEYS, command_label)
        opencli_version = _require_nonempty_string(
            raw["opencli_version"],
            f"{command_label} opencli_version",
        )
        if opencli_version != catalog.opencli_version:
            raise OpenCLIManifestError(
                "opencli_manifest_version_mismatch",
                (f"{command_label} OpenCLI version does not match the catalog version"),
            )
        browser = raw["browser"]
        if not isinstance(browser, bool):
            raise OpenCLIManifestError(
                "opencli_manifest_command_invalid",
                f"{command_label} browser must be a boolean",
            )
        commands[name] = OpenCLICommandManifest(
            name=name,
            executor=_require_enum(
                raw["executor"],
                _EXECUTORS,
                f"{command_label} executor",
            ),
            execution_state=_require_enum(
                raw["execution_state"],
                _EXECUTION_STATES,
                f"{command_label} execution_state",
            ),
            semantic_effect=_require_enum(
                raw["semantic_effect"],
                _SEMANTIC_EFFECTS,
                f"{command_label} semantic_effect",
            ),
            risk=_require_enum(
                raw["risk"],
                _RISKS,
                f"{command_label} risk",
            ),
            auth=_require_enum(
                raw["auth"],
                _AUTH_MODES,
                f"{command_label} auth",
            ),
            transport=_require_enum(
                raw["transport"],
                _TRANSPORTS,
                f"{command_label} transport",
            ),
            strategy=_require_nonempty_string(
                raw["strategy"],
                f"{command_label} strategy",
            ),
            browser=browser,
            opencli_version=opencli_version,
            access=_require_enum(
                raw["access"],
                _ACCESS_MODES,
                f"{command_label} access",
            ),
            args=_parse_arguments(raw["args"], command_label),
            confirmation=_require_enum(
                raw["confirmation"],
                _CONFIRMATIONS,
                f"{command_label} confirmation",
            ),
            fallback=_parse_fallback(raw["fallback"], command_label),
            file_inputs=_parse_unique_strings(
                raw["file_inputs"],
                f"{command_label} file_inputs",
            ),
            file_outputs=_parse_unique_strings(
                raw["file_outputs"],
                f"{command_label} file_outputs",
            ),
            sensitive_output=_parse_unique_strings(
                raw["sensitive_output"],
                f"{command_label} sensitive_output",
            ),
        )
    return commands


def _parse_arguments(
    value: Any,
    command_label: str,
) -> tuple[Mapping[str, Any], ...]:
    if not isinstance(value, list):
        raise OpenCLIManifestError(
            "opencli_manifest_arguments_invalid",
            f"{command_label} args must be an ordered object list",
        )
    parsed: list[Mapping[str, Any]] = []
    seen_names: set[str] = set()
    for index, value in enumerate(value):
        label = f"{command_label} args[{index}]"
        raw = _require_mapping(value, label)
        unexpected = set(raw).difference(_ARGUMENT_KEYS)
        missing = _ARGUMENT_REQUIRED_KEYS.difference(raw)
        if unexpected or missing:
            _raise_key_error(label, unexpected, missing)
        name = _require_nonempty_string(raw["name"], f"{label} name")
        _require_nonempty_string(raw["type"], f"{label} type")
        if name in seen_names:
            raise OpenCLIManifestError(
                "opencli_manifest_argument_duplicate",
                f"{command_label} declares argument '{name}' twice",
            )
        seen_names.add(name)
        for field in ("required", "positional", "valueRequired"):
            if field in raw and not isinstance(raw[field], bool):
                raise OpenCLIManifestError(
                    "opencli_manifest_argument_invalid",
                    f"{label} {field} must be a boolean",
                )
        if "help" in raw and not isinstance(raw["help"], str):
            raise OpenCLIManifestError(
                "opencli_manifest_argument_invalid",
                f"{label} help must be a string",
            )
        if "choices" in raw and not isinstance(raw["choices"], list):
            raise OpenCLIManifestError(
                "opencli_manifest_argument_invalid",
                f"{label} choices must be a list",
            )
        if "constraints" in raw:
            _validate_constraints(raw["constraints"], label)
        parsed.append(_freeze_mapping(raw))
    return tuple(parsed)


def _validate_constraints(value: Any, label: str) -> None:
    raw = _require_mapping(value, f"{label} constraints")
    unexpected = set(raw).difference(_CONSTRAINT_KEYS)
    if unexpected:
        _raise_key_error(f"{label} constraints", unexpected, set())
    for field in ("minimum", "maximum"):
        if field in raw and (
            not isinstance(raw[field], (int, float)) or isinstance(raw[field], bool)
        ):
            raise OpenCLIManifestError(
                "opencli_manifest_argument_invalid",
                f"{label} constraints {field} must be numeric",
            )
    if "pattern" in raw and not isinstance(raw["pattern"], str):
        raise OpenCLIManifestError(
            "opencli_manifest_argument_invalid",
            f"{label} constraints pattern must be a string",
        )
    if "max_length" in raw and (
        not isinstance(raw["max_length"], int)
        or isinstance(raw["max_length"], bool)
        or raw["max_length"] < 0
    ):
        raise OpenCLIManifestError(
            "opencli_manifest_argument_invalid",
            f"{label} constraints max_length must be non-negative",
        )


def _parse_fallback(
    value: Any,
    command_label: str,
) -> OpenCLIFallbackManifest:
    label = f"{command_label} fallback"
    raw = _require_mapping(value, label)
    _require_exact_keys(raw, _FALLBACK_KEYS, label)
    return OpenCLIFallbackManifest(
        before_dispatch=_require_enum(
            raw["before_dispatch"],
            _FALLBACK_ACTIONS,
            f"{label} before_dispatch",
        ),
        after_failure=_require_enum(
            raw["after_failure"],
            _FALLBACK_ACTIONS,
            f"{label} after_failure",
        ),
    )


def _parse_unique_strings(value: Any, label: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise OpenCLIManifestError(
            "opencli_manifest_command_invalid",
            f"{label} must be a string list",
        )
    parsed: list[str] = []
    for item in value:
        parsed.append(_require_nonempty_string(item, label))
    if len(parsed) != len(set(parsed)):
        raise OpenCLIManifestError(
            "opencli_manifest_command_invalid",
            f"{label} must not contain duplicates",
        )
    return tuple(parsed)


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateManifestKey(key)
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise _DuplicateManifestKey(value)


def _require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise OpenCLIManifestError(
            "opencli_manifest_invalid",
            f"{label} must be an object",
        )
    return value


def _require_exact_keys(
    value: Mapping[str, Any],
    expected: set[str],
    label: str,
) -> None:
    unexpected = set(value).difference(expected)
    missing = expected.difference(value)
    if unexpected or missing:
        _raise_key_error(label, unexpected, missing)


def _raise_key_error(
    label: str,
    unexpected: set[str],
    missing: set[str],
) -> None:
    details: list[str] = []
    if unexpected:
        details.append(f"unexpected fields: {', '.join(sorted(unexpected))}")
    if missing:
        details.append(f"missing fields: {', '.join(sorted(missing))}")
    raise OpenCLIManifestError(
        "opencli_manifest_fields_invalid",
        f"{label} has {'; '.join(details)}",
    )


def _require_slug(value: Any, label: str) -> str:
    if not isinstance(value, str) or not _SLUG_PATTERN.fullmatch(value):
        raise OpenCLIManifestError(
            "opencli_manifest_slug_invalid",
            f"{label} must be a canonical lowercase slug",
        )
    return value


def _require_nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise OpenCLIManifestError(
            "opencli_manifest_value_invalid",
            f"{label} must be a non-empty string",
        )
    return value


def _require_sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or not _SHA256_PATTERN.fullmatch(value):
        raise OpenCLIManifestError(
            "opencli_manifest_hash_invalid",
            f"{label} must be a lowercase SHA-256 digest",
        )
    return value


def _require_enum(
    value: Any,
    allowed: set[str],
    label: str,
) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise OpenCLIManifestError(
            "opencli_manifest_value_invalid",
            f"{label} has an unsupported value",
        )
    return value


def _require_canonical_relative_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise OpenCLIManifestError(
            "opencli_manifest_path_invalid",
            f"{label} must be a relative path",
        )
    pure_path = PurePosixPath(value)
    if (
        "\\" in value
        or pure_path.is_absolute()
        or ".." in pure_path.parts
        or pure_path.as_posix() != value
    ):
        raise OpenCLIManifestError(
            "opencli_manifest_path_invalid",
            f"{label} must be a canonical POSIX relative path",
        )
    return value


def _freeze_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType({key: _freeze_json(item) for key, item in value.items()})


def _freeze_json(value: Any) -> Any:
    if isinstance(value, dict):
        return _freeze_mapping(value)
    if isinstance(value, list):
        return tuple(_freeze_json(item) for item in value)
    return value


__all__ = [
    "OPENCLI_RUNTIME_MANIFEST_FILENAME",
    "OpenCLICatalogManifest",
    "OpenCLICommandManifest",
    "OpenCLIFallbackManifest",
    "OpenCLIManifestError",
    "OpenCLIOperationManifest",
    "OpenCLIRuntimeManifest",
    "OpenCLISiteManifest",
    "OpenCLITerminalManifest",
    "load_runtime_manifest",
]
