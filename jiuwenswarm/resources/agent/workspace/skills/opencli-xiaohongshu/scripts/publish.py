#!/usr/bin/env python3
"""Guarded OpenCLI wrapper for the Xiaohongshu publish adapter."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
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
_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
_DEFAULT_TIMEOUT_SECONDS = 180.0


class PayloadError(ValueError):
    """A deterministic, pre-execution payload failure."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class PublishRequest:
    title: str
    content: str
    media_option: str
    media_value: str
    card_style: str | None
    topics: tuple[str, ...]
    mode: str
    confirmation_id: str | None


def _bounded(value: str | None, limit: int = 4000) -> str:
    text = (value or "").strip()
    if len(text) <= limit:
        return text
    return f"{text[:limit]}…"


def _emit(payload: dict[str, Any], exit_code: int) -> int:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return exit_code


def _configure_stdout() -> None:
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8", errors="strict")


def _failure(
    *,
    mode: str,
    code: str,
    message: str,
    attempted: bool,
    fallback_allowed: bool,
    exit_code: int = 2,
    detail: str = "",
    result: Any = None,
) -> int:
    error: dict[str, str] = {"code": code, "message": message}
    if detail:
        error["detail"] = _bounded(detail)
    envelope: dict[str, Any] = {
        "ok": False,
        "mode": mode,
        "attempted": attempted,
        "fallback_allowed": fallback_allowed,
        "error": error,
    }
    if result is not None:
        envelope["result"] = result
    return _emit(envelope, exit_code)


