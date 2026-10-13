# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""Session-level pending writes survive tasks and expire after the retention window."""

from __future__ import annotations

import time
from pathlib import Path

from jiuwenswarm.extensions.opencli.pending import DEFAULT_RETENTION_S, PendingStore


def test_records_persist_per_session_and_member(tmp_path: Path) -> None:
    store = PendingStore(tmp_path)
    record = store.add(session_id="s", member_id="m", site="demo", command="follow",
                       args={"uid": "1"}, reason="timeout")
    reopened = PendingStore(tmp_path)
    assert [r.id for r in reopened.find(session_id="s", member_id="m", site="demo")] == [record.id]
    assert reopened.find(session_id="s", member_id="other", site="demo") == []
    assert reopened.find(session_id="other", member_id="m", site="demo") == []
    assert reopened.find(session_id="s", member_id="m", site="demo", command="like") == []
    assert record.public()["args"] == "uid=1"
    reopened.clear(session_id="s", record_ids=[record.id])
    assert store.find(session_id="s", member_id="m", site="demo") == []
    assert not list(tmp_path.glob("*.json"))


def test_records_expire_after_retention(tmp_path: Path, monkeypatch) -> None:
    assert DEFAULT_RETENTION_S == 24 * 60 * 60
    store = PendingStore(tmp_path, retention_s=60)
    store.add(session_id="s", member_id="", site="demo", command="follow", args={}, reason="error")
    later = time.time() + 120
    monkeypatch.setattr(time, "time", lambda: later)
    assert store.find(session_id="s", member_id="", site="demo") == []
