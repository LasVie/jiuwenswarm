# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Short-lived, one-use receipts for OpenCLI operation disclosure."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True, slots=True)
class DisclosureReceiptResult:
    """Result of atomically consuming a disclosure receipt."""

    accepted: bool
    code: str


@dataclass(frozen=True, slots=True)
class _DisclosureReceipt:
    operation_sha256: str
    expires_at: float


class DisclosureReceiptStore:
    """Thread-safe in-memory receipt store that fails closed after restart."""

    def __init__(
        self,
        *,
        ttl_seconds: float = 300.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self._ttl_seconds = float(ttl_seconds)
        self._clock = clock
        self._receipts: dict[tuple[str, str, str], _DisclosureReceipt] = {}
        self._lock = threading.RLock()

    def grant(
        self,
        *,
        scope: str,
        site: str,
        operation: str,
        operation_sha256: str,
    ) -> None:
        """Issue or replace one receipt for a trusted Agent execution scope."""
        now = self._clock()
        key = (scope, site, operation)
        with self._lock:
            self._prune_expired(now)
            self._receipts[key] = _DisclosureReceipt(
                operation_sha256=operation_sha256,
                expires_at=now + self._ttl_seconds,
            )

    def consume(
        self,
        *,
        scope: str,
        site: str,
        operation: str,
        operation_sha256: str,
    ) -> DisclosureReceiptResult:
        """Atomically validate and consume a matching receipt."""
        now = self._clock()
        key = (scope, site, operation)
        with self._lock:
            receipt = self._receipts.get(key)
            if receipt is None:
                self._prune_expired(now)
                return DisclosureReceiptResult(False, "opencli_disclosure_required")
            if receipt.expires_at <= now:
                self._receipts.pop(key, None)
                self._prune_expired(now)
                return DisclosureReceiptResult(False, "opencli_disclosure_expired")
            if receipt.operation_sha256 != operation_sha256:
                self._receipts.pop(key, None)
                return DisclosureReceiptResult(False, "opencli_disclosure_changed")
            self._receipts.pop(key, None)
            self._prune_expired(now)
            return DisclosureReceiptResult(True, "ok")

    def clear(self) -> None:
        """Clear all receipts. Intended for lifecycle cleanup and tests."""
        with self._lock:
            self._receipts.clear()

    def _prune_expired(self, now: float) -> None:
        expired = [
            key
            for key, receipt in self._receipts.items()
            if receipt.expires_at <= now
        ]
        for key in expired:
            self._receipts.pop(key, None)


_OPENCLI_DISCLOSURE_STORE = DisclosureReceiptStore()


def get_opencli_disclosure_store() -> DisclosureReceiptStore:
    """Return the process-local store shared by tool and rail providers."""
    return _OPENCLI_DISCLOSURE_STORE


__all__ = [
    "DisclosureReceiptResult",
    "DisclosureReceiptStore",
    "get_opencli_disclosure_store",
]
