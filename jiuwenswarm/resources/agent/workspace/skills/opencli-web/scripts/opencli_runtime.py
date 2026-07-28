#!/usr/bin/env python3
"""Side-effect-free OpenCLI readiness checks for guarded Skill wrappers."""

from __future__ import annotations

import ipaddress
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Mapping, Sequence


DEFAULT_DAEMON_STATUS_URL = "http://127.0.0.1:19825/status"
DEFAULT_STATUS_TIMEOUT_SECONDS = 0.75
STATUS_URL_ENV = "JIUWENSWARM_OPENCLI_DAEMON_STATUS_URL"
_MAX_STATUS_BYTES = 64 * 1024
_ERROR_CODE_LINE = re.compile(
    r"""(?im)^\s*["']?code["']?\s*:\s*["']?"""
    r"""([A-Za-z][A-Za-z0-9_-]*)["']?\s*,?\s*$"""
)


@dataclass(frozen=True)
class OpenCLIRuntimeProbe:
    """Read-only daemon state used to decide whether adapter dispatch may start."""

    state: str
    dispatch_allowed: bool
    daemon_running: bool
    extension_connected: bool | None
    error_code: str | None = None
    message: str = ""
    detail: str = ""

    def public_result(self) -> dict[str, Any]:
        """Return non-sensitive state suitable for a wrapper JSON envelope."""

        return {
            "state": self.state,
            "daemon_running": self.daemon_running,
            "extension_connected": self.extension_connected,
        }


def select_opencli_profile(
    prefix_args: Sequence[str],
    *,
    environ: Mapping[str, str] | None = None,
) -> str | None:
    """Resolve the profile selected by explicit OpenCLI args or the environment."""

    for index, argument in enumerate(prefix_args):
        if argument == "--profile":
            if index + 1 < len(prefix_args):
                value = prefix_args[index + 1].strip()
                return value or None
            return None
        if argument.startswith("--profile="):
            value = argument.partition("=")[2].strip()
            return value or None

    configured = (environ or os.environ).get("OPENCLI_PROFILE", "").strip()
    return configured or None


