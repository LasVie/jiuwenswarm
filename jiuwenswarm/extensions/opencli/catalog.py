# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""Source-neutral site command catalog and executor contract.

Everything above this module (tools, worker page, confirmation, pending
records, result classification) depends only on these types. A command
source (OpenCLI today, a self-maintained library later) converts its own
metadata into ``CommandSpec`` and its own outcomes into ``RunOutcome``.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Literal, Mapping, Protocol

RunCategory = Literal["ok", "empty", "invalid_args", "needs_user", "env_unavailable", "timeout", "error"]

_INT_TYPES = frozenset({"int"})
_NUMBER_TYPES = frozenset({"number", "float"})
_BOOL_TYPES = frozenset({"bool", "boolean"})


class ArgumentValidationError(ValueError):
    """Arguments were rejected before any process started."""


@dataclass(frozen=True)
class ArgSpec:
    name: str
    type: str = "str"
    required: bool = False
    positional: bool = False
    choices: tuple[str, ...] = ()
    default: Any = None
    help: str = ""

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "ArgSpec":
        return cls(
            name=str(payload["name"]),
            type=str(payload.get("type") or "str"),
            required=bool(payload.get("required")),
            positional=bool(payload.get("positional")),
            choices=tuple(str(choice) for choice in payload.get("choices") or ()),
            default=payload.get("default"),
            help=str(payload.get("help") or ""),
        )

    def describe(self) -> dict[str, Any]:
        described: dict[str, Any] = {"name": self.name, "type": self.type, "required": self.required}
        if self.positional:
            described["positional"] = True
        if self.choices:
            described["choices"] = list(self.choices)
        if self.default is not None:
            described["default"] = self.default
        if self.help:
            described["help"] = self.help
        return described

    def normalize(self, value: Any) -> str:
        """Validate one value like upstream does and return its CLI text."""
        if self.type in _BOOL_TYPES:
            if isinstance(value, bool):
                text = "true" if value else "false"
            elif isinstance(value, str) and value.strip().lower() in {"true", "false", "1", "0"}:
                text = "true" if value.strip().lower() in {"true", "1"} else "false"
            else:
                raise ArgumentValidationError(f'argument "{self.name}" must be a boolean')
        elif self.type in _INT_TYPES:
            if isinstance(value, bool) or not _is_integral(value):
                raise ArgumentValidationError(f'argument "{self.name}" must be an integer')
            text = str(int(float(value)))
        elif self.type in _NUMBER_TYPES:
            if isinstance(value, bool) or not _is_number(value):
                raise ArgumentValidationError(f'argument "{self.name}" must be a number')
            text = str(value)
        else:
            if isinstance(value, (dict, list)):
                raise ArgumentValidationError(f'argument "{self.name}" must be a string')
            text = str(value)
        if self.choices and text not in self.choices and str(value) not in self.choices:
            raise ArgumentValidationError(
                f'argument "{self.name}" must be one of: {", ".join(self.choices)}'
            )
        return text


def _is_number(value: Any) -> bool:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return number == number and number not in (float("inf"), float("-inf"))


def _is_integral(value: Any) -> bool:
    return _is_number(value) and float(value).is_integer()


# Argument help is cut in site-level listings; the full text stays in a command-level describe.
_SITE_HELP_LIMIT = 100


@dataclass(frozen=True)
class CommandSpec:
    source: str
    site: str
    command: str
    description: str
    access: Literal["read", "write"]
    needs_browser: bool
    args: tuple[ArgSpec, ...] = ()
    columns: tuple[str, ...] = ()
    domain: str = ""

    @property
    def key(self) -> tuple[str, str]:
        return (self.site, self.command)

    @property
    def qualified_name(self) -> str:
        return f"{self.site}/{self.command}"

    def normalize_args(self, args: Mapping[str, Any] | None) -> list[tuple[ArgSpec, str]]:
        """Reject unknown names and invalid values; return ordered CLI values."""
        provided = dict(args or {})
        known = {arg.name for arg in self.args}
        unknown = sorted(set(provided) - known)
        if unknown:
            raise ArgumentValidationError(
                f"unknown argument(s) for {self.qualified_name}: {', '.join(unknown)}; "
                "call opencli_describe to read the argument list"
            )
        ordered: list[tuple[ArgSpec, str]] = []
        skipped_positional = ""
        for arg in self.args:
            value = provided.get(arg.name)
            if value is None or value == "":
                if arg.required:
                    raise ArgumentValidationError(f'argument "{arg.name}" is required')
                if arg.positional and not skipped_positional:
                    skipped_positional = arg.name
                continue
            if arg.positional and skipped_positional:
                # Positionals are matched by order: the value would land in the skipped slot.
                raise ArgumentValidationError(
                    f'argument "{skipped_positional}" must also be given when "{arg.name}" is given'
                )
            ordered.append((arg, arg.normalize(value)))
        return ordered

    def summary(self) -> dict[str, Any]:
        return {
            "command": self.command,
            "description": self.description,
            "access": self.access,
            "needs_browser": self.needs_browser,
        }

    def describe(self) -> dict[str, Any]:
        return {
            **self.summary(),
            "site": self.site,
            "args": [arg.describe() for arg in self.args],
            "columns": list(self.columns),
        }

    def site_entry(self) -> dict[str, Any]:
        """Summary plus compact arguments, so one site-level describe is enough to run any command."""
        args = []
        for arg in self.args:
            entry = arg.describe()
            if entry.get("type") == "str":
                entry.pop("type")
            if not entry.get("required"):
                entry.pop("required", None)
            if "help" in entry:
                entry["help"] = entry["help"][:_SITE_HELP_LIMIT]
            args.append(entry)
        return {**self.summary(), "args": args}


