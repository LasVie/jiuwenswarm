# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Tests for manifest-managed builtin Skill synchronization."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from jiuwenswarm.common import utils as workspace_utils
from jiuwenswarm.common.utils import CopyDiffResult

MANIFEST_NAME = "generated-manifest.json"


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _write_manifest_tree(
    root: Path,
    files: dict[str, bytes],
    *,
    schema_version: int = 1,
    manifest_files: dict[str, str] | None = None,
) -> bytes:
    root.mkdir(parents=True, exist_ok=True)
    for relative_path, content in files.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    file_hashes = (
        manifest_files
        if manifest_files is not None
        else {
            relative_path: _sha256(content)
            for relative_path, content in sorted(files.items())
        }
    )
    manifest = {
        "schema_version": schema_version,
        "generator_version": "test",
        "opencli_version": "1.8.6",
        "catalog_sha256": "1" * 64,
        "policy_sha256": "2" * 64,
        "site_count": 1,
        "command_count": 1,
        "file_count": len(file_hashes),
        "files": file_hashes,
    }
    manifest_bytes = (
        json.dumps(
            manifest,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")
    (root / MANIFEST_NAME).write_bytes(manifest_bytes)
    return manifest_bytes


def test_manifest_upgrade_refreshes_owned_files_and_prunes_only_stale_owned_paths(
    tmp_path: Path,
) -> None:
    source = tmp_path / "package" / "opencli-web"
    destination = tmp_path / "workspace" / "opencli-web"
    expected_manifest = _write_manifest_tree(
        source,
        {
            "SKILL.md": b"new root\n",
            "sites/new/SKILL.md": b"new site\n",
        },
    )
    _write_manifest_tree(
        destination,
        {
            "SKILL.md": b"old root\n",
            "sites/removed/SKILL.md": b"removed package file\n",
        },
    )
    user_extra = destination / "sites" / "user-extra.md"
    user_extra.write_bytes(b"user content\n")

    workspace_utils._sync_managed_builtin_skill(source, destination)

    assert (destination / "SKILL.md").read_bytes() == b"new root\n"
    assert (destination / "sites" / "new" / "SKILL.md").read_bytes() == b"new site\n"
    assert not (destination / "sites" / "removed" / "SKILL.md").exists()
    assert user_extra.read_bytes() == b"user content\n"
    assert (destination / MANIFEST_NAME).read_bytes() == expected_manifest


@pytest.mark.parametrize("destination_manifest_version", [None, 0])
def test_missing_or_old_destination_manifest_uses_compatible_overlay_without_deletion(
    tmp_path: Path,
    destination_manifest_version: int | None,
) -> None:
    source = tmp_path / "package" / "opencli-web"
    destination = tmp_path / "workspace" / "opencli-web"
    expected_manifest = _write_manifest_tree(source, {"SKILL.md": b"new root\n"})
    destination.mkdir(parents=True)
    (destination / "SKILL.md").write_bytes(b"old root\n")
    user_extra = destination / "legacy-or-user-extra.md"
    user_extra.write_bytes(b"preserve me\n")
    if destination_manifest_version is not None:
        _write_manifest_tree(
            destination,
            {
                "SKILL.md": b"old root\n",
                "legacy-or-user-extra.md": b"preserve me\n",
            },
            schema_version=destination_manifest_version,
        )

    workspace_utils._sync_managed_builtin_skill(source, destination)

    assert (destination / "SKILL.md").read_bytes() == b"new root\n"
    assert user_extra.read_bytes() == b"preserve me\n"
    assert (destination / MANIFEST_NAME).read_bytes() == expected_manifest


def test_matching_manifests_skip_managed_tree_diff_and_refresh(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    builtin_dir = tmp_path / "builtin"
    user_skills_dir = tmp_path / "user-skills"
    source = builtin_dir / "opencli-web"
    destination = user_skills_dir / "opencli-web"
    manifest_bytes = _write_manifest_tree(source, {"SKILL.md": b"same\n"})
    destination.parent.mkdir(parents=True)
    shutil.copytree(source, destination)
    assert (destination / MANIFEST_NAME).read_bytes() == manifest_bytes
    state_file = user_skills_dir / "skills_state.json"
    state_file.write_text(
        json.dumps(
            {
                "marketplaces": [],
                "installed_plugins": [
                    {"name": "opencli-web", "source": "builtin"},
                ],
                "local_skills": [],
                "skill_configs": {"opencli-web": {"enabled": False}},
            }
        ),
        encoding="utf-8",
    )
    refresh_calls: list[tuple[Path, Path]] = []

    def _record_unexpected_refresh(source_path: Path, destination_path: Path) -> None:
        refresh_calls.append((source_path, destination_path))

    monkeypatch.setattr(
        workspace_utils,
        "_sync_managed_builtin_skill",
        _record_unexpected_refresh,
    )

    workspace_utils._install_default_builtin_skills(
        builtin_dir,
        user_skills_dir,
        overwrite=False,
        cumulative_diff=CopyDiffResult([], [], []),
    )

    assert refresh_calls == []
    state = json.loads(state_file.read_text(encoding="utf-8"))
    assert state["skill_configs"]["opencli-web"]["enabled"] is False


def test_manifest_refresh_preserves_explicit_disabled_state(
    tmp_path: Path,
) -> None:
    builtin_dir = tmp_path / "builtin"
    user_skills_dir = tmp_path / "user-skills"
    source = builtin_dir / "opencli-web"
    destination = user_skills_dir / "opencli-web"
    _write_manifest_tree(source, {"SKILL.md": b"new\n"})
    _write_manifest_tree(destination, {"SKILL.md": b"old\n"})
    state_file = user_skills_dir / "skills_state.json"
    state_file.write_text(
        json.dumps(
            {
                "marketplaces": [],
                "installed_plugins": [
                    {"name": "opencli-web", "source": "builtin"},
                ],
                "local_skills": [],
                "skill_configs": {"opencli-web": {"enabled": False}},
            }
        ),
        encoding="utf-8",
    )

    workspace_utils._install_default_builtin_skills(
        builtin_dir,
        user_skills_dir,
        overwrite=False,
        cumulative_diff=CopyDiffResult([], [], []),
    )

    assert (destination / "SKILL.md").read_bytes() == b"new\n"
    state = json.loads(state_file.read_text(encoding="utf-8"))
    assert state["skill_configs"]["opencli-web"]["enabled"] is False


def test_source_manifest_path_escape_is_rejected_before_destination_changes(
    tmp_path: Path,
) -> None:
    source = tmp_path / "package" / "opencli-web"
    destination = tmp_path / "workspace" / "opencli-web"
    outside = tmp_path / "package" / "outside.md"
    outside.parent.mkdir(parents=True)
    outside.write_bytes(b"outside\n")
    _write_manifest_tree(
        source,
        {},
        manifest_files={"../outside.md": _sha256(b"outside\n")},
    )
    destination.mkdir(parents=True)
    sentinel = destination / "sentinel.md"
    sentinel.write_bytes(b"unchanged\n")

    with pytest.raises(ValueError, match="manifest"):
        workspace_utils._sync_managed_builtin_skill(source, destination)

    assert sentinel.read_bytes() == b"unchanged\n"
    assert outside.read_bytes() == b"outside\n"
    assert not (destination / MANIFEST_NAME).exists()


def test_invalid_old_manifest_never_authorizes_deletion_outside_destination(
    tmp_path: Path,
) -> None:
    source = tmp_path / "package" / "opencli-web"
    destination = tmp_path / "workspace" / "opencli-web"
    expected_manifest = _write_manifest_tree(source, {"SKILL.md": b"new root\n"})
    destination.mkdir(parents=True)
    (destination / "SKILL.md").write_bytes(b"old root\n")
    outside = destination.parent / "outside.md"
    outside.write_bytes(b"must survive\n")
    _write_manifest_tree(
        destination,
        {"SKILL.md": b"old root\n"},
        manifest_files={"../outside.md": _sha256(b"must survive\n")},
    )

    workspace_utils._sync_managed_builtin_skill(source, destination)

    assert outside.read_bytes() == b"must survive\n"
    assert (destination / "SKILL.md").read_bytes() == b"new root\n"
    assert (destination / MANIFEST_NAME).read_bytes() == expected_manifest


def test_source_manifest_hash_mismatch_fails_before_destination_changes(
    tmp_path: Path,
) -> None:
    source = tmp_path / "package" / "opencli-web"
    destination = tmp_path / "workspace" / "opencli-web"
    _write_manifest_tree(
        source,
        {"SKILL.md": b"new root\n"},
        manifest_files={"SKILL.md": "0" * 64},
    )
    destination.mkdir(parents=True)
    destination_file = destination / "SKILL.md"
    destination_file.write_bytes(b"old root\n")

    with pytest.raises(ValueError, match="hash"):
        workspace_utils._sync_managed_builtin_skill(source, destination)

    assert destination_file.read_bytes() == b"old root\n"
    assert not (destination / MANIFEST_NAME).exists()


def test_failed_refresh_keeps_previous_manifest_for_retry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = tmp_path / "package" / "opencli-web"
    destination = tmp_path / "workspace" / "opencli-web"
    _write_manifest_tree(
        source,
        {
            "SKILL.md": b"new root\n",
            "sites/new/SKILL.md": b"new site\n",
        },
    )
    previous_manifest = _write_manifest_tree(
        destination,
        {"SKILL.md": b"old root\n"},
    )
    original_copy2 = workspace_utils.shutil.copy2

    def _fail_on_nested_file(src, dst, *args, **kwargs):
        if Path(src).as_posix().endswith("sites/new/SKILL.md"):
            raise OSError("injected copy failure")
        return original_copy2(src, dst, *args, **kwargs)

    monkeypatch.setattr(workspace_utils.shutil, "copy2", _fail_on_nested_file)

    with pytest.raises(OSError, match="injected copy failure"):
        workspace_utils._sync_managed_builtin_skill(source, destination)

    assert (destination / MANIFEST_NAME).read_bytes() == previous_manifest


@pytest.mark.parametrize(
    ("old_files", "new_files", "expected_path"),
    [
        (
            {"sites/example": b"old file\n"},
            {"sites/example/SKILL.md": b"new nested file\n"},
            "sites/example/SKILL.md",
        ),
        (
            {"sites/example/SKILL.md": b"old nested file\n"},
            {"sites/example": b"new file\n"},
            "sites/example",
        ),
    ],
)
def test_manifest_upgrade_handles_owned_file_directory_transitions(
    tmp_path: Path,
    old_files: dict[str, bytes],
    new_files: dict[str, bytes],
    expected_path: str,
) -> None:
    source = tmp_path / "package" / "opencli-web"
    destination = tmp_path / "workspace" / "opencli-web"
    _write_manifest_tree(source, new_files)
    _write_manifest_tree(destination, old_files)

    workspace_utils._sync_managed_builtin_skill(source, destination)

    assert (destination / expected_path).read_bytes() == next(iter(new_files.values()))
