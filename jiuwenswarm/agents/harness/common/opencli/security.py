# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Security snapshots shared by OpenCLI disclosure and execution gates."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jiuwenswarm.server.runtime.skill.skilldev.state_utils import (
    get_skill_enabled,
)

from jiuwenswarm.agents.harness.common.opencli.contracts import (
    OPENCLI_WEB_SKILL_NAME,
)

_MAX_SKILL_STATE_BYTES = 4 * 1024 * 1024
_MISSING_STATE_BYTES = b"opencli-skill-state:missing-default-enabled:v1"
_UNREADABLE_STATE_BYTES = b"opencli-skill-state:unreadable:v1"
_OVERSIZED_STATE_BYTES = b"opencli-skill-state:oversized:v1"


@dataclass(frozen=True, slots=True)
class SkillEnabledSnapshot:
    """Exact global Skill enabled decision and state-file fingerprint."""

    enabled: bool
    valid: bool
    code: str
    state_path: Path
    state_sha256: str


class _DuplicateStateKey(ValueError):
    pass


def load_skill_enabled_snapshot(
    skills_root: str | Path,
    skill_name: str = OPENCLI_WEB_SKILL_NAME,
) -> SkillEnabledSnapshot:
    """Load the global enabled flag, failing closed for invalid state.

    A missing legacy state file intentionally defaults to enabled. Once a
    state file exists, malformed JSON, an invalid root/config shape, or a
    non-boolean explicit flag disables automatic OpenCLI disclosure.
    """
    unresolved_state_path = Path(skills_root).expanduser() / "skills_state.json"
    try:
        state_path = unresolved_state_path.resolve()
    except (OSError, RuntimeError, ValueError):
        return SkillEnabledSnapshot(
            enabled=False,
            valid=False,
            code="opencli_skill_state_unreadable",
            state_path=unresolved_state_path,
            state_sha256=_digest(_UNREADABLE_STATE_BYTES),
        )
    try:
        size = state_path.stat().st_size
    except FileNotFoundError:
        return SkillEnabledSnapshot(
            enabled=True,
            valid=True,
            code="opencli_skill_state_missing_default_enabled",
            state_path=state_path,
            state_sha256=_digest(_MISSING_STATE_BYTES),
        )
    except OSError:
        return SkillEnabledSnapshot(
            enabled=False,
            valid=False,
            code="opencli_skill_state_unreadable",
            state_path=state_path,
            state_sha256=_digest(_UNREADABLE_STATE_BYTES),
        )

    if size > _MAX_SKILL_STATE_BYTES:
        return SkillEnabledSnapshot(
            enabled=False,
            valid=False,
            code="opencli_skill_state_invalid",
            state_path=state_path,
            state_sha256=_digest(_OVERSIZED_STATE_BYTES),
        )
    content_bytes: bytes | None = None
    try:
        content_bytes = state_path.read_bytes()
        content = content_bytes.decode("utf-8")
        state = json.loads(
            content,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_json_constant,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, _DuplicateStateKey):
        if content_bytes is None:
            content_bytes = _safe_state_bytes(state_path)
        return SkillEnabledSnapshot(
            enabled=False,
            valid=False,
            code="opencli_skill_state_invalid",
            state_path=state_path,
            state_sha256=_digest(content_bytes),
        )

    state_sha256 = _digest(content_bytes)
    if not isinstance(state, dict):
        return _invalid_snapshot(state_path, state_sha256)
    configs = state.get("skill_configs")
    if configs is None:
        return _enabled_snapshot(state_path, state_sha256)
    if not isinstance(configs, dict):
        return _invalid_snapshot(state_path, state_sha256)
    config = configs.get(skill_name)
    if config is None:
        return _enabled_snapshot(state_path, state_sha256)
    if not isinstance(config, dict):
        return _invalid_snapshot(state_path, state_sha256)
    if "enabled" in config and not isinstance(config["enabled"], bool):
        return _invalid_snapshot(state_path, state_sha256)

    enabled = get_skill_enabled(state, skill_name)
    return SkillEnabledSnapshot(
        enabled=enabled,
        valid=True,
        code="ok" if enabled else "opencli_skill_disabled",
        state_path=state_path,
        state_sha256=state_sha256,
    )


def _enabled_snapshot(
    state_path: Path,
    state_sha256: str,
) -> SkillEnabledSnapshot:
    return SkillEnabledSnapshot(
        enabled=True,
        valid=True,
        code="ok",
        state_path=state_path,
        state_sha256=state_sha256,
    )


def _invalid_snapshot(
    state_path: Path,
    state_sha256: str,
) -> SkillEnabledSnapshot:
    return SkillEnabledSnapshot(
        enabled=False,
        valid=False,
        code="opencli_skill_state_invalid",
        state_path=state_path,
        state_sha256=state_sha256,
    )


def _safe_state_bytes(state_path: Path) -> bytes:
    try:
        content_bytes = state_path.read_bytes()
    except OSError:
        return _UNREADABLE_STATE_BYTES
    if len(content_bytes) > _MAX_SKILL_STATE_BYTES:
        return _OVERSIZED_STATE_BYTES
    return content_bytes


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateStateKey(key)
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise _DuplicateStateKey(value)


def _digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


__all__ = [
    "SkillEnabledSnapshot",
    "load_skill_enabled_snapshot",
]
