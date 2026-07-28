from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import pytest

from jiuwenswarm.agents.harness.common.opencli import preparation
from jiuwenswarm.agents.harness.common.opencli.preparation import (
    PayloadPreparationError,
    PayloadPreparationLimits,
    prepare_xiaohongshu_payload,
)


def _write_payload(
    workspace: Path,
    payload: object,
    *,
    name: str = "payload.json",
) -> Path:
    path = workspace / name
    path.write_text(
        json.dumps(payload, ensure_ascii=False),
        encoding="utf-8",
    )
    return path


def _draft_payload(image: Path | str) -> dict[str, object]:
    return {
        "title": "安全草稿",
        "content": "准备后只能读取 staging 快照。",
        "images": [str(image)],
        "topics": ["OpenCLI", "OpenJiuwen"],
    }


def _assert_error(
    expected_code: str,
    payload_path: Path,
    workspace: Path,
    staging_root: Path,
    *,
    limits: PayloadPreparationLimits | None = None,
) -> None:
    with pytest.raises(PayloadPreparationError) as raised:
        prepare_xiaohongshu_payload(
            payload_path,
            [workspace],
            staging_root=staging_root,
            limits=limits,
        )
    assert raised.value.code == expected_code


def _simulate_reparse_point(
    path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    marked = path.lstat()
    marked_identity = marked.st_dev, marked.st_ino
    original = preparation._is_reparse_point

    def is_reparse(value: os.stat_result) -> bool:
        identity = value.st_dev, value.st_ino
        return identity == marked_identity or original(value)

    monkeypatch.setattr(preparation, "_is_reparse_point", is_reparse)


def test_image_draft_is_snapshotted_hashed_and_cleanable(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    image = workspace / "cover.PNG"
    image.write_bytes(b"reviewed-image")
    payload_path = _write_payload(workspace, _draft_payload(image))
    staging_root = tmp_path / "trusted-staging"

    with prepare_xiaohongshu_payload(
        payload_path,
        [workspace],
        staging_root=staging_root,
    ) as prepared:
        assert prepared.mode == "draft"
        assert prepared.payload_path.parent == prepared.staging_directory
        assert prepared.staging_directory.parent == staging_root.resolve()
        assert len(prepared.media) == 1

        staged_media = prepared.media[0]
        assert staged_media.source_path == image.resolve()
        assert staged_media.staged_path.parent == prepared.staging_directory
        assert staged_media.staged_path.suffix == ".png"
        assert staged_media.size == len(b"reviewed-image")
        assert staged_media.sha256 == hashlib.sha256(b"reviewed-image").hexdigest()

        staged_payload_bytes = prepared.payload_path.read_bytes()
        assert (
            prepared.payload_sha256 == hashlib.sha256(staged_payload_bytes).hexdigest()
        )
        staged_payload = json.loads(staged_payload_bytes)
        assert staged_payload["mode"] == "draft"
        assert staged_payload["images"] == [str(staged_media.staged_path)]
        assert staged_payload["title"] == "安全草稿"

        image.write_bytes(b"changed-after-preparation")
        payload_path.write_text("{}", encoding="utf-8")
        assert staged_media.staged_path.read_bytes() == b"reviewed-image"
        staging_directory = prepared.staging_directory

    assert not staging_directory.exists()


def test_publish_card_payload_is_normalized_without_media_copy(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    payload_path = _write_payload(
        workspace,
        {
            "title": "  发布确认  ",
            "content": "  用户确认后的正文  ",
            "card_text": [" 第一张 ", "第二张"],
            "card_style": " clean ",
            "topics": [" 测试 "],
            "mode": "publish",
            "confirmation": {
                "action": "social_post_confirm",
                "id": " confirm-123 ",
            },
        },
    )

    prepared = prepare_xiaohongshu_payload(
        payload_path,
        [workspace],
        staging_root=tmp_path / "trusted-staging",
    )
    try:
        assert prepared.mode == "publish"
        assert prepared.media == ()
        staged = json.loads(prepared.payload_path.read_text(encoding="utf-8"))
        assert staged == {
            "title": "发布确认",
            "content": "用户确认后的正文",
            "card_text": ["第一张", "第二张"],
            "card_style": "clean",
            "topics": ["测试"],
            "mode": "publish",
            "confirmation": {
                "action": "social_post_confirm",
                "id": "confirm-123",
            },
        }
    finally:
        prepared.cleanup()
        prepared.cleanup()
    assert not prepared.staging_directory.exists()


def test_prepared_payload_verify_rejects_staging_mutation(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    image = workspace / "cover.png"
    image.write_bytes(b"reviewed-image")
    payload_path = _write_payload(workspace, _draft_payload(image))
    prepared = prepare_xiaohongshu_payload(
        payload_path,
        [workspace],
        staging_root=tmp_path / "trusted-staging",
    )
    try:
        prepared.verify()
        prepared.media[0].staged_path.write_bytes(b"tampered-image")
        with pytest.raises(PayloadPreparationError) as raised:
            prepared.verify()
        assert raised.value.code == "opencli_prepared_payload_changed"
    finally:
        prepared.cleanup()


@pytest.mark.parametrize(
    ("content", "expected_code"),
    [
        (b"[]", "opencli_payload_invalid"),
        (b'{"title":"a","title":"b"}', "opencli_payload_invalid"),
        (
            b'{"confirmation":{"id":"a","id":"b"}}',
            "opencli_payload_invalid",
        ),
        (b'{"value":NaN}', "opencli_payload_invalid"),
        (b"\xff\xfe", "opencli_payload_invalid"),
    ],
)
def test_payload_requires_strict_utf8_json_object(
    tmp_path: Path,
    content: bytes,
    expected_code: str,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    payload_path = workspace / "payload.json"
    payload_path.write_bytes(content)

    _assert_error(
        expected_code,
        payload_path,
        workspace,
        tmp_path / "trusted-staging",
    )


def test_payload_size_limit_is_enforced_before_json_parse(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    payload_path = workspace / "payload.json"
    payload_path.write_bytes(b"{" + (b" " * 64) + b"}")

    _assert_error(
        "opencli_payload_too_large",
        payload_path,
        workspace,
        tmp_path / "trusted-staging",
        limits=PayloadPreparationLimits(max_payload_bytes=32),
    )


@pytest.mark.parametrize(
    "payload",
    [
        {
            "title": "draft",
            "content": "body",
            "card_text": "card",
            "unexpected": True,
        },
        {
            "title": "draft",
            "content": "body",
            "images": ["ignored.png"],
            "card_text": "card",
        },
        {
            "title": "draft",
            "content": "body",
            "card_text": "card",
            "mode": "preview",
        },
        {
            "title": "draft",
            "content": "body",
            "card_text": "card",
            "confirmation": {
                "action": "social_post_confirm",
                "id": "draft-confirm",
            },
        },
        {
            "title": "publish",
            "content": "body",
            "card_text": "card",
            "mode": "publish",
        },
        {
            "title": "publish",
            "content": "body",
            "card_text": "card",
            "mode": "publish",
            "confirmation": {
                "action": "social_post_confirm",
                "id": "confirm",
                "extra": "not-allowed",
            },
        },
    ],
)
def test_payload_schema_and_mode_fail_closed(
    tmp_path: Path,
    payload: dict[str, object],
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    payload_path = _write_payload(workspace, payload)

    _assert_error(
        "opencli_payload_invalid",
        payload_path,
        workspace,
        tmp_path / "trusted-staging",
    )


def test_payload_file_must_be_regular_and_inside_workspace(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    outside = tmp_path / "outside.json"
    outside.write_text("{}", encoding="utf-8")
    staging_root = tmp_path / "trusted-staging"

    _assert_error(
        "opencli_payload_untrusted",
        outside,
        workspace,
        staging_root,
    )
    _assert_error(
        "opencli_payload_untrusted",
        workspace,
        workspace,
        staging_root,
    )


def test_payload_file_symlink_is_rejected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    staging_root = tmp_path / "trusted-staging"
    target = _write_payload(
        workspace,
        {
            "title": "draft",
            "content": "body",
            "card_text": "card",
        },
        name="target.json",
    )
    link = workspace / "payload.json"
    try:
        link.symlink_to(target)
    except OSError:
        link.write_bytes(target.read_bytes())
        _simulate_reparse_point(link, monkeypatch)
    _assert_error(
        "opencli_payload_untrusted",
        link,
        workspace,
        staging_root,
    )


@pytest.mark.parametrize(
    ("filename", "content", "expected_code"),
    [
        ("image.bmp", b"bmp", "opencli_media_invalid"),
        ("image.png", b"", "opencli_media_invalid"),
        ("folder.png", None, "opencli_media_untrusted"),
    ],
)
def test_media_requires_supported_nonempty_regular_file(
    tmp_path: Path,
    filename: str,
    content: bytes | None,
    expected_code: str,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    media = workspace / filename
    if content is None:
        media.mkdir()
    else:
        media.write_bytes(content)
    payload_path = _write_payload(workspace, _draft_payload(media))

    _assert_error(
        expected_code,
        payload_path,
        workspace,
        tmp_path / "trusted-staging",
    )


def test_media_must_stay_inside_workspace(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    outside = tmp_path / "outside.png"
    outside.write_bytes(b"outside")
    staging_root = tmp_path / "trusted-staging"

    outside_payload = _write_payload(workspace, _draft_payload(outside))
    _assert_error(
        "opencli_media_untrusted",
        outside_payload,
        workspace,
        staging_root,
    )


def test_media_leaf_symlink_is_rejected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    outside = tmp_path / "outside.png"
    outside.write_bytes(b"outside")
    staging_root = tmp_path / "trusted-staging"
    link = workspace / "linked.png"
    try:
        link.symlink_to(outside)
    except OSError:
        link.write_bytes(outside.read_bytes())
        _simulate_reparse_point(link, monkeypatch)
    linked_payload = _write_payload(
        workspace,
        _draft_payload(link),
        name="linked-payload.json",
    )
    _assert_error(
        "opencli_media_untrusted",
        linked_payload,
        workspace,
        staging_root,
    )


def test_media_parent_symlink_is_rejected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    staging_root = tmp_path / "trusted-staging"
    real_directory = workspace / "real"
    real_directory.mkdir()
    nested_media = real_directory / "nested.png"
    nested_media.write_bytes(b"nested")
    linked_directory = workspace / "linked-directory"
    try:
        linked_directory.symlink_to(real_directory, target_is_directory=True)
    except OSError:
        linked_directory.mkdir()
        (linked_directory / "nested.png").write_bytes(b"nested")
        _simulate_reparse_point(linked_directory, monkeypatch)
    parent_link_payload = _write_payload(
        workspace,
        _draft_payload(linked_directory / "nested.png"),
        name="parent-link-payload.json",
    )
    _assert_error(
        "opencli_media_untrusted",
        parent_link_payload,
        workspace,
        staging_root,
    )


def test_media_count_individual_and_total_size_limits(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    images: list[Path] = []
    for index in range(3):
        image = workspace / f"{index}.png"
        image.write_bytes(b"x" * 5)
        images.append(image)
    staging_root = tmp_path / "trusted-staging"

    too_many = _write_payload(
        workspace,
        _draft_payload(images[0]) | {"images": [str(path) for path in images]},
        name="too-many.json",
    )
    _assert_error(
        "opencli_media_invalid",
        too_many,
        workspace,
        staging_root,
        limits=PayloadPreparationLimits(max_media_count=2),
    )

    too_large = _write_payload(
        workspace,
        _draft_payload(images[0]),
        name="too-large.json",
    )
    _assert_error(
        "opencli_media_too_large",
        too_large,
        workspace,
        staging_root,
        limits=PayloadPreparationLimits(max_media_bytes=4),
    )

    total_too_large = _write_payload(
        workspace,
        _draft_payload(images[0]) | {"images": [str(images[0]), str(images[1])]},
        name="total-too-large.json",
    )
    _assert_error(
        "opencli_media_too_large",
        total_too_large,
        workspace,
        staging_root,
        limits=PayloadPreparationLimits(
            max_media_bytes=8,
            max_total_media_bytes=8,
        ),
    )


def test_source_mutation_during_copy_is_rejected_and_staging_removed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    image = workspace / "cover.png"
    image.write_bytes(b"initial-image")
    payload_path = _write_payload(workspace, _draft_payload(image))
    staging_root = tmp_path / "trusted-staging"
    original_copy = preparation._copy_fd_to_destination

    def racing_copy(
        source_descriptor: int,
        destination_descriptor: int,
        *,
        byte_limit: int,
    ) -> tuple[int, str]:
        copied = original_copy(
            source_descriptor,
            destination_descriptor,
            byte_limit=byte_limit,
        )
        image.write_bytes(b"mutated-during-copy")
        return copied

    monkeypatch.setattr(
        preparation,
        "_copy_fd_to_destination",
        racing_copy,
    )

    _assert_error(
        "opencli_media_changed",
        payload_path,
        workspace,
        staging_root,
    )
    assert not staging_root.exists() or list(staging_root.iterdir()) == []


def test_payload_mutation_during_read_is_rejected_before_staging(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    payload_path = _write_payload(
        workspace,
        {
            "title": "draft",
            "content": "body",
            "card_text": "card",
        },
    )
    staging_root = tmp_path / "trusted-staging"
    original_read = preparation.os.read
    mutated = False

    def racing_read(descriptor: int, count: int) -> bytes:
        nonlocal mutated
        chunk = original_read(descriptor, count)
        if not mutated:
            mutated = True
            payload_path.write_bytes(payload_path.read_bytes() + b" ")
        return chunk

    monkeypatch.setattr(preparation.os, "read", racing_read)

    _assert_error(
        "opencli_payload_changed",
        payload_path,
        workspace,
        staging_root,
    )
    assert not staging_root.exists()


def test_staging_root_cannot_be_a_symlink(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    image = workspace / "cover.png"
    image.write_bytes(b"image")
    payload_path = _write_payload(workspace, _draft_payload(image))
    real_staging = tmp_path / "real-staging"
    real_staging.mkdir()
    staging_link = tmp_path / "staging-link"
    try:
        staging_link.symlink_to(real_staging, target_is_directory=True)
    except OSError:
        staging_link.mkdir()
        _simulate_reparse_point(staging_link, monkeypatch)

    _assert_error(
        "opencli_staging_untrusted",
        payload_path,
        workspace,
        staging_link,
    )
    assert list(real_staging.iterdir()) == []