@dataclass(frozen=True)
class Catalog:
    commands: Mapping[tuple[str, str], CommandSpec] = field(default_factory=dict)
    version: str = ""

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], *, source: str) -> "Catalog":
        commands: dict[tuple[str, str], CommandSpec] = {}
        for entry in payload.get("commands") or []:
            spec = CommandSpec(
                source=source,
                site=str(entry["site"]),
                command=str(entry["command"]),
                description=str(entry.get("description") or ""),
                access="write" if entry.get("access") == "write" else "read",
                needs_browser=bool(entry.get("needs_browser")),
                args=tuple(ArgSpec.from_payload(arg) for arg in entry.get("args") or []),
                columns=tuple(str(column) for column in entry.get("columns") or []),
                domain=str(entry.get("domain") or ""),
            )
            commands.setdefault(spec.key, spec)
        return cls(commands=commands, version=str(payload.get("version") or ""))

    @classmethod
    def load(cls, path: Path, *, source: str) -> "Catalog":
        return cls.from_payload(json.loads(path.read_text(encoding="utf-8")), source=source)

    def filter_sites(self, enabled_sites: Iterable[str] | None) -> "Catalog":
        if enabled_sites is None:
            return self
        allowed = {str(site).strip() for site in enabled_sites if str(site).strip()}
        return Catalog(
            commands={key: spec for key, spec in self.commands.items() if key[0] in allowed},
            version=self.version,
        )

    def sites(self) -> list[str]:
        return sorted({site for site, _ in self.commands})

    def site_domain(self, site: str) -> str:
        """The site's most common command domain without "www.", or "" when none is declared."""
        counts: dict[str, int] = {}
        for spec in self.site_commands(site):
            domain = spec.domain.strip().lower().removeprefix("www.")
            if domain:
                counts[domain] = counts.get(domain, 0) + 1
        return max(sorted(counts), key=counts.get) if counts else ""

    def site_commands(self, site: str) -> list[CommandSpec]:
        return sorted(
            (spec for (spec_site, _), spec in self.commands.items() if spec_site == site),
            key=lambda spec: spec.command,
        )

    def get(self, site: str, command: str) -> CommandSpec | None:
        return self.commands.get((site, command))

    def __len__(self) -> int:
        return len(self.commands)

    @staticmethod
    def merge(*catalogs: "Catalog") -> "Catalog":
        """Merge in priority order: the first catalog providing a command wins."""
        merged: dict[tuple[str, str], CommandSpec] = {}
        for catalog in catalogs:
            for key, spec in catalog.commands.items():
                merged.setdefault(key, spec)
        return Catalog(commands=merged, version="+".join(c.version for c in catalogs if c.version))


@dataclass
class RunOutcome:
    started: bool
    category: RunCategory
    rows: Any = None
    exit_code: int | None = None
    killed: bool = False
    output_too_large: bool = False
    error_code: str = ""
    error_message: str = ""
    error_help: str = ""


class CommandCancelled(asyncio.CancelledError):
    """A cancelled invocation, after the source has stopped its process tree.

    Carry execution facts through cancellation so the tool can reset the page
    and persist an unknown write before propagating the task cancellation.
    """

    def __init__(self, outcome: RunOutcome) -> None:
        super().__init__(outcome.error_message)
        self.outcome = outcome


class CommandSource(Protocol):
    """A command provider, independent of the CLI package format.

    After launch, cancellation must stop the command's process tree and
    raise ``CommandCancelled`` with execution facts, so callers can retain
    unknown writes and clean up page activity before propagating cancellation.
    """

    id: str

    def catalog(self) -> Catalog: ...

    async def run(
        self,
        spec: CommandSpec,
        values: list[tuple[ArgSpec, str]],
        *,
        page_endpoint: str | None,
        timeout_s: float,
        cwd: Path,
    ) -> RunOutcome: ...
