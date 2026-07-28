# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Tests for managed team Skill copies used when directory links are unavailable."""

from __future__ import annotations

import errno
import json
from pathlib import Path

import pytest

from jiuwenswarm.agents.harness.team import team_skill_links

MARKER_NAME = ".jiuwenswarm-managed-skill-copy.json"


def _create_skill(root: Path, name: str, content: str = "initial\n") -> Path:
    skill_dir = root / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\n---\n{content}",
        encoding="utf-8",
    )
    (skill_dir / "obsolete.txt").write_text("old\n", encoding="utf-8")
    return skill_dir


def _deny_symlink(*args, **kwargs) -> None:
    raise OSError(errno.EPERM, "symlink unavailable")


def test_copy_fallback_writes_marker_and_refreshes_from_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_root = tmp_path / "global"
    target_root = tmp_path / "team" / "skills"
    source = _create_skill(source_root, "skill-a")
    target = target_root / "skill-a"
    monkeypatch.setattr(team_skill_links.os, "symlink", _deny_symlink)

    team_skill_links.link_skill_dir(source, target)

    marker = target / MARKER_NAME
    marker_payload = json.loads(marker.read_text(encoding="utf-8"))
    assert marker_payload == {
        "schema_version": 1,
        "source": str(source.resolve()),
        "target": str(target.resolve()),
    }
    assert not target.is_symlink()

    (source / "SKILL.md").write_text(
        "---\nname: skill-a\n---\nupdated\n",
        encoding="utf-8",
    )
    (source / "obsolete.txt").unlink()
    (source / "new.txt").write_text("new\n", encoding="utf-8")

    team_skill_links.sync_skill_dir_links(source_root, target_root)

    assert "updated" in (target / "SKILL.md").read_text(encoding="utf-8")
    assert not (target / "obsolete.txt").exists()
    assert (target / "new.txt").read_text(encoding="utf-8") == "new\n"
    assert marker.is_file()


def test_prune_removes_stale_managed_copy_but_never_unmarked_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_root = tmp_path / "global"
    target_root = tmp_path / "team" / "skills"
    source = _create_skill(source_root, "managed")
    managed_target = target_root / "managed"
    ordinary_target = target_root / "ordinary"
    ordinary_target.mkdir(parents=True)
    (ordinary_target / "SKILL.md").write_text(
        "---\nname: ordinary\n---\nuser content\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(team_skill_links.os, "symlink", _deny_symlink)
    team_skill_links.link_skill_dir(source, managed_target)

    for path in sorted(source.rglob("*"), reverse=True):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            path.rmdir()
    source.rmdir()

    team_skill_links.prune_skill_dir_links(source_root, target_root)

    assert not managed_target.exists()
    assert ordinary_target.is_dir()
    assert (ordinary_target / "SKILL.md").is_file()


def test_remove_skill_dir_link_removes_only_valid_managed_copy(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = _create_skill(tmp_path / "global", "managed")
    managed_target = tmp_path / "team" / "managed"
    ordinary_target = tmp_path / "team" / "ordinary"
    ordinary_target.mkdir(parents=True)
    (ordinary_target / "SKILL.md").write_text(
        "---\nname: ordinary\n---\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(team_skill_links.os, "symlink", _deny_symlink)
    team_skill_links.link_skill_dir(source, managed_target)

    team_skill_links.remove_skill_dir_link(managed_target)
    team_skill_links.remove_skill_dir_link(ordinary_target)

    assert not managed_target.exists()
    assert ordinary_target.is_dir()


def test_mismatched_marker_does_not_authorize_refresh_or_deletion(
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "global"
    target_root = tmp_path / "team" / "skills"
    source = _create_skill(source_root, "skill-a", content="source\n")
    target = _create_skill(target_root, "skill-a", content="user\n")
    marker = target / MARKER_NAME
    marker.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "source": str((tmp_path / "different-source").resolve()),
                "target": str(target.resolve()),
            }
        ),
        encoding="utf-8",
    )

    team_skill_links.sync_skill_dir_links(source_root, target_root)

    assert "user" in (target / "SKILL.md").read_text(encoding="utf-8")
    assert source.is_dir()


def test_refresh_copy_failure_preserves_previous_managed_copy(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_root = tmp_path / "global"
    target_root = tmp_path / "team" / "skills"
    source = _create_skill(source_root, "skill-a", content="old\n")
    target = target_root / "skill-a"
    monkeypatch.setattr(team_skill_links.os, "symlink", _deny_symlink)
    team_skill_links.link_skill_dir(source, target)
    (source / "SKILL.md").write_text(
        "---\nname: skill-a\n---\nnew\n",
        encoding="utf-8",
    )

    def _fail_copy(*args, **kwargs):
        raise OSError("injected copy failure")

    monkeypatch.setattr(team_skill_links.shutil, "copytree", _fail_copy)

    with pytest.raises(OSError, match="injected copy failure"):
        team_skill_links.sync_skill_dir_links(source_root, target_root)

    assert "old" in (target / "SKILL.md").read_text(encoding="utf-8")
    assert (target / MARKER_NAME).is_file()
