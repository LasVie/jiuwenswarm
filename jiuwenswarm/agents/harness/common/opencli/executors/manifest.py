"""Strict manifest-bound argv rendering for reviewed public-read commands."""

from __future__ import annotations

import math
import re
from collections.abc import Mapping, Sequence
from typing import Any

from jiuwenswarm.agents.harness.common.opencli.executor import (
    OpenCLIExecutionError,
)

_SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_ARGUMENT_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
_STRING_TYPES = {"str", "string"}
_INTEGER_TYPES = {"int"}
_NUMBER_TYPES = {"float", "number"}
_BOOLEAN_TYPES = {"bool", "boolean"}
_SUPPORTED_TYPES = _STRING_TYPES | _INTEGER_TYPES | _NUMBER_TYPES | _BOOLEAN_TYPES
_CONSTRAINT_KEYS = {"minimum", "maximum", "pattern", "max_length"}
_MAX_PATTERN_CHARS = 4_096
_MISSING = object()


def validate_generic_public_read_contract(contract: Any) -> None:
    """Reject a generic executor contract outside its reviewed low-risk lane."""

    if _contract_field(contract, "executor", "") != "generic_manifest_read":
        _contract_error(
            "opencli_executor_unsupported",
            "The disclosed command is not a generic manifest read",
            fallback_allowed=True,
        )
    if _contract_field(contract, "execution_state", "") != "enabled":
        _contract_error(
            "opencli_executor_disabled",
            "The disclosed generic OpenCLI executor is not enabled",
            fallback_allowed=True,
        )
    if _contract_field(contract, "semantic_effect", "") != "public_read":
        _contract_error(
            "opencli_executor_effect_unsupported",
            "Generic manifest execution is restricted to public reads",
        )
    if _contract_field(contract, "risk", "") != "low":
        _contract_error(
            "opencli_executor_risk_unsupported",
            "Generic public-read execution is restricted to low-risk commands",
        )
    if _contract_field(contract, "auth", "") != "none":
        _contract_error(
            "opencli_executor_auth_unsupported",
            "Generic public-read execution cannot use an authenticated session",
        )
    if _contract_field(contract, "transport", "") != "public_http":
        _contract_error(
            "opencli_executor_transport_unsupported",
            "Generic public-read execution requires public HTTP transport",
        )
    if _contract_field(contract, "browser", None) is not False:
        _contract_error(
            "opencli_executor_browser_unsupported",
            "Generic public-read execution cannot start a browser-backed command",
        )
    if _contract_field(contract, "strategy", "") != "public":
        _contract_error(
            "opencli_executor_strategy_unsupported",
            "Generic public-read execution requires the public OpenCLI strategy",
        )
    if _contract_field(contract, "access", "") != "read":
        _contract_error(
            "opencli_executor_access_unsupported",
            "Generic public-read execution cannot use a write command",
        )
    if _contract_field(contract, "confirmation", "") != "none":
        _contract_error(
            "opencli_executor_confirmation_unsupported",
            "Generic public-read execution cannot require a write confirmation",
        )
    for field in ("file_inputs", "file_outputs", "sensitive_output"):
        value = _contract_field(contract, field, _MISSING)
        if (
            value is _MISSING
            or isinstance(value, (str, bytes, bytearray))
            or not isinstance(value, Sequence)
            or len(value) != 0
        ):
            _contract_error(
                "opencli_executor_io_unsupported",
                "Generic public-read execution cannot use files or sensitive output",
            )


