# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""Session-level record of site-command writes whose outcome is unknown.

A write whose process started but did not exit cleanly may or may not have
taken effect. The record outlives the Browser Agent task that produced it, so
a later task (or the user, on the confirmation bar) is reminded to verify
before the same operation runs again. It never depends on an agent's memory.
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

DEFAULT_RETENTION_S = 24 * 60 * 60
_PREVIEW_LIMIT = 200


@dataclass(frozen=True)
class PendingWrite:
    id: str
    member_id: str
    site: str
    command: str
    args_digest: str
    args_preview: str
    reason: str
    created_at: float

    def public(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "command": f"{self.site}/{self.command}",
            "args": self.args_preview,
            "reason": self.reason,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.created_at)),
        }


def args_digest(args: Mapping[str, Any]) -> str:
    canonical = json.dumps(dict(args), ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def args_preview(args: Mapping[str, Any]) -> str:
    text = ", ".join(f"{key}={value}" for key, value in sorted(dict(args).items()))
    return text if len(text) <= _PREVIEW_LIMIT else text[: _PREVIEW_LIMIT - 1] + "…"


class PendingStore:
    """File-backed store, one JSON file per conversation session."""

    def __init__(self, root: Path, *, retention_s: float = DEFAULT_RETENTION_S) -> None:
        self._root = Path(root)
        self._retention_s = float(retention_s)
        self._lock = threading.Lock()

    def _path(self, session_id: str) -> Path:
        digest = hashlib.sha256(session_id.encode("utf-8")).hexdigest()[:32]
        return self._root / f"{digest}.json"

    def _load(self, session_id: str) -> list[PendingWrite]:
        path = self._path(session_id)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        cutoff = time.time() - self._retention_s
        records: list[PendingWrite] = []
        for raw in payload.get("records") or [] if isinstance(payload, dict) else []:
            try:
                record = PendingWrite(**raw)
            except TypeError:
                continue
            if record.created_at >= cutoff:
                records.append(record)
        return records

    def _save(self, session_id: str, records: list[PendingWrite]) -> None:
        path = self._path(session_id)
        if not records:
            path.unlink(missing_ok=True)
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
        temporary.write_text(
            json.dumps({"version": 1, "records": [asdict(r) for r in records]}, ensure_ascii=False),
            encoding="utf-8",
        )
        os.replace(temporary, path)

    def add(
        self,
        *,
        session_id: str,
        member_id: str,
        site: str,
        command: str,
        args: Mapping[str, Any],
        reason: str,
    ) -> PendingWrite:
        record = PendingWrite(
            id=uuid.uuid4().hex,
            member_id=member_id,
            site=site,
            command=command,
            args_digest=args_digest(args),
            args_preview=args_preview(args),
            reason=reason,
            created_at=time.time(),
        )
        with self._lock:
            records = self._load(session_id)
            records.append(record)
            self._save(session_id, records)
        return record

    def find(self, *, session_id: str, member_id: str, site: str, command: str | None = None) -> list[PendingWrite]:
        with self._lock:
            records = self._load(session_id)
        return [
            record
            for record in records
            if record.member_id == member_id
            and record.site == site
            and (command is None or record.command == command)
        ]

    def clear(self, *, session_id: str, record_ids: list[str]) -> None:
        if not record_ids:
            return
        drop = set(record_ids)
        with self._lock:
            records = [record for record in self._load(session_id) if record.id not in drop]
            self._save(session_id, records)
