#!/usr/bin/env python3
"""Generate the managed OpenCLI Web Skill tree from a frozen catalog.

The frozen OpenCLI manifest defines the commands that OpenCLI exposes.  The
repository-owned site policies add semantic effects, risk, fallback rules, and
progressive-disclosure boundaries without maintaining a separate execution
allowlist.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Sequence

import yaml

try:
    import jsonschema
except ImportError:  # pragma: no cover - exercised by CLI error handling
    jsonschema = None


OPENCLI_VERSION = "1.8.6"
GENERATOR_VERSION = "2"
CATALOG_COMMAND_COUNT = 1331
CATALOG_SITE_COUNT = 176
GENERATED_SITE_COUNT = 164
GENERATED_COMMAND_COUNT = 1154
EXCLUDED_ADAPTERS = frozenset(
    {
        "antigravity",
        "chatgpt-app",
        "chatwise",
        "codex",
        "cursor",
        "discord-app",
        "doubao-app",
        "qoder",
        "trae-cn",
        "trae-solo",
        "web",
    }
)
_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_PLACEHOLDER_RE = re.compile(r'^[^\s<>"|]+$')
_INDEX_RE = re.compile(
    r"(?ms)^## Supported websites\s*.*\Z"
)
_MANIFEST_NAME = "generated-manifest.json"
_LEGACY_RUNTIME_NAME = "opencli-runtime.json"


class GenerationError(ValueError):
    """The catalog, ownership, policy, or generated output is inconsistent."""


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
        + "\n"
    ).encode("utf-8")


def _require_slug(value: Any, field: str) -> str:
    normalized = str(value or "").strip().lower()
    if not _SLUG_RE.fullmatch(normalized):
        raise GenerationError(f"{field} is not a canonical slug: {value!r}")
    return normalized


def _require_mapping(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise GenerationError(f"{field} must be an object")
    return value


def _require_string_list(value: Any, field: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise GenerationError(f"{field} must be a list of non-empty strings")
    if len(set(value)) != len(value):
        raise GenerationError(f"{field} contains duplicates")
    return tuple(value)


@dataclass(frozen=True, slots=True)
class CatalogCommand:
    """One exact command from the frozen upstream manifest."""

    raw: dict[str, Any]

    @property
    def site(self) -> str:
        return str(self.raw["site"])

    @property
    def name(self) -> str:
        return str(self.raw["name"])

    @property
    def description(self) -> str:
        return str(self.raw["description"])

    @property
    def access(self) -> str:
        return str(self.raw["access"])

    @property
    def strategy(self) -> str:
        return str(self.raw["strategy"])

    @property
    def browser(self) -> bool:
        return bool(self.raw["browser"])

    @property
    def args(self) -> tuple[dict[str, Any], ...]:
        return tuple(dict(item) for item in self.raw["args"])


@dataclass(frozen=True, slots=True)
class CatalogSnapshot:
    """Validated wrapper around the frozen raw OpenCLI manifest."""

    opencli_version: str
    source_sha256: str
    canonical_sha256: str
    raw_commands: list[dict[str, Any]]
    commands: tuple[CatalogCommand, ...]

    def site_commands(self, site: str) -> tuple[CatalogCommand, ...]:
        return tuple(command for command in self.commands if command.site == site)


@dataclass(frozen=True, slots=True)
class Ownership:
    """Unique site ownership and fixed exclusions."""

    owners: dict[str, tuple[str, ...]]
    excluded: tuple[str, ...]
    completed: tuple[str, ...]

    def owner_for(self, site: str) -> str:
        for owner, sites in self.owners.items():
            if site in sites:
                return owner
        if site in self.completed:
            return "coordinator"
        raise GenerationError(f"site has no owner: {site}")


@dataclass(frozen=True, slots=True)
class CommandPolicy:
    """Capability metadata applied to one catalog command."""

    catalog: CatalogCommand
    operation: str
    semantic_effect: str
    risk: str
    auth: str
    transport: str
    fallback_before: str
    fallback_after: str
    file_inputs: tuple[str, ...]
    file_outputs: tuple[str, ...]
    sensitive_output: tuple[str, ...]
    notes: str
    args: tuple[dict[str, Any], ...]

    @property
    def name(self) -> str:
        return self.catalog.name


@dataclass(frozen=True, slots=True)
class OperationPolicy:
    """One logical terminal contract group within a site."""

    slug: str
    purpose: str
    commands: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SitePolicy:
    """Complete policy and progressive-disclosure layout for one site."""

    slug: str
    display_name: str
    domains: tuple[str, ...]
    aliases: tuple[str, ...]
    terminal: str
    operations: dict[str, OperationPolicy]
    commands: dict[str, CommandPolicy]
    policy_sha256: str

    def command(self, name: str) -> CommandPolicy:
        try:
            return self.commands[name]
        except KeyError as exc:
            raise GenerationError(
                f"{self.slug} policy has no command {name!r}"
            ) from exc


@dataclass(frozen=True, slots=True)
class GenerationModel:
    """Fully joined and validated generation input."""

    catalog: CatalogSnapshot
    ownership: Ownership
    sites: dict[str, SitePolicy]
    policy_sha256: str


@dataclass(frozen=True, slots=True)
class GenerationResult:
    """Summary of one deterministic generation."""

    site_count: int
    command_count: int
    file_count: int
    manifest_sha256: str


def load_catalog(path: str | Path) -> CatalogSnapshot:
    """Load and strictly validate the frozen raw OpenCLI catalog wrapper."""
    source = Path(path)
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise GenerationError(f"catalog cannot be read: {source}") from exc
    root = _require_mapping(payload, "catalog")
    allowed_root = {
        "schema_version",
        "opencli_version",
        "source",
        "source_sha256",
        "canonical_sha256",
        "commands",
    }
    unknown = set(root) - allowed_root
    if unknown:
        raise GenerationError(f"catalog has unknown fields: {sorted(unknown)}")
    if root.get("schema_version") != 1:
        raise GenerationError("catalog schema_version must be 1")
    version = str(root.get("opencli_version") or "")
    if version != OPENCLI_VERSION:
        raise GenerationError(
            f"catalog OpenCLI version is {version!r}, expected {OPENCLI_VERSION!r}"
        )
    source_sha256 = str(root.get("source_sha256") or "").lower()
    canonical_sha256 = str(root.get("canonical_sha256") or "").lower()
    if not _SHA256_RE.fullmatch(source_sha256):
        raise GenerationError("catalog source_sha256 is invalid")
    if not _SHA256_RE.fullmatch(canonical_sha256):
        raise GenerationError("catalog canonical_sha256 is invalid")
    raw_commands = root.get("commands")
    if not isinstance(raw_commands, list):
        raise GenerationError("catalog commands must be a list")
    computed_canonical = _sha256(_canonical_json(raw_commands))
    if computed_canonical != canonical_sha256:
        raise GenerationError("catalog canonical_sha256 does not match commands")

    required_fields = {
        "site",
        "name",
        "description",
        "access",
        "strategy",
        "browser",
        "args",
        "type",
        "modulePath",
        "sourceFile",
    }
    commands: list[CatalogCommand] = []
    identities: set[tuple[str, str]] = set()
    for index, raw_command in enumerate(raw_commands):
        command = _require_mapping(raw_command, f"catalog.commands[{index}]")
        missing = required_fields - set(command)
        if missing:
            raise GenerationError(
                f"catalog command {index} misses fields: {sorted(missing)}"
            )
        site = _require_slug(command.get("site"), f"catalog command {index} site")
        name = _require_slug(command.get("name"), f"catalog command {index} name")
        identity = (site, name)
        if identity in identities:
            raise GenerationError(f"duplicate catalog command: {site}/{name}")
        identities.add(identity)
        if command.get("access") not in {"read", "write"}:
            raise GenerationError(f"unsupported access for {site}/{name}")
        if command.get("strategy") not in {
            "cookie",
            "public",
            "ui",
            "local",
            "intercept",
        }:
            raise GenerationError(f"unsupported strategy for {site}/{name}")
        if not isinstance(command.get("browser"), bool):
            raise GenerationError(f"browser must be bool for {site}/{name}")
        if not isinstance(command.get("args"), list):
            raise GenerationError(f"args must be a list for {site}/{name}")
        commands.append(CatalogCommand(dict(command)))

    if len(commands) != CATALOG_COMMAND_COUNT:
        raise GenerationError(
            f"catalog has {len(commands)} commands, expected {CATALOG_COMMAND_COUNT}"
        )
    site_count = len({command.site for command in commands})
    if site_count != CATALOG_SITE_COUNT:
        raise GenerationError(
            f"catalog has {site_count} sites, expected {CATALOG_SITE_COUNT}"
        )
    if commands != sorted(commands, key=lambda item: (item.site, item.name)):
        raise GenerationError("catalog commands must be sorted by site/name")

    return CatalogSnapshot(
        opencli_version=version,
        source_sha256=source_sha256,
        canonical_sha256=canonical_sha256,
        raw_commands=[dict(command) for command in raw_commands],
        commands=tuple(commands),
    )


def load_ownership(path: str | Path) -> Ownership:
    """Load unique site ownership and exclusions."""
    source = Path(path)
    try:
        payload = yaml.safe_load(source.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise GenerationError(f"ownership cannot be read: {source}") from exc
    root = _require_mapping(payload, "ownership")
    if set(root) != {
        "schema_version",
        "catalog_version",
        "excluded",
        "completed",
        "owners",
    }:
        raise GenerationError("ownership fields are incomplete or unknown")
    if root["schema_version"] != 1:
        raise GenerationError("ownership schema_version must be 1")
    if root["catalog_version"] != f"opencli-{OPENCLI_VERSION}":
        raise GenerationError("ownership catalog_version is unsupported")
    excluded = tuple(
        _require_slug(item, "excluded site")
        for item in _require_string_list(root["excluded"], "ownership.excluded")
    )
    completed = tuple(
        _require_slug(item, "completed site")
        for item in _require_string_list(root["completed"], "ownership.completed")
    )
    raw_owners = _require_mapping(root["owners"], "ownership.owners")
    owners: dict[str, tuple[str, ...]] = {}
    assigned: list[str] = []
    for owner, raw_sites in raw_owners.items():
        if not isinstance(owner, str) or not owner.strip():
            raise GenerationError("ownership owner name must be non-empty")
        sites = tuple(
            _require_slug(site, f"owner {owner} site")
            for site in _require_string_list(raw_sites, f"ownership.owners.{owner}")
        )
        if sites != tuple(sorted(sites)):
            raise GenerationError(f"owner {owner} sites must be sorted")
        owners[owner] = sites
        assigned.extend(sites)
    if len(assigned) != len(set(assigned)):
        raise GenerationError("ownership assigns at least one site more than once")
    if set(excluded) != EXCLUDED_ADAPTERS:
        raise GenerationError("ownership exclusions do not match fixed boundary")
    if completed != ("xiaohongshu",):
        raise GenerationError("ownership completed set must contain xiaohongshu")
    return Ownership(
        owners=owners,
        excluded=excluded,
        completed=completed,
    )


def load_policies(path: str | Path) -> dict[str, dict[str, Any]]:
    """Load and schema-validate all repository-owned site policy YAML files."""
    root = Path(path)
    schema_path = root.parent / "schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise GenerationError(f"policy schema cannot be read: {schema_path}") from exc
    if jsonschema is None:
        raise GenerationError(
            "jsonschema is required to validate OpenCLI site policies"
        )
    policies: dict[str, dict[str, Any]] = {}
    for policy_path in sorted(root.glob("*.yaml")):
        try:
            raw = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            raise GenerationError(f"policy cannot be read: {policy_path}") from exc
        try:
            jsonschema.validate(raw, schema)
        except jsonschema.ValidationError as exc:
            location = ".".join(str(part) for part in exc.absolute_path)
            raise GenerationError(
                f"invalid policy {policy_path.name} at {location or '<root>'}: "
                f"{exc.message}"
            ) from exc
        policy = _require_mapping(raw, f"policy {policy_path.name}")
        site = _require_slug(policy.get("site"), f"policy {policy_path.name} site")
        if policy_path.stem != site:
            raise GenerationError(
                f"policy filename does not match site: {policy_path.name}"
            )
        if site in policies:
            raise GenerationError(f"duplicate policy for {site}")
        policies[site] = policy
    return policies


def _apply_arg_overrides(
    catalog_args: Sequence[Mapping[str, Any]],
    raw_overrides: Any,
    *,
    identity: str,
) -> tuple[dict[str, Any], ...]:
    if raw_overrides is None:
        return tuple(dict(arg) for arg in catalog_args)
    overrides = _require_mapping(raw_overrides, f"{identity}.arg_overrides")
    known_names = {str(arg.get("name")) for arg in catalog_args}
    unknown = set(overrides) - known_names
    if unknown:
        raise GenerationError(
            f"{identity} has arg overrides for unknown args: {sorted(unknown)}"
        )
    result: list[dict[str, Any]] = []
    for raw_arg in catalog_args:
        arg = dict(raw_arg)
        arg_override = overrides.get(str(arg.get("name")))
        if arg_override is not None:
            fields = _require_mapping(
                arg_override, f"{identity}.arg_overrides.{arg.get('name')}"
            )
            constraint_names = {"minimum", "maximum", "pattern", "max_length"}
            allowed = constraint_names | {"placeholder"}
            if set(fields) - allowed:
                raise GenerationError(
                    f"{identity} has unknown argument override fields"
                )
            if "placeholder" in fields:
                placeholder = fields["placeholder"]
                if not isinstance(placeholder, str) or not _PLACEHOLDER_RE.fullmatch(
                    placeholder.strip()
                ):
                    raise GenerationError(
                        f"{identity} argument placeholder must be one non-empty token"
                    )
                arg["placeholder"] = placeholder.strip()
            constraints = {
                key: value for key, value in fields.items() if key in constraint_names
            }
            if constraints:
                arg["constraints"] = constraints
        result.append(arg)
    return tuple(result)


def build_generation_model(
    catalog: CatalogSnapshot,
    ownership: Ownership,
    raw_policies: Mapping[str, Mapping[str, Any]],
) -> GenerationModel:
    """Join catalog and policies and enforce every global safety invariant."""
    expected_sites = {
        command.site
        for command in catalog.commands
        if command.site not in EXCLUDED_ADAPTERS
    }
    if len(expected_sites) != GENERATED_SITE_COUNT + 1:
        raise GenerationError("catalog website boundary count drifted")
    if set(raw_policies) != expected_sites:
        missing = sorted(expected_sites - set(raw_policies))
        extra = sorted(set(raw_policies) - expected_sites)
        raise GenerationError(
            f"policy coverage mismatch; missing={missing}, extra={extra}"
        )
    assigned = {site for sites in ownership.owners.values() for site in sites}
    expected_assigned = expected_sites - set(ownership.completed)
    if assigned != expected_assigned:
        raise GenerationError("ownership does not exactly cover pending sites")

    sites: dict[str, SitePolicy] = {}
    policy_digests: dict[str, str] = {}
    for site_slug in sorted(expected_sites):
        raw_policy = dict(raw_policies[site_slug])
        if raw_policy["catalog_version"] != f"opencli-{OPENCLI_VERSION}":
            raise GenerationError(f"{site_slug} policy catalog version drifted")
        catalog_commands = {
            command.name: command for command in catalog.site_commands(site_slug)
        }
        raw_operations = _require_mapping(
            raw_policy["operations"], f"{site_slug}.operations"
        )
        operations: dict[str, OperationPolicy] = {}
        covered: list[str] = []
        for raw_operation, raw_spec in sorted(raw_operations.items()):
            operation = _require_slug(raw_operation, f"{site_slug} operation")
            spec = _require_mapping(raw_spec, f"{site_slug}.operations.{operation}")
            commands = tuple(
                _require_slug(item, f"{site_slug}.{operation} command")
                for item in _require_string_list(
                    spec["commands"],
                    f"{site_slug}.operations.{operation}.commands",
                )
            )
            covered.extend(commands)
            operations[operation] = OperationPolicy(
                slug=operation,
                purpose=str(spec["purpose"]).strip(),
                commands=commands,
            )
        if len(covered) != len(set(covered)):
            raise GenerationError(f"{site_slug} covers a command more than once")
        if set(covered) != set(catalog_commands):
            missing = sorted(set(catalog_commands) - set(covered))
            extra = sorted(set(covered) - set(catalog_commands))
            raise GenerationError(
                f"{site_slug} operation coverage mismatch; "
                f"missing={missing}, extra={extra}"
            )

        raw_commands = _require_mapping(raw_policy["commands"], f"{site_slug}.commands")
        if set(raw_commands) != set(catalog_commands):
            raise GenerationError(
                f"{site_slug} command policy keys do not match catalog"
            )
        command_policies: dict[str, CommandPolicy] = {}
        for command_name in sorted(catalog_commands):
            raw_command_policy = _require_mapping(
                raw_commands[command_name],
                f"{site_slug}.commands.{command_name}",
            )
            operation = _require_slug(
                raw_command_policy["operation"],
                f"{site_slug}/{command_name} operation",
            )
            if operation not in operations:
                raise GenerationError(
                    f"{site_slug}/{command_name} references missing operation"
                )
            if command_name not in operations[operation].commands:
                raise GenerationError(
                    f"{site_slug}/{command_name} operation mapping disagrees"
                )
            catalog_command = catalog_commands[command_name]
            command_policy = CommandPolicy(
                catalog=catalog_command,
                operation=operation,
                semantic_effect=str(raw_command_policy["semantic_effect"]),
                risk=str(raw_command_policy["risk"]),
                auth=str(raw_command_policy["auth"]),
                transport=str(raw_command_policy["transport"]),
                fallback_before=str(raw_command_policy["fallback_before"]),
                fallback_after=str(raw_command_policy["fallback_after"]),
                file_inputs=_require_string_list(
                    raw_command_policy["file_inputs"],
                    f"{site_slug}/{command_name}.file_inputs",
                ),
                file_outputs=_require_string_list(
                    raw_command_policy["file_outputs"],
                    f"{site_slug}/{command_name}.file_outputs",
                ),
                sensitive_output=_require_string_list(
                    raw_command_policy["sensitive_output"],
                    f"{site_slug}/{command_name}.sensitive_output",
                ),
                notes=str(raw_command_policy.get("notes") or "").strip(),
                args=_apply_arg_overrides(
                    catalog_command.args,
                    raw_command_policy.get("arg_overrides"),
                    identity=f"{site_slug}/{command_name}",
                ),
            )
            _validate_command_policy(command_policy)
            command_policies[command_name] = command_policy

        terminal = str(raw_policy["terminal"])
        if terminal == "site":
            _validate_site_terminal(
                site_slug,
                operations,
                command_policies,
            )
        policy_sha256 = _sha256(_canonical_json(raw_policy))
        policy_digests[site_slug] = policy_sha256
        sites[site_slug] = SitePolicy(
            slug=site_slug,
            display_name=str(raw_policy["display_name"]).strip(),
            domains=tuple(str(item) for item in raw_policy["domains"]),
            aliases=tuple(str(item) for item in raw_policy["aliases"]),
            terminal=terminal,
            operations=operations,
            commands=command_policies,
            policy_sha256=policy_sha256,
        )

    pending_command_count = sum(
        len(site.commands) for slug, site in sites.items() if slug != "xiaohongshu"
    )
    if pending_command_count != GENERATED_COMMAND_COUNT:
        raise GenerationError("pending generated command count drifted")
    return GenerationModel(
        catalog=catalog,
        ownership=ownership,
        sites=sites,
        policy_sha256=_sha256(_canonical_json(policy_digests)),
    )


def _validate_command_policy(policy: CommandPolicy) -> None:
    identity = f"{policy.catalog.site}/{policy.name}"
    if policy.semantic_effect != "public_read" and policy.fallback_after != "none":
        raise GenerationError(
            f"{identity} mutating/private command cannot auto-fallback after failure"
        )


def _validate_site_terminal(
    site: str,
    operations: Mapping[str, OperationPolicy],
    commands: Mapping[str, CommandPolicy],
) -> None:
    if len(commands) > 3 or len(operations) != 1:
        raise GenerationError(
            f"{site} site terminal requires <=3 commands in one operation"
        )
    for command in commands.values():
        if (
            command.semantic_effect != "public_read"
            or command.risk != "low"
            or command.auth != "none"
            or command.catalog.access != "read"
            or command.catalog.strategy != "public"
            or command.catalog.browser
            or command.file_inputs
            or command.file_outputs
        ):
            raise GenerationError(
                f"{site} does not satisfy the low-risk site-terminal contract"
            )


def _argument_placeholder(argument: Mapping[str, Any]) -> str:
    """Render one human-readable CLI value placeholder."""
    name = str(argument["name"])
    explicit_placeholder = str(argument.get("placeholder") or "").strip()
    choices = argument.get("choices") or []
    type_name = str(argument.get("type", "")).lower()
    if explicit_placeholder:
        label = explicit_placeholder
    elif choices:
        label = "|".join(str(choice) for choice in choices)
    elif type_name in {"bool", "boolean"}:
        label = "true|false"
    else:
        label = name
    placeholder = f"<{label}>"
    if type_name in {"int", "integer", "float", "number", "bool", "boolean"}:
        return placeholder
    return f'"{placeholder}"'


def _command_invocation(site: SitePolicy, command: CommandPolicy) -> str:
    """Render the exact OpenCLI CLI shape for one command."""
    parts = ["opencli", site.slug, command.name]
    for argument in command.args:
        name = str(argument["name"])
        value = _argument_placeholder(argument)
        item = value if argument.get("positional") else f"--{name} {value}"
        if not argument.get("required"):
            item = f"[{item}]"
        parts.append(item)
    parts.extend(["-f", "json"])
    return " ".join(parts)


def _argument_summary(command: CommandPolicy) -> str:
    if not command.args:
        return "none"
    summaries: list[str] = []
    for arg in command.args:
        name = str(arg.get("name"))
        type_name = str(arg.get("type"))
        required = "required" if arg.get("required") else "optional"
        positional = ", positional" if arg.get("positional") else ""
        default = f", default={arg['default']!r}" if "default" in arg else ""
        choices = (
            f", choices={','.join(str(item) for item in arg['choices'])}"
            if arg.get("choices")
            else ""
        )
        constraints = arg.get("constraints") or {}
        constraint_text = (
            ", " + ",".join(f"{key}={value}" for key, value in constraints.items())
            if constraints
            else ""
        )
        summaries.append(
            f"`{name}` ({type_name}, {required}{positional}{default}{choices}"
            f"{constraint_text})"
        )
    return "; ".join(summaries)


def _command_policy_summary(command: CommandPolicy) -> str:
    return (
        f"auth={command.auth}; transport={command.transport}; "
        f"fallback_before={command.fallback_before}; "
        f"fallback_after={command.fallback_after}"
    )


def _render_command_table(
    site: SitePolicy,
    commands: Iterable[CommandPolicy],
) -> str:
    lines = [
        "| Command | Effect / risk | Exact usage | Arguments | Runtime |",
        "|---|---|---|---|---|",
    ]
    for command in commands:
        invocation = f"`{_command_invocation(site, command)}`"
        description = command.catalog.description.replace("|", "\\|").replace("\n", " ")
        invocation = invocation.replace("|", "\\|")
        argument_summary = _argument_summary(command).replace("|", "\\|")
        policy_summary = _command_policy_summary(command).replace("|", "\\|")
        lines.append(
            f"| `{command.name}` | `{command.semantic_effect}` / `{command.risk}` | "
            f"{invocation}<br>{description} | "
            f"{argument_summary} | {policy_summary} |"
        )
    return "\n".join(lines)


def _render_operation_constraints(
    site: SitePolicy,
    operation: OperationPolicy,
) -> str:
    lines: list[str] = []
    for name in operation.commands:
        command = site.commands[name]
        details: list[str] = []
        if command.notes:
            details.append(command.notes)
        if command.file_inputs:
            details.append(f"file inputs: {', '.join(command.file_inputs)}")
        if command.file_outputs:
            details.append(f"file outputs: {', '.join(command.file_outputs)}")
        if command.sensitive_output:
            details.append(
                f"sensitive output: {', '.join(command.sensitive_output)}"
            )
        if details:
            lines.append(f"- `{name}`: {'; '.join(details)}")
    if not lines:
        return ""
    return "## Operation-specific constraints\n\n" + "\n".join(lines)


def _render_site_index(site: SitePolicy) -> bytes:
    lines = [
        f"# {site.display_name}",
        "",
        f"- Site slug: `{site.slug}`",
        "- Domains: "
        + (", ".join(f"`{domain}`" for domain in site.domains) or "none"),
        "- Aliases: "
        + (", ".join(f"`{alias}`" for alias in site.aliases) or "none"),
        "",
        "## Operations",
        "",
        "| Operation | Purpose | Commands | Terminal contract |",
        "|---|---|---|---|",
    ]
    for operation in site.operations.values():
        command_list = ", ".join(f"`{name}`" for name in operation.commands)
        path = (
            f"sites/{site.slug}/index.md"
            if site.terminal == "site"
            else f"sites/{site.slug}/operations/{operation.slug}.md"
        )
        lines.append(
            f"| `{operation.slug}` | {operation.purpose} | {command_list} | "
            f"`{path}` |"
        )
    if site.terminal == "site":
        operation = next(iter(site.operations.values()))
        lines.extend(
            [
                "",
                "## Commands",
                "",
                _render_command_table(
                    site,
                    (site.commands[name] for name in operation.commands),
                ),
            ]
        )
        constraints = _render_operation_constraints(site, operation)
        if constraints:
            lines.extend(["", constraints])
    return ("\n".join(lines).rstrip() + "\n").encode("utf-8")


def _render_operation(site: SitePolicy, operation: OperationPolicy) -> bytes:
    lines = [
        f"# {site.display_name}: {operation.slug}",
        "",
        operation.purpose,
        "",
        _render_command_table(
            site,
            (site.commands[name] for name in operation.commands),
        ),
    ]
    constraints = _render_operation_constraints(site, operation)
    if constraints:
        lines.extend(["", constraints])
    return ("\n".join(lines).rstrip() + "\n").encode("utf-8")


def _render_root_index(model: GenerationModel, root_skill: bytes) -> bytes:
    try:
        text = root_skill.decode("utf-8")
    except UnicodeError as exc:
        raise GenerationError("root SKILL.md is not UTF-8") from exc
    lines = [
        "## Supported websites",
        "",
        "| Website | Aliases | Domains | Site module |",
        "|---|---|---|---|",
    ]
    for site in model.sites.values():
        aliases = ", ".join(site.aliases) or "none"
        domains = ", ".join(site.domains) or "none"
        lines.append(
            f"| {site.display_name} | {aliases} | {domains} | "
            f"`sites/{site.slug}/index.md` |"
        )
    replacement = "\n".join(lines) + "\n"
    if not _INDEX_RE.search(text):
        raise GenerationError(
            "root SKILL.md lacks replaceable Supported websites section"
        )
    return _INDEX_RE.sub(replacement, text, count=1).encode("utf-8")


def _safe_relative_path(value: str) -> PurePosixPath:
    if "\\" in value:
        raise GenerationError(f"generated path uses a backslash: {value}")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or not path.parts
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise GenerationError(f"generated path is unsafe: {value}")
    return path


def _load_manual_files(manual_root: Path) -> dict[str, bytes]:
    if not (manual_root / "SKILL.md").is_file():
        raise GenerationError(f"manual OpenCLI Skill root is invalid: {manual_root}")
    files: dict[str, bytes] = {}
    for path in sorted(manual_root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(manual_root).as_posix()
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if relative in {_MANIFEST_NAME, _LEGACY_RUNTIME_NAME}:
            continue
        if relative == "sites/xiaohongshu/SKILL.md":
            continue
        if relative.startswith("sites/") and not relative.startswith(
            "sites/xiaohongshu/"
        ):
            continue
        files[relative] = path.read_bytes()
    return files


def _write_generated_files(
    output_root: Path,
    files: Mapping[str, bytes],
) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    old_owned: set[str] = set()
    old_manifest = output_root / _MANIFEST_NAME
    if old_manifest.is_file():
        try:
            old_payload = json.loads(old_manifest.read_text(encoding="utf-8"))
            raw_owned = old_payload.get("files", {})
            if isinstance(raw_owned, dict):
                old_owned = {str(_safe_relative_path(str(item))) for item in raw_owned}
        except (OSError, UnicodeError, json.JSONDecodeError, GenerationError):
            old_owned = set()

    for relative in sorted(old_owned - set(files)):
        target = (output_root / Path(*PurePosixPath(relative).parts)).resolve()
        resolved_root = output_root.resolve()
        if resolved_root not in target.parents:
            raise GenerationError(f"stale generated path escapes root: {relative}")
        if target.is_file() or target.is_symlink():
            target.unlink()

    for relative, content in sorted(files.items()):
        pure_path = _safe_relative_path(relative)
        destination = output_root / Path(*pure_path.parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.is_file() and destination.read_bytes() == content:
            continue
        destination.write_bytes(content)

    for directory in sorted(
        (path for path in output_root.rglob("*") if path.is_dir()),
        key=lambda item: len(item.parts),
        reverse=True,
    ):
        try:
            directory.rmdir()
        except OSError:
            pass


def generate(
    model: GenerationModel,
    *,
    output_root: str | Path,
    manual_skill_root: str | Path,
    selected_sites: Sequence[str] | None = None,
) -> GenerationResult:
    """Generate a deterministic full tree or a scoped set of site files."""
    output = Path(output_root)
    manual_root = Path(manual_skill_root)
    files = _load_manual_files(manual_root)
    selected = (
        set(model.sites)
        if selected_sites is None
        else {_require_slug(site, "selected site") for site in selected_sites}
    )
    unknown = selected - set(model.sites)
    if unknown:
        raise GenerationError(f"unknown selected sites: {sorted(unknown)}")
    if selected_sites is not None:
        # Scoped generation is intentionally site-owned only. Shared root and
        # manifests are refreshed by the coordinator's subsequent full run.
        files = {
            relative: content
            for relative, content in files.items()
            if relative.startswith("sites/xiaohongshu/")
        }
    for site_slug in sorted(selected):
        site = model.sites[site_slug]
        files[f"sites/{site_slug}/index.md"] = _render_site_index(site)
        if site.terminal == "operation":
            for operation in site.operations.values():
                relative = (
                    f"sites/{site_slug}/operations/{operation.slug}.md"
                )
                files[relative] = _render_operation(site, operation)

    if selected_sites is not None:
        scoped_files = {
            relative: content
            for relative, content in files.items()
            if any(relative.startswith(f"sites/{site}/") for site in selected)
        }
        _write_generated_files(output, scoped_files)
        return GenerationResult(
            site_count=len(selected),
            command_count=sum(len(model.sites[site].commands) for site in selected),
            file_count=len(scoped_files),
            manifest_sha256="",
        )

    files["SKILL.md"] = _render_root_index(model, files["SKILL.md"])
    owned_hashes = {
        relative: _sha256(content) for relative, content in sorted(files.items())
    }
    manifest = {
        "schema_version": 1,
        "generator_version": GENERATOR_VERSION,
        "opencli_version": model.catalog.opencli_version,
        "catalog_sha256": model.catalog.source_sha256,
        "policy_sha256": model.policy_sha256,
        "site_count": len(model.sites),
        "command_count": sum(len(site.commands) for site in model.sites.values()),
        "file_count": len(owned_hashes),
        "files": owned_hashes,
    }
    manifest_bytes = _json_bytes(manifest)
    files[_MANIFEST_NAME] = manifest_bytes
    _write_generated_files(output, files)
    return GenerationResult(
        site_count=len(model.sites),
        command_count=sum(len(site.commands) for site in model.sites.values()),
        file_count=len(files),
        manifest_sha256=_sha256(manifest_bytes),
    )


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    repo_root = _default_repo_root()
    input_root = Path(__file__).resolve().parent
    default_skill = (
        repo_root
        / "jiuwenswarm"
        / "resources"
        / "agent"
        / "workspace"
        / "skills"
        / "opencli-web"
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--catalog",
        type=Path,
        default=input_root / "catalog" / f"opencli-{OPENCLI_VERSION}.json",
    )
    parser.add_argument(
        "--ownership",
        type=Path,
        default=input_root / "ownership.yaml",
    )
    parser.add_argument(
        "--policies",
        type=Path,
        default=input_root / "sites",
    )
    parser.add_argument("--output", type=Path, default=default_skill)
    parser.add_argument(
        "--manual-skill-root",
        type=Path,
        default=default_skill,
    )
    parser.add_argument(
        "--site",
        action="append",
        default=None,
        help="Generate only this site-owned subtree; repeat for multiple sites.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Generate to a temporary sibling and fail if checked-in output differs.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        model = build_generation_model(
            load_catalog(args.catalog),
            load_ownership(args.ownership),
            load_policies(args.policies),
        )
        if args.check:
            if args.site:
                raise GenerationError("--check cannot be combined with --site")
            check_root = args.output.parent / f".{args.output.name}.generation-check"
            if check_root.exists():
                shutil.rmtree(check_root)
            try:
                generate(
                    model,
                    output_root=check_root,
                    manual_skill_root=args.manual_skill_root,
                )
                expected = {
                    path.relative_to(check_root).as_posix(): path.read_bytes()
                    for path in check_root.rglob("*")
                    if path.is_file()
                }
                actual = {
                    path.relative_to(args.output).as_posix(): path.read_bytes()
                    for path in args.output.rglob("*")
                    if path.is_file()
                }
                if actual != expected:
                    missing = sorted(set(expected) - set(actual))
                    extra = sorted(set(actual) - set(expected))
                    changed = sorted(
                        path
                        for path in set(expected) & set(actual)
                        if expected[path] != actual[path]
                    )
                    raise GenerationError(
                        "checked-in OpenCLI Skill tree drifted; "
                        f"missing={missing[:10]}, extra={extra[:10]}, "
                        f"changed={changed[:10]}"
                    )
            finally:
                if check_root.exists():
                    shutil.rmtree(check_root)
        else:
            result = generate(
                model,
                output_root=args.output,
                manual_skill_root=args.manual_skill_root,
                selected_sites=args.site,
            )
            print(
                json.dumps(
                    {
                        "ok": True,
                        "site_count": result.site_count,
                        "command_count": result.command_count,
                        "file_count": result.file_count,
                        "manifest_sha256": result.manifest_sha256,
                    },
                    sort_keys=True,
                )
            )
    except GenerationError as exc:
        print(f"OpenCLI Skill generation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "CATALOG_COMMAND_COUNT",
    "CATALOG_SITE_COUNT",
    "EXCLUDED_ADAPTERS",
    "GENERATED_COMMAND_COUNT",
    "GENERATED_SITE_COUNT",
    "OPENCLI_VERSION",
    "CatalogCommand",
    "CatalogSnapshot",
    "CommandPolicy",
    "GenerationError",
    "GenerationModel",
    "GenerationResult",
    "OperationPolicy",
    "Ownership",
    "SitePolicy",
    "build_generation_model",
    "generate",
    "load_catalog",
    "load_ownership",
    "load_policies",
]