def _required_text(payload: dict[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise PayloadError("invalid_payload", f"{field} must be a non-empty string")
    return value.strip()


def _parse_string_list(
    value: Any,
    *,
    field: str,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise PayloadError("invalid_payload", f"{field} must be a list of strings")
    normalized = tuple(item.strip() for item in value)
    if not allow_empty and (not normalized or any(not item for item in normalized)):
        raise PayloadError("invalid_payload", f"{field} cannot be empty")
    return normalized


def _parse_payload(payload: Any) -> PublishRequest:
    if not isinstance(payload, dict):
        raise PayloadError("invalid_payload", "payload must be a JSON object")

    unknown = sorted(set(payload) - _ALLOWED_FIELDS)
    if unknown:
        raise PayloadError(
            "invalid_payload",
            f"unknown payload fields: {', '.join(unknown)}",
        )

    title = _required_text(payload, "title")
    if len(title) > 20:
        raise PayloadError("invalid_payload", "title must contain at most 20 characters")
    content = _required_text(payload, "content")

    has_images = payload.get("images") is not None
    has_card_text = payload.get("card_text") is not None
    if has_images == has_card_text:
        raise PayloadError(
            "invalid_payload",
            "provide exactly one of images or card_text",
        )

    card_style: str | None = None
    if has_images:
        images = _parse_string_list(payload["images"], field="images")
        if len(images) > 9:
            raise PayloadError("invalid_payload", "images supports at most 9 paths")
        for image in images:
            if "," in image:
                raise PayloadError("invalid_payload", "image paths cannot contain commas")
            if Path(image).suffix.lower() not in _IMAGE_SUFFIXES:
                raise PayloadError(
                    "invalid_payload",
                    f"unsupported image extension: {Path(image).suffix or '(none)'}",
                )
        media_option = "--images"
        media_value = ",".join(images)
        if payload.get("card_style") is not None:
            raise PayloadError(
                "invalid_payload",
                "card_style is valid only with card_text",
            )
    else:
        raw_card_text = payload["card_text"]
        if isinstance(raw_card_text, str):
            media_value = raw_card_text.strip()
            if not media_value:
                raise PayloadError("invalid_payload", "card_text cannot be empty")
        else:
            cards = _parse_string_list(raw_card_text, field="card_text")
            if any("|||" in card for card in cards):
                raise PayloadError(
                    "invalid_payload",
                    "card_text list entries cannot contain the ||| separator",
                )
            media_value = "|||".join(cards)
        media_option = "--card-text"
        raw_style = payload.get("card_style")
        if raw_style is not None:
            if not isinstance(raw_style, str) or not raw_style.strip():
                raise PayloadError(
                    "invalid_payload",
                    "card_style must be a non-empty string",
                )
            card_style = raw_style.strip()

    raw_topics = payload.get("topics", [])
    topics = _parse_string_list(
        raw_topics,
        field="topics",
        allow_empty=True,
    )
    for topic in topics:
        if not topic or "#" in topic or "," in topic:
            raise PayloadError(
                "invalid_payload",
                "topics cannot be empty or contain # or commas",
            )

    mode = payload.get("mode", "draft")
    if mode not in {"draft", "publish"}:
        raise PayloadError("invalid_payload", "mode must be draft or publish")

    confirmation = payload.get("confirmation")
    confirmation_id: str | None = None
    if mode == "publish":
        if not isinstance(confirmation, dict):
            raise PayloadError(
                "confirmation_required",
                "publish mode requires a social_post_confirm confirmation",
            )
        if confirmation.get("action") != "social_post_confirm":
            raise PayloadError(
                "confirmation_required",
                "confirmation action must be social_post_confirm",
            )
        raw_confirmation_id = confirmation.get("id")
        if (
            not isinstance(raw_confirmation_id, str)
            or not raw_confirmation_id.strip()
            or len(raw_confirmation_id.strip()) > 256
        ):
            raise PayloadError(
                "confirmation_required",
                "confirmation id must be a non-empty string of at most 256 characters",
            )
        confirmation_id = raw_confirmation_id.strip()
    elif confirmation is not None:
        raise PayloadError(
            "invalid_payload",
            "confirmation is valid only in publish mode",
        )

    return PublishRequest(
        title=title,
        content=content,
        media_option=media_option,
        media_value=media_value,
        card_style=card_style,
        topics=topics,
        mode=mode,
        confirmation_id=confirmation_id,
    )


def _load_payload(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PayloadError("payload_not_found", "payload file does not exist") from exc
    except (OSError, UnicodeError) as exc:
        raise PayloadError("payload_unreadable", "payload file could not be read") from exc
    except json.JSONDecodeError as exc:
        raise PayloadError("invalid_json", "payload is not valid JSON") from exc


def _resolve_opencli_argv(executable: str) -> list[str]:
    resolved = shutil.which(executable)
    if resolved is None:
        candidate = Path(executable)
        if candidate.is_file():
            resolved = str(candidate.resolve())
    if resolved is None:
        raise FileNotFoundError(executable)

    resolved_path = Path(resolved)
    if os.name == "nt" and resolved_path.suffix.lower() in {".cmd", ".bat"}:
        opencli_main = (
            resolved_path.parent
            / "node_modules"
            / "@jackwener"
            / "opencli"
            / "dist"
            / "src"
            / "main.js"
        )
        local_node = resolved_path.parent / "node.exe"
        node = str(local_node) if local_node.is_file() else shutil.which("node")
        if not node or not opencli_main.is_file():
            raise PayloadError(
                "unsupported_opencli_launcher",
                "the Windows OpenCLI launcher could not be resolved without a shell",
            )
        return [node, str(opencli_main)]

    if os.name == "nt" and resolved_path.suffix.lower() == ".ps1":
        raise PayloadError(
            "unsupported_opencli_launcher",
            "PowerShell launchers are not supported by the shell-free wrapper",
        )
    return [str(resolved_path)]


def _build_adapter_args(request: PublishRequest) -> list[str]:
    args = [
        "xiaohongshu",
        "publish",
        request.content,
        "--title",
        request.title,
        request.media_option,
        request.media_value,
    ]
    if request.card_style:
        args.extend(["--card-style", request.card_style])
    if request.topics:
        args.extend(["--topics", ",".join(request.topics)])
    args.extend(
        [
            "--draft",
            "true" if request.mode == "draft" else "false",
            "-f",
            "json",
        ]
    )
    return args


def _default_confirmation_dir() -> Path:
    configured = os.environ.get("JIUWENSWARM_OPENCLI_CONFIRMATION_DIR", "").strip()
    if configured:
        return Path(configured).expanduser()
    return (
        Path.home()
        / ".jiuwenswarm"
        / "agent"
        / "workspace"
        / ".opencli-confirmations"
    )


def _consume_confirmation(confirmation_id: str, confirmation_dir: Path) -> None:
    digest = hashlib.sha256(confirmation_id.encode("utf-8")).hexdigest()
    confirmation_dir.mkdir(parents=True, exist_ok=True)
    marker = confirmation_dir / f"{digest}.json"
    try:
        descriptor = os.open(
            str(marker),
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o600,
        )
    except FileExistsError as exc:
        raise PayloadError(
            "confirmation_already_used",
            "this confirmation id has already been consumed",
        ) from exc
    except OSError as exc:
        raise PayloadError(
            "confirmation_state_unavailable",
            "confirmation state could not be persisted safely",
        ) from exc

    with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(
            {
                "confirmation_id_sha256": digest,
                "consumed_at": datetime.now(timezone.utc).isoformat(),
            },
            handle,
            ensure_ascii=True,
            sort_keys=True,
        )
        handle.write("\n")


def _parse_child_output(stdout: str | None) -> Any:
    value = (stdout or "").strip()
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {"raw": _bounded(value)}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the guarded OpenCLI Xiaohongshu publish adapter.",
    )
    parser.add_argument("--payload", required=True, type=Path)
    parser.add_argument(
        "--opencli-bin",
        default=os.environ.get("OPENCLI_BIN", "opencli"),
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--opencli-prefix-arg",
        action="append",
        default=[],
        help=argparse.SUPPRESS,
    )
    parser.add_argument("--confirmation-dir", type=Path)
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=_DEFAULT_TIMEOUT_SECONDS,
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    _configure_stdout()
    args = _build_parser().parse_args(argv)
    mode = "unknown"
    try:
        request = _parse_payload(_load_payload(args.payload))
        mode = request.mode
        if not 1 <= args.timeout_seconds <= 600:
            raise PayloadError(
                "invalid_timeout",
                "timeout-seconds must be between 1 and 600",
            )
        runner = _resolve_opencli_argv(args.opencli_bin)
    except FileNotFoundError:
        return _failure(
            mode=mode,
            code="opencli_not_found",
            message="OpenCLI executable was not found",
            attempted=False,
            fallback_allowed=True,
        )
    except PayloadError as exc:
        return _failure(
            mode=mode,
            code=exc.code,
            message=str(exc),
            attempted=False,
            fallback_allowed=False,
        )

    if request.mode == "publish":
        assert request.confirmation_id is not None
        try:
            _consume_confirmation(
                request.confirmation_id,
                args.confirmation_dir or _default_confirmation_dir(),
            )
        except PayloadError as exc:
            return _failure(
                mode=request.mode,
                code=exc.code,
                message=str(exc),
                attempted=False,
                fallback_allowed=False,
            )

    command = [
        *runner,
        *args.opencli_prefix_arg,
        *_build_adapter_args(request),
    ]
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=args.timeout_seconds,
            shell=False,
        )
    except FileNotFoundError:
        return _failure(
            mode=request.mode,
            code="opencli_start_failed",
            message="OpenCLI disappeared before process start",
            attempted=False,
            fallback_allowed=request.mode == "draft",
        )
    except subprocess.TimeoutExpired as exc:
        return _failure(
            mode=request.mode,
            code="opencli_timeout",
            message="OpenCLI timed out after the process started",
            attempted=True,
            fallback_allowed=False,
            exit_code=124,
            detail=exc.stderr or "",
        )
    except OSError as exc:
        return _failure(
            mode=request.mode,
            code="opencli_start_failed",
            message="OpenCLI could not be started",
            attempted=False,
            fallback_allowed=request.mode == "draft",
            detail=str(exc),
        )

    result = _parse_child_output(completed.stdout)
    if completed.returncode != 0:
        child_exit = (
            completed.returncode
            if 1 <= completed.returncode <= 255
            else 1
        )
        return _failure(
            mode=request.mode,
            code="opencli_failed",
            message="OpenCLI returned a non-zero exit code after process start",
            attempted=True,
            fallback_allowed=False,
            exit_code=child_exit,
            detail=completed.stderr or "",
            result=result,
        )

    return _emit(
        {
            "ok": True,
            "mode": request.mode,
            "attempted": True,
            "fallback_allowed": False,
            "result": result,
        },
        0,
    )


if __name__ == "__main__":
    raise SystemExit(main())