def render_manifest_command_argv(
    contract: Any,
    arguments: Mapping[str, Any],
) -> list[str]:
    """Render only the site, command, and arguments frozen in the contract."""

    validate_generic_public_read_contract(contract)
    if not isinstance(arguments, Mapping) or any(
        not isinstance(key, str) for key in arguments
    ):
        _contract_error(
            "opencli_arguments_invalid",
            "arguments must be an object with string keys",
        )

    site = str(_contract_field(contract, "site", "") or "").strip()
    command = str(_contract_field(contract, "command", "") or "").strip()
    if not _SLUG_PATTERN.fullmatch(site) or not _SLUG_PATTERN.fullmatch(command):
        _contract_error(
            "opencli_manifest_command_invalid",
            "The manifest-bound site and command must be canonical slugs",
        )

    raw_specs = _contract_field(contract, "args", _MISSING)
    if raw_specs is _MISSING:
        command_spec = _contract_field(contract, "command_spec", None)
        raw_specs = _spec_field(command_spec, "args", _MISSING)
    if (
        raw_specs is _MISSING
        or isinstance(raw_specs, (str, bytes, bytearray))
        or not isinstance(raw_specs, Sequence)
    ):
        _contract_error(
            "opencli_manifest_arguments_invalid",
            "The manifest command has no ordered argument schema",
        )

    specs_by_name: dict[str, Any] = {}
    ordered_specs: list[tuple[str, Any]] = []
    for raw_spec in raw_specs:
        name = str(_spec_field(raw_spec, "name", "") or "").strip()
        if not _ARGUMENT_NAME_PATTERN.fullmatch(name) or name in specs_by_name:
            _contract_error(
                "opencli_manifest_arguments_invalid",
                "The manifest command contains an invalid or duplicate argument",
            )
        argument_type = str(_spec_field(raw_spec, "type", "") or "").strip()
        if argument_type not in _SUPPORTED_TYPES:
            _contract_error(
                "opencli_manifest_arguments_invalid",
                f"Manifest argument '{name}' has an unsupported type",
            )
        _validate_constraint_schema(name, raw_spec, argument_type)
        specs_by_name[name] = raw_spec
        ordered_specs.append((name, raw_spec))

    unknown = sorted(set(arguments) - set(specs_by_name))
    if unknown:
        _contract_error(
            "opencli_argument_unknown",
            f"Unknown OpenCLI argument: {unknown[0]}",
        )

    named_tokens: list[str] = []
    positional_tokens: list[str] = []
    for name, spec in ordered_specs:
        if name not in arguments:
            if _spec_field(spec, "required", False) is True:
                _contract_error(
                    "opencli_argument_required",
                    f"OpenCLI argument '{name}' is required",
                )
            continue
        rendered = _render_argument_value(name, spec, arguments[name])
        if _spec_field(spec, "positional", False) is True:
            positional_tokens.append(rendered)
        else:
            # The equals form prevents values beginning with '-' from being
            # reinterpreted as another optional Commander flag.
            named_tokens.append(f"--{name}={rendered}")

    argv = [site, command, *named_tokens, "-f", "json"]
    if positional_tokens:
        # Keep every payload-derived positional after the option terminator.
        argv.extend(["--", *positional_tokens])
    return argv


def _render_argument_value(name: str, spec: Any, value: Any) -> str:
    if value is None:
        _argument_type_error(name)
    argument_type = str(_spec_field(spec, "type", "") or "").strip()
    if argument_type in _STRING_TYPES:
        if not isinstance(value, str):
            _argument_type_error(name)
        rendered = value
    elif argument_type in _INTEGER_TYPES:
        if isinstance(value, bool) or not isinstance(value, int):
            _argument_type_error(name)
        rendered = str(value)
    elif argument_type in _NUMBER_TYPES:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            _argument_type_error(name)
        numeric = float(value)
        if not math.isfinite(numeric):
            _argument_type_error(name)
        rendered = str(value)
    elif argument_type in _BOOLEAN_TYPES:
        if not isinstance(value, bool):
            _argument_type_error(name)
        rendered = "true" if value else "false"
    else:  # Defensive: schemas are validated before values are rendered.
        _contract_error(
            "opencli_manifest_arguments_invalid",
            f"Manifest argument '{name}' has an unsupported type",
        )

    if "\x00" in rendered:
        _argument_type_error(name)
    choices = _spec_field(spec, "choices", ())
    if choices is None:
        choices = ()
    if isinstance(choices, (str, bytes, bytearray)) or not isinstance(
        choices, Sequence
    ):
        _contract_error(
            "opencli_manifest_arguments_invalid",
            f"Manifest argument '{name}' has invalid choices",
        )
    if choices and rendered not in {str(choice) for choice in choices}:
        _contract_error(
            "opencli_argument_choice_invalid",
            f"OpenCLI argument '{name}' is outside its declared choices",
        )
    _enforce_constraints(name, spec, value, rendered)
    return rendered