def probe_opencli_runtime(
    *,
    profile: str | None = None,
    timeout_seconds: float = DEFAULT_STATUS_TIMEOUT_SECONDS,
    environ: Mapping[str, str] | None = None,
) -> OpenCLIRuntimeProbe:
    """Query daemon ``/status`` without starting or changing OpenCLI.

    An unreachable daemon is intentionally dispatch-safe: the real OpenCLI
    command owns daemon auto-start. A running daemon that explicitly reports no
    usable extension/profile is blocked before an adapter can execute.
    """

    env = environ or os.environ
    status_url = env.get(STATUS_URL_ENV, DEFAULT_DAEMON_STATUS_URL).strip()
    try:
        request_url = _status_url(status_url, profile)
        status = _request_status(request_url, timeout_seconds)
    except urllib.error.HTTPError as exc:
        return OpenCLIRuntimeProbe(
            state="status_unavailable",
            dispatch_allowed=True,
            daemon_running=True,
            extension_connected=None,
            detail=f"daemon /status returned HTTP {exc.code}; OpenCLI will decide readiness",
        )
    except (urllib.error.URLError, TimeoutError, OSError):
        return OpenCLIRuntimeProbe(
            state="daemon_not_running",
            dispatch_allowed=True,
            daemon_running=False,
            extension_connected=None,
            detail="daemon /status is unreachable; OpenCLI may auto-start the daemon",
        )
    except (UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return OpenCLIRuntimeProbe(
            state="status_unavailable",
            dispatch_allowed=True,
            daemon_running=False,
            extension_connected=None,
            detail=f"daemon /status could not be interpreted: {exc}",
        )

    if status.get("ok") is not True:
        return OpenCLIRuntimeProbe(
            state="status_unavailable",
            dispatch_allowed=True,
            daemon_running=True,
            extension_connected=None,
            detail="daemon /status did not return an OpenCLI success envelope",
        )

    if status.get("profileRequired") is True:
        return OpenCLIRuntimeProbe(
            state="profile_required",
            dispatch_allowed=False,
            daemon_running=True,
            extension_connected=False,
            error_code="opencli_browser_unavailable",
            message="OpenCLI requires an explicit connected browser profile",
            detail="daemon /status reports profileRequired=true",
        )

    if status.get("profileDisconnected") is True:
        return OpenCLIRuntimeProbe(
            state="profile_disconnected",
            dispatch_allowed=False,
            daemon_running=True,
            extension_connected=False,
            error_code="opencli_browser_unavailable",
            message="The selected OpenCLI browser profile is disconnected",
            detail="daemon /status reports profileDisconnected=true",
        )

    extension_connected = status.get("extensionConnected")
    if extension_connected is False:
        return OpenCLIRuntimeProbe(
            state="extension_not_connected",
            dispatch_allowed=False,
            daemon_running=True,
            extension_connected=False,
            error_code="opencli_browser_unavailable",
            message="The OpenCLI Browser Bridge extension is not connected",
            detail="daemon /status reports extensionConnected=false",
        )

    if extension_connected is True:
        return OpenCLIRuntimeProbe(
            state="ready",
            dispatch_allowed=True,
            daemon_running=True,
            extension_connected=True,
        )

    return OpenCLIRuntimeProbe(
        state="status_unavailable",
        dispatch_allowed=True,
        daemon_running=True,
        extension_connected=None,
        detail="daemon /status omitted extensionConnected; OpenCLI will decide readiness",
    )


def opencli_error_code(stdout: str | None, stderr: str | None) -> str | None:
    """Extract a typed OpenCLI error code from JSON or its YAML error envelope."""

    for raw_text in (stderr, stdout):
        text = (raw_text or "").strip()
        if not text:
            continue
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = None
        code = _nested_error_code(parsed)
        if code:
            return code
        match = _ERROR_CODE_LINE.search(text)
        if match:
            return match.group(1)
    return None


def is_browser_connect_failure(
    stdout: str | None,
    stderr: str | None,
) -> bool:
    """Return whether OpenCLI failed before adapter dispatch with BROWSER_CONNECT."""

    code = opencli_error_code(stdout, stderr)
    return isinstance(code, str) and code.upper() == "BROWSER_CONNECT"


def _status_url(base_url: str, profile: str | None) -> str:
    if not base_url:
        raise ValueError("daemon status URL is empty")
    parts = urllib.parse.urlsplit(base_url)
    if parts.scheme != "http" or not parts.hostname or not _is_loopback(parts.hostname):
        raise ValueError("daemon status URL must use HTTP on a loopback host")
    if parts.path != "/status":
        raise ValueError("daemon status URL path must be /status")

    if not profile:
        return base_url
    query = urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
    query = [(key, value) for key, value in query if key != "contextId"]
    query.append(("contextId", profile))
    return urllib.parse.urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urllib.parse.urlencode(query), "")
    )


def _is_loopback(hostname: str) -> bool:
    if hostname.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(hostname).is_loopback
    except ValueError:
        return False


def _request_status(status_url: str, timeout_seconds: float) -> dict[str, Any]:
    if not 0 < timeout_seconds <= 5:
        raise ValueError("status timeout must be greater than 0 and at most 5 seconds")
    request = urllib.request.Request(
        status_url,
        headers={"X-OpenCLI": "1"},
        method="GET",
    )
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(request, timeout=timeout_seconds) as response:
        raw = response.read(_MAX_STATUS_BYTES + 1)
    if len(raw) > _MAX_STATUS_BYTES:
        raise ValueError("daemon status response is too large")
    parsed = json.loads(raw.decode("utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError("daemon status response must be a JSON object")
    return parsed


def _nested_error_code(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None
    error = value.get("error")
    if isinstance(error, dict):
        code = error.get("code")
        if isinstance(code, str) and code.strip():
            return code.strip()
    code = value.get("code")
    if isinstance(code, str) and code.strip():
        return code.strip()
    return None
