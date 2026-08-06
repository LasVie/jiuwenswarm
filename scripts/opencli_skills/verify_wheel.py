#!/usr/bin/env python3
"""Verify packaged OpenCLI Web resources in a JiuwenSwarm wheel."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence


OPENCLI_SKILL_PREFIX = "jiuwenswarm/resources/agent/workspace/skills/opencli-web/"
EXPECTED_OPENCLI_VERSION = "1.8.6"
EXPECTED_SITE_COUNT = 165
EXPECTED_COMMAND_COUNT = 1179
MANAGED_MANIFEST_NAME = "generated-manifest.json"
REQUIRED_SKILL_RESOURCES = frozenset(
    {
        "SKILL.md",
        MANAGED_MANIFEST_NAME,
    }
)

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class WheelVerificationError(ValueError):
    """The wheel does not satisfy the OpenCLI resource contract."""


@dataclass(frozen=True, slots=True)
class WheelVerificationResult:
    """Verified inventory summary for one wheel."""

    wheel_path: Path
    site_count: int
    command_count: int
    managed_file_count: int
    wheel_member_count: int
    managed_manifest_sha256: str


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise WheelVerificationError(f"{label} must be a JSON object")
    return value


def _require_exact_int(
    value: Any,
    *,
    expected: int,
    label: str,
) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value != expected:
        raise WheelVerificationError(f"{label} is {value!r}, expected {expected}")


def _require_sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
        raise WheelVerificationError(f"{label} must be a lowercase SHA-256")
    return value


def _canonical_relative_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise WheelVerificationError(f"{label} is not a canonical path")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or path.as_posix() != value
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise WheelVerificationError(f"{label} is not a safe relative path")
    return value


def _load_json(value: bytes, label: str) -> dict[str, Any]:
    try:
        parsed = json.loads(value.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WheelVerificationError(f"{label} must be valid UTF-8 JSON") from exc
    return _require_mapping(parsed, label)


def _is_cached_bytecode(member: str) -> bool:
    path = PurePosixPath(member)
    return "__pycache__" in path.parts or path.suffix.lower() in {".pyc", ".pyo"}


def _read_wheel(
    wheel_path: Path,
) -> tuple[Path, set[str], dict[str, bytes]]:
    try:
        resolved_wheel = wheel_path.expanduser().resolve(strict=True)
    except OSError as exc:
        raise WheelVerificationError(
            f"wheel path cannot be resolved: {wheel_path}"
        ) from exc
    if not resolved_wheel.is_file():
        raise WheelVerificationError(f"wheel path is not a file: {wheel_path}")

    try:
        with zipfile.ZipFile(resolved_wheel) as wheel:
            infos = wheel.infolist()
            names = [info.filename for info in infos]
            if len(names) != len(set(names)):
                raise WheelVerificationError("wheel contains duplicate archive members")
            for name in names:
                comparable = name[:-1] if name.endswith("/") else name
                _canonical_relative_path(comparable, f"wheel member {name!r}")
            cached = sorted(name for name in names if _is_cached_bytecode(name))
            if cached:
                raise WheelVerificationError(
                    f"wheel contains cached bytecode: {cached[:5]}"
                )

            file_names = {info.filename for info in infos if not info.is_dir()}
            skill_files = {
                name.removeprefix(OPENCLI_SKILL_PREFIX): wheel.read(name)
                for name in sorted(file_names)
                if name.startswith(OPENCLI_SKILL_PREFIX)
            }
    except WheelVerificationError:
        raise
    except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
        raise WheelVerificationError(
            f"wheel archive cannot be read: {wheel_path}"
        ) from exc
    return resolved_wheel, file_names, skill_files


def _validate_required_members(
    skill_files: Mapping[str, bytes],
) -> None:
    missing_resources = sorted(REQUIRED_SKILL_RESOURCES - set(skill_files))
    if missing_resources:
        raise WheelVerificationError(
            f"wheel is missing required OpenCLI resources: {missing_resources}"
        )


def _validate_managed_manifest(
    skill_files: Mapping[str, bytes],
) -> tuple[dict[str, str], dict[str, Any]]:
    manifest = _load_json(
        skill_files[MANAGED_MANIFEST_NAME],
        MANAGED_MANIFEST_NAME,
    )
    _require_exact_int(
        manifest.get("schema_version"),
        expected=1,
        label="managed manifest schema_version",
    )
    if manifest.get("opencli_version") != EXPECTED_OPENCLI_VERSION:
        raise WheelVerificationError(
            "managed manifest OpenCLI version does not match the pinned release"
        )
    _require_exact_int(
        manifest.get("site_count"),
        expected=EXPECTED_SITE_COUNT,
        label="managed manifest sites count",
    )
    _require_exact_int(
        manifest.get("command_count"),
        expected=EXPECTED_COMMAND_COUNT,
        label="managed manifest commands count",
    )

    raw_files = _require_mapping(
        manifest.get("files"),
        "managed manifest files",
    )
    managed_files: dict[str, str] = {}
    for raw_relative, raw_digest in raw_files.items():
        relative = _canonical_relative_path(
            raw_relative,
            "managed manifest file",
        )
        if relative == MANAGED_MANIFEST_NAME:
            raise WheelVerificationError("managed manifest must not inventory itself")
        managed_files[relative] = _require_sha256(
            raw_digest,
            f"managed digest for {relative}",
        )
    _require_exact_int(
        manifest.get("file_count"),
        expected=len(managed_files),
        label="managed manifest file_count",
    )

    actual_owned = set(skill_files) - {MANAGED_MANIFEST_NAME}
    declared_owned = set(managed_files)
    if declared_owned != actual_owned:
        missing = sorted(declared_owned - actual_owned)
        unmanaged = sorted(actual_owned - declared_owned)
        raise WheelVerificationError(
            "managed file inventory mismatch; "
            f"missing_from_wheel={missing[:5]}, unmanaged_in_wheel={unmanaged[:5]}"
        )
    for relative, expected_digest in sorted(managed_files.items()):
        if _sha256(skill_files[relative]) != expected_digest:
            raise WheelVerificationError(f"managed file hash mismatch: {relative}")
    return managed_files, manifest


def _validate_packaged_sites(managed_files: Mapping[str, str]) -> int:
    sites: set[str] = set()
    for relative in managed_files:
        parts = PurePosixPath(relative).parts
        if (
            len(parts) == 3
            and parts[0] == "sites"
            and parts[2] == "index.md"
        ):
            site = parts[1]
            if not _SLUG_RE.fullmatch(site):
                raise WheelVerificationError(
                    f"packaged site is not a canonical slug: {site!r}"
                )
            sites.add(site)
    if len(sites) != EXPECTED_SITE_COUNT:
        raise WheelVerificationError(
            f"packaged sites count is {len(sites)}, expected {EXPECTED_SITE_COUNT}"
        )
    return len(sites)


def verify_wheel(wheel_path: str | Path) -> WheelVerificationResult:
    """Validate one built wheel without extracting or importing it."""
    resolved, wheel_members, skill_files = _read_wheel(Path(wheel_path))
    _validate_required_members(skill_files)
    managed_files, manifest = _validate_managed_manifest(skill_files)
    site_count = _validate_packaged_sites(managed_files)
    return WheelVerificationResult(
        wheel_path=resolved,
        site_count=site_count,
        command_count=int(manifest["command_count"]),
        managed_file_count=len(managed_files),
        wheel_member_count=len(wheel_members),
        managed_manifest_sha256=_sha256(skill_files[MANAGED_MANIFEST_NAME]),
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Verify OpenCLI Web resources and managed hashes in a JiuwenSwarm wheel."
        )
    )
    parser.add_argument("wheel", type=Path, help="Path to the .whl archive")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the wheel verifier CLI."""
    args = _build_parser().parse_args(argv)
    try:
        result = verify_wheel(args.wheel)
    except WheelVerificationError as exc:
        print(
            f"OpenCLI wheel verification failed: {exc}",
            file=sys.stderr,
        )
        return 1
    payload = asdict(result)
    payload["ok"] = True
    payload["wheel_path"] = str(result.wheel_path)
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
