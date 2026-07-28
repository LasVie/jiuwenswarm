# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Utilities for linking team skill directories."""

from __future__ import annotations

import json
import logging
import os
import shutil
import stat
import subprocess
import sys
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import winerror
except ImportError:  # pragma: no cover - unavailable outside Windows
    ERROR_PRIVILEGE_NOT_HELD = 1314
else:
    ERROR_PRIVILEGE_NOT_HELD = winerror.ERROR_PRIVILEGE_NOT_HELD

_MANAGED_SKILL_COPY_MARKER = ".jiuwenswarm-managed-skill-copy.json"
_MANAGED_SKILL_COPY_SCHEMA_VERSION = 1


def is_valid_skill_dir(path: Path) -> bool:
    """Return whether the path points to a valid skill directory."""
    return path.is_dir() and (path / "SKILL.md").is_file()


def path_exists_or_link(path: Path) -> bool:
    """Return whether a path entry exists, including broken links."""
    return os.path.lexists(path)


def _is_windows_reparse_point(path: Path) -> bool:
    """Return whether a path entry is a Windows reparse point."""
    if sys.platform != "win32":
        return False
    try:
        file_attributes = os.lstat(path).st_file_attributes
    except (AttributeError, OSError):
        return False
    return bool(file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def _is_skill_dir_link(path: Path) -> bool:
    """Return whether the path entry is a skill directory link."""
    return path.is_symlink() or _is_windows_reparse_point(path)


def _normalized_path(path: Path) -> str:
    """Return a platform-aware absolute path identity."""
    return os.path.normcase(os.path.normpath(str(path.resolve(strict=False))))


def _managed_copy_marker_payload(source: Path, target: Path) -> dict[str, object]:
    return {
        "schema_version": _MANAGED_SKILL_COPY_SCHEMA_VERSION,
        "source": str(source.resolve(strict=True)),
        "target": str(target.resolve(strict=False)),
    }


def _write_managed_copy_marker(
    copy_root: Path,
    source: Path,
    final_target: Path,
) -> None:
    """Write the copy ownership marker after the Skill contents are complete."""
    marker = copy_root / _MANAGED_SKILL_COPY_MARKER
    marker_payload = _managed_copy_marker_payload(source, final_target)
    marker.write_text(
        json.dumps(
            marker_payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n",
        encoding="utf-8",
    )


def _read_managed_copy_marker(target: Path) -> dict[str, str] | None:
    """Return a validated marker for an ordinary managed-copy directory."""
    if not target.is_dir() or _is_skill_dir_link(target):
        return None
    marker = target / _MANAGED_SKILL_COPY_MARKER
    if marker.is_symlink() or not marker.is_file():
        return None
    try:
        payload = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    schema_version = payload.get("schema_version")
    source = payload.get("source")
    marker_target = payload.get("target")
    if (
        isinstance(schema_version, bool)
        or schema_version != _MANAGED_SKILL_COPY_SCHEMA_VERSION
        or not isinstance(source, str)
        or not source
        or not isinstance(marker_target, str)
        or not marker_target
    ):
        return None
    source_path = Path(source)
    target_path = Path(marker_target)
    if not source_path.is_absolute() or not target_path.is_absolute():
        return None
    if _normalized_path(target_path) != _normalized_path(target):
        return None
    return {"source": source, "target": marker_target}


def _managed_copy_matches_source(target: Path, source: Path) -> bool:
    marker = _read_managed_copy_marker(target)
    return (
        marker is not None
        and _normalized_path(Path(marker["source"])) == _normalized_path(source)
    )


def _remove_managed_skill_copy(
    target: Path,
    *,
    expected_source: Path | None = None,
) -> bool:
    """Remove only an ordinary directory carrying a valid matching marker."""
    marker = _read_managed_copy_marker(target)
    if marker is None:
        return False
    if (
        expected_source is not None
        and _normalized_path(Path(marker["source"]))
        != _normalized_path(expected_source)
    ):
        return False
    shutil.rmtree(target)
    return True


def _new_managed_copy_sibling(target: Path, purpose: str) -> Path:
    token = uuid.uuid4().hex
    return target.parent / f".{target.name}.{purpose}-{token}"


def _stage_managed_skill_copy(source: Path, final_target: Path) -> Path:
    """Create a complete marked copy beside its final target."""
    staging = _new_managed_copy_sibling(final_target, "managed-copy")
    try:
        shutil.copytree(
            str(source),
            str(staging),
            symlinks=False,
            copy_function=shutil.copy2,
            dirs_exist_ok=False,
        )
        _write_managed_copy_marker(staging, source, final_target)
        return staging
    except Exception:
        if os.path.lexists(staging):
            shutil.rmtree(staging)
        raise


def _refresh_managed_skill_copy(source: Path, target: Path) -> bool:
    """Replace a matching managed copy while preserving it on staging failure."""
    if not _managed_copy_matches_source(target, source):
        return False

    staging = _stage_managed_skill_copy(source, target)
    backup = _new_managed_copy_sibling(target, "managed-backup")
    try:
        target.rename(backup)
        try:
            staging.rename(target)
        except Exception:
            backup.rename(target)
            raise
        try:
            shutil.rmtree(backup)
        except OSError:
            logger.exception(
                "[TeamSkillLinks] refreshed managed copy but failed to remove "
                "backup: %s",
                backup,
            )
        return True
    finally:
        if os.path.lexists(staging):
            shutil.rmtree(staging)


def ensure_skill_dir_links(source: Path, target: Path) -> None:
    """Link every valid skill directory from *source* into *target*.

    A valid skill is a sub-directory containing a ``SKILL.md`` file.
    Existing target entries are left untouched.
    """
    if not source.is_dir():
        return
    target.mkdir(parents=True, exist_ok=True)
    linked = 0
    for skill_dir in source.iterdir():
        if not is_valid_skill_dir(skill_dir):
            continue
        dest = target / skill_dir.name
        if path_exists_or_link(dest):
            continue
        link_skill_dir(skill_dir, dest)
        linked += 1
    if linked:
        logger.info("[TeamSkillLinks] linked %d skills: %s -> %s", linked, source, target)


def prune_skill_dir_links(
    source: Path,
    target: Path,
    selected_skill_names: set[str] | None = None,
) -> None:
    """Remove stale managed entries without touching ordinary directories."""
    if not target.is_dir():
        return

    removed = 0
    refreshed = 0
    for entry in target.iterdir():
        source_skill_dir = source / entry.name
        if _is_skill_dir_link(entry):
            if selected_skill_names is not None and entry.name not in selected_skill_names:
                remove_skill_dir_link(entry)
                removed += 1
                continue
            if not is_valid_skill_dir(source_skill_dir):
                remove_skill_dir_link(entry)
                removed += 1
            continue

        if not _managed_copy_matches_source(entry, source_skill_dir):
            continue
        if (
            selected_skill_names is not None
            and entry.name not in selected_skill_names
        ) or not is_valid_skill_dir(source_skill_dir):
            if _remove_managed_skill_copy(
                entry,
                expected_source=source_skill_dir,
            ):
                removed += 1
            continue
        if _refresh_managed_skill_copy(source_skill_dir, entry):
            refreshed += 1
    if removed:
        logger.info("[TeamSkillLinks] pruned %d stale skill links: %s", removed, target)
    if refreshed:
        logger.info(
            "[TeamSkillLinks] refreshed %d managed skill copies: %s",
            refreshed,
            target,
        )


def sync_skill_dir_links(source: Path, target: Path) -> None:
    """Synchronize valid skill links from *source* into *target*."""
    prune_skill_dir_links(source, target)
    ensure_skill_dir_links(source, target)


def link_skill_dir(source: Path, target: Path) -> None:
    """Create a directory link for a single skill directory."""
    if path_exists_or_link(target):
        return
    try:
        _create_directory_link(source.resolve(), target)
    except Exception:
        if path_exists_or_link(target):
            logger.debug("[TeamSkillLinks] skill dir link already exists after create race: %s", target)
            return
        logger.exception("[TeamSkillLinks] failed to link skill dir: %s -> %s", target, source)
        raise


def remove_skill_dir_link(target: Path) -> None:
    """Remove a link or marked managed copy, never an ordinary directory."""
    if target.is_symlink():
        target.unlink()
        return
    if _is_windows_reparse_point(target):
        os.rmdir(target)
        return
    _remove_managed_skill_copy(target)


def _create_directory_link(target_path: Path, link_path: Path) -> None:
    """Create a directory link, falling back to a junction on Windows or a copy on sandboxed runtimes."""
    try:
        os.symlink(str(target_path), str(link_path), target_is_directory=True)
        return
    except OSError as exc:
        errno = getattr(exc, "errno", None)
        is_privilege_error = errno in (13, 1)  # EACCES/EPERM
        if sys.platform == "win32" and getattr(exc, "winerror", None) == ERROR_PRIVILEGE_NOT_HELD:
            _create_windows_junction(target_path, link_path)
            return
        if not is_privilege_error:
            raise
        # Sandboxed runtimes (e.g. HarmonyOS app sandbox) forbid symlink(2)
        # even inside the app's own filesDir. Fall back to a real copy so
        # team skill directories remain usable without kernel privileges.
        logger.info(
            "[TeamSkillLinks] symlink not permitted (%s); copying %s -> %s",
            exc, target_path, link_path,
        )
        _copy_skill_directory(target_path, link_path)


def _copy_skill_directory(target_path: Path, link_path: Path) -> None:
    """Copy a skill directory as a fallback when symlinks are unavailable."""
    link_path.parent.mkdir(parents=True, exist_ok=True)
    if link_path.exists() or os.path.lexists(link_path):
        return
    staging = _stage_managed_skill_copy(target_path, link_path)
    try:
        staging.rename(link_path)
    finally:
        if os.path.lexists(staging):
            shutil.rmtree(staging)


def _create_windows_junction(target_path: Path, link_path: Path) -> None:
    """Create a directory junction using ``mklink /J`` on Windows."""
    cmd_path = os.path.join(
        os.environ.get("SystemRoot", r"C:\Windows"),
        "System32",
        "cmd.exe",
    )
    result = subprocess.run(
        [cmd_path, "/c", "mklink", "/J", str(link_path), str(target_path)],
        capture_output=True,
        text=True,
        check=False,
        shell=False,
    )
    if result.returncode != 0:
        error_output = result.stderr.strip() or result.stdout.strip()
        raise OSError(f"Failed to create junction {link_path} -> {target_path}: {error_output}")
