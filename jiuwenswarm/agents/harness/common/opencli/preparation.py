# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Fail-closed preparation of Xiaohongshu publish payload snapshots."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_ALLOWED_FIELDS = {
    "title",
    "content",
    "images",
    "card_text",
    "card_style",
    "topics",
    "mode",
    "confirmation",
}
_CONFIRMATION_FIELDS = {"action", "id"}
_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
_FILE_ATTRIBUTE_REPARSE_POINT = 0x400
_COPY_BUFFER_BYTES = 1024 * 1024


class PayloadPreparationError(ValueError):
    """A payload cannot be converted into a trusted immutable snapshot."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True, slots=True)
class PayloadPreparationLimits:
    """Resource limits applied before any OpenCLI process may start."""

    max_payload_bytes: int = 256 * 1024
    max_media_count: int = 9
    max_media_bytes: int = 20 * 1024 * 1024
    max_total_media_bytes: int = 100 * 1024 * 1024

    def __post_init__(self) -> None:
        for field in (
            "max_payload_bytes",
            "max_media_count",
            "max_media_bytes",
            "max_total_media_bytes",
        ):
            value = getattr(self, field)
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise ValueError(f"{field} must be a positive integer")


@dataclass(frozen=True, slots=True)
class PreparedMedia:
    """One reviewed media file copied into the owned staging directory."""

    source_path: Path
    staged_path: Path
    size: int
    sha256: str


@dataclass(frozen=True, slots=True)
class PreparedPayload:
    """A self-contained payload snapshot whose staging can be cleaned safely."""

    payload_path: Path
    staging_directory: Path
    payload_sha256: str
    mode: str
    media: tuple[PreparedMedia, ...]
    _staging_identity: tuple[int, int]

    def verify(self) -> None:
        """Verify that no staged payload or media changed after preparation."""
        _verify_owned_staging(
            self.staging_directory,
            self._staging_identity,
        )
        if _hash_staged_regular_file(self.payload_path) != (self.payload_sha256):
            raise PayloadPreparationError(
                "opencli_prepared_payload_changed",
                "Prepared payload content changed before dispatch",
            )
        for item in self.media:
            if (
                item.staged_path.parent != self.staging_directory
                or _hash_staged_regular_file(item.staged_path) != item.sha256
            ):
                raise PayloadPreparationError(
                    "opencli_prepared_payload_changed",
                    "Prepared media changed before dispatch",
                )

    def cleanup(self) -> None:
        """Remove only the exact staging directory created for this snapshot."""
        try:
            current = self.staging_directory.lstat()
        except FileNotFoundError:
            return
        except OSError as exc:
            raise PayloadPreparationError(
                "opencli_staging_unavailable",
                "Prepared payload staging cannot be inspected for cleanup",
            ) from exc
        if (
            not stat.S_ISDIR(current.st_mode)
            or _is_reparse_point(current)
            or _object_identity(current) != self._staging_identity
        ):
            raise PayloadPreparationError(
                "opencli_staging_changed",
                "Prepared payload staging changed before cleanup",
            )
        try:
            shutil.rmtree(self.staging_directory)
        except OSError as exc:
            raise PayloadPreparationError(
                "opencli_staging_unavailable",
                "Prepared payload staging could not be cleaned",
            ) from exc

    def __enter__(self) -> PreparedPayload:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.cleanup()


@dataclass(frozen=True, slots=True)
class _TrustedFile:
    path: Path
    workspace_root: Path
    initial_stat: os.stat_result
    parent_chain: tuple[tuple[Path, tuple[int, int]], ...]


class _DuplicateJSONKey(ValueError):
    pass


def prepare_xiaohongshu_payload(
    payload_path: str | Path,
    workspace_roots: Sequence[str | Path],
    *,
    staging_root: str | Path | None = None,
    limits: PayloadPreparationLimits | None = None,
) -> PreparedPayload:
    """Validate and snapshot one Xiaohongshu publish payload.

    The returned JSON points only at copied, content-hashed media under a new
    owned staging directory. Neither the original payload nor its media is read
    again by the caller.
    """
    if limits is not None and not isinstance(
        limits,
        PayloadPreparationLimits,
    ):
        raise TypeError("limits must be PayloadPreparationLimits")
    selected_limits = limits or PayloadPreparationLimits()
    roots = _normalize_workspace_roots(workspace_roots)
    trusted_payload = _resolve_trusted_file(
        payload_path,
        base_directory=None,
        workspace_roots=roots,
        error_code="opencli_payload_untrusted",
        label="Payload",
    )
    payload_bytes = _read_trusted_file(
        trusted_payload,
        byte_limit=selected_limits.max_payload_bytes,
        too_large_code="opencli_payload_too_large",
        changed_code="opencli_payload_changed",
        label="Payload",
    )
    raw_payload = _parse_strict_json(payload_bytes)
    normalized, raw_images, mode = _normalize_payload(raw_payload)
    trusted_media = _resolve_media(
        raw_images,
        payload_directory=trusted_payload.path.parent,
        workspace_roots=roots,
        limits=selected_limits,
    )

    owned_staging, staging_identity = _create_owned_staging(staging_root)
    try:
        prepared_media = _stage_media(
            trusted_media,
            owned_staging,
            staging_identity,
            selected_limits,
        )
        if prepared_media:
            normalized["images"] = [str(item.staged_path) for item in prepared_media]
        prepared_payload_bytes = (
            json.dumps(
                normalized,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ).encode("utf-8")
            + b"\n"
        )
        if len(prepared_payload_bytes) > selected_limits.max_payload_bytes:
            raise PayloadPreparationError(
                "opencli_payload_too_large",
                "Prepared payload exceeds the supported size",
            )
        staged_payload_path = owned_staging / "payload.json"
        _write_exclusive(
            staged_payload_path,
            prepared_payload_bytes,
            staging_directory=owned_staging,
            staging_identity=staging_identity,
        )
        prepared = PreparedPayload(
            payload_path=staged_payload_path,
            staging_directory=owned_staging,
            payload_sha256=hashlib.sha256(prepared_payload_bytes).hexdigest(),
            mode=mode,
            media=prepared_media,
            _staging_identity=staging_identity,
        )
        prepared.verify()
        return prepared
    except BaseException:
        _cleanup_owned_staging(
            owned_staging,
            staging_identity,
            suppress_errors=True,
        )
        raise


def _normalize_workspace_roots(
    workspace_roots: Sequence[str | Path],
) -> tuple[Path, ...]:
    if not isinstance(workspace_roots, Sequence) or isinstance(
        workspace_roots,
        (str, bytes, Path),
    ):
        raise PayloadPreparationError(
            "opencli_workspace_unavailable",
            "Trusted workspace roots must be a sequence of directories",
        )
    roots: list[Path] = []
    for raw_root in workspace_roots:
        try:
            root = _absolute_lexical_path(Path(raw_root).expanduser())
            root_stat = root.lstat()
        except (FileNotFoundError, OSError, RuntimeError, TypeError, ValueError):
            continue
        if not stat.S_ISDIR(root_stat.st_mode) or _is_reparse_point(root_stat):
            continue
        try:
            resolved = root.resolve(strict=True)
        except (FileNotFoundError, OSError, RuntimeError, ValueError):
            continue
        if resolved != root:
            continue
        if root not in roots:
            roots.append(root)
    if not roots:
        raise PayloadPreparationError(
            "opencli_workspace_unavailable",
            "No trusted workspace directory is available",
        )
    return tuple(roots)


def _resolve_trusted_file(
    raw_path: str | Path,
    *,
    base_directory: Path | None,
    workspace_roots: Sequence[Path],
    error_code: str,
    label: str,
) -> _TrustedFile:
    try:
        text = os.fspath(raw_path)
    except TypeError as exc:
        raise PayloadPreparationError(
            error_code,
            f"{label} path is invalid",
        ) from exc
    if not isinstance(text, str) or not text.strip() or "\x00" in text:
        raise PayloadPreparationError(
            error_code,
            f"{label} path is invalid",
        )
    supplied = Path(text).expanduser()
    if ".." in supplied.parts:
        raise PayloadPreparationError(
            error_code,
            f"{label} path traversal is not allowed",
        )
    if not supplied.is_absolute():
        if base_directory is None:
            raise PayloadPreparationError(
                error_code,
                f"{label} path must be absolute",
            )
        supplied = base_directory / supplied
    try:
        candidate = _absolute_lexical_path(supplied)
    except (OSError, RuntimeError, ValueError) as exc:
        raise PayloadPreparationError(
            error_code,
            f"{label} path is invalid",
        ) from exc

    workspace_root = next(
        (root for root in workspace_roots if _is_relative_to(candidate, root)),
        None,
    )
    if workspace_root is None:
        raise PayloadPreparationError(
            error_code,
            f"{label} must be inside a trusted workspace",
        )
    try:
        parent_chain = _capture_parent_chain(workspace_root, candidate)
        initial_stat = candidate.lstat()
        resolved = candidate.resolve(strict=True)
    except (FileNotFoundError, OSError, RuntimeError, ValueError) as exc:
        raise PayloadPreparationError(
            error_code,
            f"{label} is unavailable",
        ) from exc
    if (
        resolved != candidate
        or not stat.S_ISREG(initial_stat.st_mode)
        or _is_reparse_point(initial_stat)
    ):
        raise PayloadPreparationError(
            error_code,
            f"{label} must be a non-symlink regular file",
        )
    return _TrustedFile(
        path=candidate,
        workspace_root=workspace_root,
        initial_stat=initial_stat,
        parent_chain=parent_chain,
    )


def _capture_parent_chain(
    workspace_root: Path,
    candidate: Path,
) -> tuple[tuple[Path, tuple[int, int]], ...]:
    relative = candidate.relative_to(workspace_root)
    chain: list[tuple[Path, tuple[int, int]]] = []
    current = workspace_root
    parent_parts = relative.parts[:-1]
    for part in ("", *parent_parts):
        if part:
            current = current / part
        current_stat = current.lstat()
        if not stat.S_ISDIR(current_stat.st_mode) or _is_reparse_point(current_stat):
            raise OSError("trusted path contains a reparse point")
        chain.append((current, _object_identity(current_stat)))
    return tuple(chain)


def _read_trusted_file(
    trusted_file: _TrustedFile,
    *,
    byte_limit: int,
    too_large_code: str,
    changed_code: str,
    label: str,
) -> bytes:
    if trusted_file.initial_stat.st_size > byte_limit:
        raise PayloadPreparationError(
            too_large_code,
            f"{label} exceeds the supported size",
        )
    descriptor = _open_readonly(trusted_file, changed_code, label)
    try:
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(_COPY_BUFFER_BYTES, byte_limit + 1))
            if not chunk:
                break
            total += len(chunk)
            if total > byte_limit:
                raise PayloadPreparationError(
                    too_large_code,
                    f"{label} exceeds the supported size",
                )
            chunks.append(chunk)
        _verify_source_unchanged(
            descriptor,
            trusted_file,
            changed_code,
            label,
        )
        return b"".join(chunks)
    except PayloadPreparationError:
        raise
    except OSError as exc:
        raise PayloadPreparationError(
            changed_code,
            f"{label} changed or became unreadable while being prepared",
        ) from exc
    finally:
        os.close(descriptor)


def _parse_strict_json(content: bytes) -> dict[str, Any]:
    try:
        decoded = content.decode("utf-8")
        value = json.loads(
            decoded,
            object_pairs_hook=_unique_json_object,
            parse_constant=_reject_json_constant,
        )
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise PayloadPreparationError(
            "opencli_payload_invalid",
            "Payload must be strict UTF-8 JSON without duplicate keys",
        ) from exc
    if not isinstance(value, dict):
        raise PayloadPreparationError(
            "opencli_payload_invalid",
            "Payload must be a JSON object",
        )
    return value


def _normalize_payload(
    payload: Mapping[str, Any],
) -> tuple[dict[str, Any], tuple[str, ...], str]:
    unknown = sorted(set(payload).difference(_ALLOWED_FIELDS))
    if unknown:
        raise PayloadPreparationError(
            "opencli_payload_invalid",
            f"Payload has unknown fields: {', '.join(unknown)}",
        )
    title = _required_text(payload, "title")
    if len(title) > 20:
        raise PayloadPreparationError(
            "opencli_payload_invalid",
            "title must contain at most 20 characters",
        )
    content = _required_text(payload, "content")

    has_images = payload.get("images") is not None
    has_card_text = payload.get("card_text") is not None
    if has_images == has_card_text:
        raise PayloadPreparationError(
            "opencli_payload_invalid",
            "Provide exactly one of images or card_text",
        )

    normalized: dict[str, Any] = {
        "title": title,
        "content": content,
    }
    raw_images: tuple[str, ...] = ()
    if has_images:
        raw_images = _string_list(payload["images"], "images")
        if payload.get("card_style") is not None:
            raise PayloadPreparationError(
                "opencli_payload_invalid",
                "card_style is valid only with card_text",
            )
        normalized["images"] = list(raw_images)
    else:
        raw_card_text = payload["card_text"]
        if isinstance(raw_card_text, str):
            card_text: str | list[str] = raw_card_text.strip()
            if not card_text:
                raise PayloadPreparationError(
                    "opencli_payload_invalid",
                    "card_text cannot be empty",
                )
        else:
            cards = _string_list(raw_card_text, "card_text")
            if any("|||" in card for card in cards):
                raise PayloadPreparationError(
                    "opencli_payload_invalid",
                    "card_text entries cannot contain the ||| separator",
                )
            card_text = list(cards)
        normalized["card_text"] = card_text
        raw_style = payload.get("card_style")
        if raw_style is not None:
            if not isinstance(raw_style, str) or not raw_style.strip():
                raise PayloadPreparationError(
                    "opencli_payload_invalid",
                    "card_style must be a non-empty string",
                )
            normalized["card_style"] = raw_style.strip()

    topics = _string_list(
        payload.get("topics", []),
        "topics",
        allow_empty=True,
    )
    if any(not topic or "#" in topic or "," in topic for topic in topics):
        raise PayloadPreparationError(
            "opencli_payload_invalid",
            "topics cannot be empty or contain # or commas",
        )
    normalized["topics"] = list(topics)

    mode = payload.get("mode", "draft")
    if not isinstance(mode, str) or mode not in {"draft", "publish"}:
        raise PayloadPreparationError(
            "opencli_payload_invalid",
            "mode must be draft or publish",
        )
    normalized["mode"] = mode
    confirmation = payload.get("confirmation")
    if mode == "publish":
        normalized["confirmation"] = _normalize_confirmation(confirmation)
    elif confirmation is not None:
        raise PayloadPreparationError(
            "opencli_payload_invalid",
            "confirmation is valid only in publish mode",
        )
    return normalized, raw_images, mode


def _normalize_confirmation(value: Any) -> dict[str, str]:
    if not isinstance(value, dict) or set(value) != _CONFIRMATION_FIELDS:
        raise PayloadPreparationError(
            "opencli_payload_invalid",
            "publish mode requires an exact social_post_confirm confirmation",
        )
    if value["action"] != "social_post_confirm":
        raise PayloadPreparationError(
            "opencli_payload_invalid",
            "confirmation action must be social_post_confirm",
        )
    confirmation_id = value["id"]
    if (
        not isinstance(confirmation_id, str)
        or not confirmation_id.strip()
        or len(confirmation_id.strip()) > 256
    ):
        raise PayloadPreparationError(
            "opencli_payload_invalid",
            "confirmation id must be 1-256 characters",
        )
    return {
        "action": "social_post_confirm",
        "id": confirmation_id.strip(),
    }


def _required_text(payload: Mapping[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise PayloadPreparationError(
            "opencli_payload_invalid",
            f"{field} must be a non-empty string",
        )
    return value.strip()


def _string_list(
    value: Any,
    field: str,
    *,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise PayloadPreparationError(
            "opencli_payload_invalid",
            f"{field} must be a list of strings",
        )
    normalized = tuple(item.strip() for item in value)
    if not allow_empty and (not normalized or any(not item for item in normalized)):
        raise PayloadPreparationError(
            "opencli_payload_invalid",
            f"{field} cannot be empty",
        )
    return normalized


def _resolve_media(
    raw_images: Sequence[str],
    *,
    payload_directory: Path,
    workspace_roots: Sequence[Path],
    limits: PayloadPreparationLimits,
) -> tuple[_TrustedFile, ...]:
    if len(raw_images) > limits.max_media_count:
        raise PayloadPreparationError(
            "opencli_media_invalid",
            (f"images supports at most {limits.max_media_count} paths"),
        )
    trusted: list[_TrustedFile] = []
    seen_paths: set[Path] = set()
    total_size = 0
    for raw_image in raw_images:
        if "," in raw_image or "\x00" in raw_image:
            raise PayloadPreparationError(
                "opencli_media_invalid",
                "Image paths cannot contain commas or NUL characters",
            )
        suffix = Path(raw_image).suffix.lower()
        if suffix not in _IMAGE_SUFFIXES:
            raise PayloadPreparationError(
                "opencli_media_invalid",
                f"Unsupported image extension: {suffix or '(none)'}",
            )
        item = _resolve_trusted_file(
            raw_image,
            base_directory=payload_directory,
            workspace_roots=workspace_roots,
            error_code="opencli_media_untrusted",
            label="Media",
        )
        if item.path in seen_paths:
            raise PayloadPreparationError(
                "opencli_media_invalid",
                "images must not contain duplicate paths",
            )
        seen_paths.add(item.path)
        size = item.initial_stat.st_size
        if size <= 0:
            raise PayloadPreparationError(
                "opencli_media_invalid",
                "Media files cannot be empty",
            )
        if size > limits.max_media_bytes:
            raise PayloadPreparationError(
                "opencli_media_too_large",
                "A media file exceeds the supported size",
            )
        total_size += size
        if total_size > limits.max_total_media_bytes:
            raise PayloadPreparationError(
                "opencli_media_too_large",
                "Combined media exceeds the supported size",
            )
        trusted.append(item)
    return tuple(trusted)


def _stage_media(
    media: Sequence[_TrustedFile],
    staging_directory: Path,
    staging_identity: tuple[int, int],
    limits: PayloadPreparationLimits,
) -> tuple[PreparedMedia, ...]:
    prepared: list[PreparedMedia] = []
    total_size = 0
    for index, source in enumerate(media, start=1):
        suffix = source.path.suffix.lower()
        partial_path = staging_directory / f"media-{index:02d}.partial"
        _verify_owned_staging(staging_directory, staging_identity)
        source_descriptor = _open_readonly(
            source,
            "opencli_media_changed",
            "Media",
        )
        destination_descriptor: int | None = None
        try:
            destination_descriptor = os.open(
                str(partial_path),
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0),
                0o600,
            )
            size, sha256 = _copy_fd_to_destination(
                source_descriptor,
                destination_descriptor,
                byte_limit=limits.max_media_bytes,
            )
            os.fsync(destination_descriptor)
            _verify_source_unchanged(
                source_descriptor,
                source,
                "opencli_media_changed",
                "Media",
            )
        except PayloadPreparationError:
            raise
        except OSError as exc:
            raise PayloadPreparationError(
                "opencli_staging_unavailable",
                "Media could not be copied into trusted staging",
            ) from exc
        finally:
            if destination_descriptor is not None:
                os.close(destination_descriptor)
            os.close(source_descriptor)
        total_size += size
        if total_size > limits.max_total_media_bytes:
            raise PayloadPreparationError(
                "opencli_media_too_large",
                "Combined media exceeds the supported size",
            )
        final_path = staging_directory / f"media-{index:02d}-{sha256[:16]}{suffix}"
        try:
            partial_path.rename(final_path)
        except OSError as exc:
            raise PayloadPreparationError(
                "opencli_staging_unavailable",
                "Staged media could not be finalized",
            ) from exc
        _verify_owned_staging(staging_directory, staging_identity)
        prepared.append(
            PreparedMedia(
                source_path=source.path,
                staged_path=final_path,
                size=size,
                sha256=sha256,
            )
        )
    return tuple(prepared)


def _open_readonly(
    trusted_file: _TrustedFile,
    changed_code: str,
    label: str,
) -> int:
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(str(trusted_file.path), flags)
    except OSError as exc:
        raise PayloadPreparationError(
            changed_code,
            f"{label} changed before it could be opened",
        ) from exc
    try:
        opened_stat = os.fstat(descriptor)
        if (
            not stat.S_ISREG(opened_stat.st_mode)
            or _object_identity(opened_stat)
            != _object_identity(trusted_file.initial_stat)
            or _stat_signature(opened_stat)
            != _stat_signature(trusted_file.initial_stat)
        ):
            raise PayloadPreparationError(
                changed_code,
                f"{label} changed before it could be opened",
            )
    except BaseException:
        os.close(descriptor)
        raise
    return descriptor


def _copy_fd_to_destination(
    source_descriptor: int,
    destination_descriptor: int,
    *,
    byte_limit: int,
) -> tuple[int, str]:
    """Copy one open source descriptor while computing its exact SHA-256."""
    digest = hashlib.sha256()
    total = 0
    while True:
        chunk = os.read(source_descriptor, _COPY_BUFFER_BYTES)
        if not chunk:
            break
        total += len(chunk)
        if total > byte_limit:
            raise PayloadPreparationError(
                "opencli_media_too_large",
                "A media file exceeds the supported size",
            )
        digest.update(chunk)
        view = memoryview(chunk)
        while view:
            written = os.write(destination_descriptor, view)
            if written <= 0:
                raise OSError("staging write made no progress")
            view = view[written:]
    return total, digest.hexdigest()


def _verify_source_unchanged(
    descriptor: int,
    trusted_file: _TrustedFile,
    changed_code: str,
    label: str,
) -> None:
    try:
        descriptor_stat = os.fstat(descriptor)
        path_stat = trusted_file.path.lstat()
        current_chain = _capture_parent_chain(
            trusted_file.workspace_root,
            trusted_file.path,
        )
    except OSError as exc:
        raise PayloadPreparationError(
            changed_code,
            f"{label} changed while it was being prepared",
        ) from exc
    if (
        _stat_signature(descriptor_stat) != _stat_signature(trusted_file.initial_stat)
        or _stat_signature(path_stat) != _stat_signature(trusted_file.initial_stat)
        or current_chain != trusted_file.parent_chain
    ):
        raise PayloadPreparationError(
            changed_code,
            f"{label} changed while it was being prepared",
        )


def _create_owned_staging(
    staging_root: str | Path | None,
) -> tuple[Path, tuple[int, int]]:
    root = (
        Path(tempfile.gettempdir()) / "jiuwenswarm-opencli-staging"
        if staging_root is None
        else Path(staging_root).expanduser()
    )
    if ".." in root.parts:
        raise PayloadPreparationError(
            "opencli_staging_untrusted",
            "Staging root path traversal is not allowed",
        )
    try:
        root = _absolute_lexical_path(root)
        if "," in str(root):
            raise ValueError("staging paths cannot contain commas")
        root_existed = root.exists()
        root.mkdir(mode=0o700, parents=True, exist_ok=True)
        if not root_existed:
            try:
                root.chmod(0o700)
            except OSError:
                pass
        root_stat = root.lstat()
        resolved_root = root.resolve(strict=True)
    except (OSError, RuntimeError, ValueError) as exc:
        raise PayloadPreparationError(
            "opencli_staging_untrusted",
            "Trusted staging root is unavailable",
        ) from exc
    if (
        resolved_root != root
        or not stat.S_ISDIR(root_stat.st_mode)
        or _is_reparse_point(root_stat)
        or not _directory_permissions_trusted(root_stat)
    ):
        raise PayloadPreparationError(
            "opencli_staging_untrusted",
            "Trusted staging root must be a non-symlink directory",
        )
    try:
        staging = Path(
            tempfile.mkdtemp(
                prefix="xiaohongshu-",
                dir=str(root),
            )
        ).resolve(strict=True)
        staging_stat = staging.lstat()
    except (OSError, RuntimeError, ValueError) as exc:
        raise PayloadPreparationError(
            "opencli_staging_unavailable",
            "Owned payload staging could not be created",
        ) from exc
    if (
        staging.parent != root
        or not stat.S_ISDIR(staging_stat.st_mode)
        or _is_reparse_point(staging_stat)
    ):
        _cleanup_owned_staging(
            staging,
            _object_identity(staging_stat),
            suppress_errors=True,
        )
        raise PayloadPreparationError(
            "opencli_staging_untrusted",
            "Owned payload staging is not trustworthy",
        )
    return staging, _object_identity(staging_stat)


def _write_exclusive(
    path: Path,
    content: bytes,
    *,
    staging_directory: Path,
    staging_identity: tuple[int, int],
) -> None:
    descriptor: int | None = None
    try:
        _verify_owned_staging(staging_directory, staging_identity)
        descriptor = os.open(
            str(path),
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0),
            0o600,
        )
        view = memoryview(content)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise OSError("staging write made no progress")
            view = view[written:]
        os.fsync(descriptor)
        _verify_owned_staging(staging_directory, staging_identity)
    except OSError as exc:
        raise PayloadPreparationError(
            "opencli_staging_unavailable",
            "Prepared payload could not be written",
        ) from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _cleanup_owned_staging(
    staging: Path,
    expected_identity: tuple[int, int],
    *,
    suppress_errors: bool,
) -> None:
    try:
        current = staging.lstat()
        if (
            not stat.S_ISDIR(current.st_mode)
            or _is_reparse_point(current)
            or _object_identity(current) != expected_identity
        ):
            raise OSError("owned staging changed")
        shutil.rmtree(staging)
    except FileNotFoundError:
        return
    except OSError:
        if not suppress_errors:
            raise


def _verify_owned_staging(
    staging: Path,
    expected_identity: tuple[int, int],
) -> None:
    try:
        current = staging.lstat()
    except OSError as exc:
        raise PayloadPreparationError(
            "opencli_staging_changed",
            "Owned payload staging changed during preparation",
        ) from exc
    if (
        not stat.S_ISDIR(current.st_mode)
        or _is_reparse_point(current)
        or _object_identity(current) != expected_identity
    ):
        raise PayloadPreparationError(
            "opencli_staging_changed",
            "Owned payload staging changed during preparation",
        )


def _hash_staged_regular_file(path: Path) -> str:
    descriptor: int | None = None
    try:
        path_stat = path.lstat()
        if not stat.S_ISREG(path_stat.st_mode) or _is_reparse_point(path_stat):
            raise OSError("staged path is not a regular file")
        descriptor = os.open(
            str(path),
            os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0),
        )
        opened_stat = os.fstat(descriptor)
        if _stat_signature(opened_stat) != _stat_signature(path_stat):
            raise OSError("staged path changed before it could be opened")
        digest = hashlib.sha256()
        while chunk := os.read(descriptor, _COPY_BUFFER_BYTES):
            digest.update(chunk)
        descriptor_stat = os.fstat(descriptor)
        final_stat = path.lstat()
    except OSError as exc:
        raise PayloadPreparationError(
            "opencli_prepared_payload_changed",
            "Prepared payload staging changed before dispatch",
        ) from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
    if _stat_signature(descriptor_stat) != _stat_signature(
        path_stat
    ) or _stat_signature(final_stat) != _stat_signature(path_stat):
        raise PayloadPreparationError(
            "opencli_prepared_payload_changed",
            "Prepared payload staging changed before dispatch",
        )
    return digest.hexdigest()


def _absolute_lexical_path(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def _is_relative_to(candidate: Path, root: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def _object_identity(value: os.stat_result) -> tuple[int, int]:
    return value.st_dev, value.st_ino


def _stat_signature(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev,
        value.st_ino,
        stat.S_IFMT(value.st_mode),
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
    )


def _is_reparse_point(value: os.stat_result) -> bool:
    if stat.S_ISLNK(value.st_mode):
        return True
    attributes = getattr(value, "st_file_attributes", 0)
    return bool(attributes & _FILE_ATTRIBUTE_REPARSE_POINT)


def _directory_permissions_trusted(value: os.stat_result) -> bool:
    getuid = getattr(os, "getuid", None)
    if not callable(getuid):
        return True
    return value.st_uid == getuid() and value.st_mode & 0o022 == 0


def _unique_json_object(
    pairs: list[tuple[str, Any]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateJSONKey(key)
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise _DuplicateJSONKey(value)


__all__ = [
    "PayloadPreparationError",
    "PayloadPreparationLimits",
    "PreparedMedia",
    "PreparedPayload",
    "prepare_xiaohongshu_payload",
]
