# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Short-lived, one-use receipts for OpenCLI operation disclosure."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Callable


@dataclass(frozen=True, slots=True)
class DisclosureReceiptResult:
    """Result of atomically consuming a disclosure receipt."""

    accepted: bool
    code: str


@dataclass(frozen=True, slots=True)
class DisclosureReceiptBinding:
    """Security fingerprints bound to one exact terminal disclosure."""

    terminal_relative_path: str
    terminal_sha256: str
    policy_sha256: str
    enabled_state_sha256: str

    @property
    def complete(self) -> bool:
        return bool(
            self.terminal_relative_path
            and self.policy_sha256
            and self.enabled_state_sha256
        )


@dataclass(frozen=True, slots=True)
class _DisclosureReceipt:
    binding: DisclosureReceiptBinding
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
        """Issue a legacy operation-hash receipt.

        Kept while the existing v1 ``opencli_execute`` consumer migrates to
        :meth:`consume_bound`.
        """
        self._grant(
            scope=scope,
            site=site,
            operation=operation,
            binding=DisclosureReceiptBinding(
                terminal_relative_path="",
                terminal_sha256=operation_sha256,
                policy_sha256="",
                enabled_state_sha256="",
            ),
        )

    def grant_bound(
        self,
        *,
        scope: str,
        site: str,
        operation: str,
        terminal_relative_path: str,
        terminal_sha256: str,
        policy_sha256: str,
        enabled_state_sha256: str,
    ) -> None:
        """Issue or replace one fully bound terminal receipt."""
        binding = DisclosureReceiptBinding(
            terminal_relative_path=_validate_terminal_path(terminal_relative_path),
            terminal_sha256=_validate_fingerprint(
                terminal_sha256,
                "terminal_sha256",
            ),
            policy_sha256=_validate_fingerprint(
                policy_sha256,
                "policy_sha256",
            ),
            enabled_state_sha256=_validate_fingerprint(
                enabled_state_sha256,
                "enabled_state_sha256",
            ),
        )
        self._grant(
            scope=scope,
            site=site,
            operation=operation,
            binding=binding,
        )

    def _grant(
        self,
        *,
        scope: str,
        site: str,
        operation: str,
        binding: DisclosureReceiptBinding,
    ) -> None:
        now = self._clock()
        key = (scope, site, operation)
        with self._lock:
            self._prune_expired(now)
            self._receipts[key] = _DisclosureReceipt(
                binding=binding,
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
        """Atomically consume by legacy operation hash.

        A fully bound receipt can still be consumed through this compatibility
        path during the tool migration, but only its terminal content hash is
        checked. New manifest consumers must call :meth:`consume_bound`.
        """
        return self._consume(
            scope=scope,
            site=site,
            operation=operation,
            expected=DisclosureReceiptBinding(
                terminal_relative_path="",
                terminal_sha256=operation_sha256,
                policy_sha256="",
                enabled_state_sha256="",
            ),
            require_bound=False,
        )

    def consume_bound(
        self,
        *,
        scope: str,
        site: str,
        operation: str,
        terminal_relative_path: str,
        terminal_sha256: str,
        policy_sha256: str,
        enabled_state_sha256: str,
    ) -> DisclosureReceiptResult:
        """Atomically validate and consume every terminal security binding."""
        try:
            expected = DisclosureReceiptBinding(
                terminal_relative_path=_validate_terminal_path(terminal_relative_path),
                terminal_sha256=_validate_fingerprint(
                    terminal_sha256,
                    "terminal_sha256",
                ),
                policy_sha256=_validate_fingerprint(
                    policy_sha256,
                    "policy_sha256",
                ),
                enabled_state_sha256=_validate_fingerprint(
                    enabled_state_sha256,
                    "enabled_state_sha256",
                ),
            )
        except ValueError:
            return DisclosureReceiptResult(
                False,
                "opencli_disclosure_binding_invalid",
            )
        return self._consume(
            scope=scope,
            site=site,
            operation=operation,
            expected=expected,
            require_bound=True,
        )

    def _consume(
        self,
        *,
        scope: str,
        site: str,
        operation: str,
        expected: DisclosureReceiptBinding,
        require_bound: bool,
    ) -> DisclosureReceiptResult:
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
            actual = receipt.binding
            if require_bound and not actual.complete:
                self._receipts.pop(key, None)
                return DisclosureReceiptResult(
                    False,
                    "opencli_disclosure_binding_required",
                )
            if (
                require_bound
                and actual.terminal_relative_path != expected.terminal_relative_path
            ):
                self._receipts.pop(key, None)
                return DisclosureReceiptResult(
                    False,
                    "opencli_disclosure_terminal_changed",
                )
            if actual.terminal_sha256 != expected.terminal_sha256:
                self._receipts.pop(key, None)
                return DisclosureReceiptResult(False, "opencli_disclosure_changed")
            if require_bound and actual.policy_sha256 != expected.policy_sha256:
                self._receipts.pop(key, None)
                return DisclosureReceiptResult(
                    False,
                    "opencli_disclosure_policy_changed",
                )
            if (
                require_bound
                and actual.enabled_state_sha256 != expected.enabled_state_sha256
            ):
                self._receipts.pop(key, None)
                return DisclosureReceiptResult(
                    False,
                    "opencli_disclosure_state_changed",
                )
            self._receipts.pop(key, None)
            self._prune_expired(now)
            return DisclosureReceiptResult(True, "ok")

    def clear(self) -> None:
        """Clear all receipts. Intended for lifecycle cleanup and tests."""
        with self._lock:
            self._receipts.clear()

    def _prune_expired(self, now: float) -> None:
        expired = [
            key for key, receipt in self._receipts.items() if receipt.expires_at <= now
        ]
        for key in expired:
            self._receipts.pop(key, None)


_OPENCLI_DISCLOSURE_STORE = DisclosureReceiptStore()


def get_opencli_disclosure_store() -> DisclosureReceiptStore:
    """Return the process-local store shared by tool and rail providers."""
    return _OPENCLI_DISCLOSURE_STORE


def _validate_terminal_path(value: str) -> str:
    normalized = str(value or "")
    pure_path = PurePosixPath(normalized)
    if (
        not normalized
        or "\\" in normalized
        or pure_path.is_absolute()
        or ".." in pure_path.parts
        or pure_path.as_posix() != normalized
    ):
        raise ValueError("terminal_relative_path must be canonical")
    return normalized


def _validate_fingerprint(value: str, field: str) -> str:
    normalized = str(value or "")
    if len(normalized) != 64 or any(
        character not in "0123456789abcdef" for character in normalized
    ):
        raise ValueError(f"{field} must be a lowercase SHA-256 digest")
    return normalized


__all__ = [
    "DisclosureReceiptBinding",
    "DisclosureReceiptResult",
    "DisclosureReceiptStore",
    "get_opencli_disclosure_store",
]