def _validate_constraint_schema(
    name: str,
    spec: Any,
    argument_type: str,
) -> None:
    constraints = _spec_field(spec, "constraints", _MISSING)
    if constraints is _MISSING:
        return
    if not isinstance(constraints, Mapping):
        _manifest_argument_error(name, "has invalid constraints")
    unknown = set(constraints).difference(_CONSTRAINT_KEYS)
    if unknown:
        _manifest_argument_error(name, "has unsupported constraints")

    minimum = constraints.get("minimum", _MISSING)
    maximum = constraints.get("maximum", _MISSING)
    for field, bound in (("minimum", minimum), ("maximum", maximum)):
        if bound is _MISSING:
            continue
        if (
            argument_type not in _INTEGER_TYPES | _NUMBER_TYPES
            or isinstance(bound, bool)
            or not isinstance(bound, (int, float))
            or not math.isfinite(float(bound))
        ):
            _manifest_argument_error(name, f"has an invalid {field}")
    if minimum is not _MISSING and maximum is not _MISSING and minimum > maximum:
        _manifest_argument_error(name, "has an inverted numeric range")

    max_length = constraints.get("max_length", _MISSING)
    if max_length is not _MISSING and (
        argument_type not in _STRING_TYPES
        or isinstance(max_length, bool)
        or not isinstance(max_length, int)
        or max_length < 0
    ):
        _manifest_argument_error(name, "has an invalid max_length")

    pattern = constraints.get("pattern", _MISSING)
    if pattern is not _MISSING:
        if (
            argument_type not in _STRING_TYPES
            or not isinstance(pattern, str)
            or len(pattern) > _MAX_PATTERN_CHARS
        ):
            _manifest_argument_error(name, "has an invalid pattern")
        try:
            re.compile(pattern)
        except re.error as exc:
            raise OpenCLIExecutionError(
                "opencli_manifest_arguments_invalid",
                f"Manifest argument '{name}' has an invalid pattern",
                attempted=False,
                fallback_allowed=False,
            ) from exc


def _enforce_constraints(
    name: str,
    spec: Any,
    value: Any,
    rendered: str,
) -> None:
    constraints = _spec_field(spec, "constraints", _MISSING)
    if constraints is _MISSING:
        return

    minimum = constraints.get("minimum", _MISSING)
    maximum = constraints.get("maximum", _MISSING)
    if (minimum is not _MISSING and value < minimum) or (
        maximum is not _MISSING and value > maximum
    ):
        _contract_error(
            "opencli_argument_range_invalid",
            f"OpenCLI argument '{name}' is outside its declared range",
        )

    max_length = constraints.get("max_length", _MISSING)
    if max_length is not _MISSING and len(rendered) > max_length:
        _contract_error(
            "opencli_argument_length_invalid",
            f"OpenCLI argument '{name}' exceeds its declared length",
        )

    pattern = constraints.get("pattern", _MISSING)
    if pattern is not _MISSING and re.search(pattern, rendered) is None:
        _contract_error(
            "opencli_argument_pattern_invalid",
            f"OpenCLI argument '{name}' does not match its declared pattern",
        )


def _manifest_argument_error(name: str, detail: str) -> None:
    _contract_error(
        "opencli_manifest_arguments_invalid",
        f"Manifest argument '{name}' {detail}",
    )


def _argument_type_error(name: str) -> None:
    _contract_error(
        "opencli_argument_type_invalid",
        f"OpenCLI argument '{name}' has the wrong JSON type",
    )


def _contract_field(value: Any, field: str, default: Any) -> Any:
    if isinstance(value, Mapping):
        return value.get(field, default)
    return getattr(value, field, default)


def _spec_field(value: Any, field: str, default: Any) -> Any:
    if isinstance(value, Mapping):
        return value.get(field, default)
    return getattr(value, field, default)


def _contract_error(
    code: str,
    message: str,
    *,
    fallback_allowed: bool = False,
) -> None:
    raise OpenCLIExecutionError(
        code,
        message,
        attempted=False,
        fallback_allowed=fallback_allowed,
    )


__all__ = [
    "render_manifest_command_argv",
    "validate_generic_public_read_contract",
]
