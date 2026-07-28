"""Resolve the installed OpenCLI entry point without invoking a shell."""

from __future__ import annotations

import json
import os
import shutil
from collections.abc import Sequence
from pathlib import Path

_IS_WINDOWS = os.name == "nt"
_OPENCLI_PACKAGE_NAME = "@jackwener/opencli"
_OPENCLI_MAIN_RELATIVE_PATH = (
    Path("node_modules") / "@jackwener" / "opencli" / "dist" / "src" / "main.js"
)
_WINDOWS_SHIM_SUFFIXES = {".bat", ".cmd", ".ps1"}
_MAX_PACKAGE_JSON_BYTES = 1_000_000


class OpenCLILauncherError(RuntimeError):
    """The installed OpenCLI launcher cannot be executed with ``shell=False``."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def resolve_opencli_launcher() -> list[str]:
    """Return a trusted argv prefix discovered only from the process PATH.

    The structured contract and model payload cannot select a binary, inject an
    environment, or supply Node flags. On Windows, npm command shims are
    resolved to the adjacent package ``main.js`` and a real ``node.exe`` so the
    caller can keep ``shell=False``.
    """

    resolved = _find_opencli_on_path()
    if resolved is None:
        raise OpenCLILauncherError(
            "opencli_not_found",
            "OpenCLI is not installed on the current process PATH",
        )

    try:
        launcher = Path(resolved).resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise OpenCLILauncherError(
            "opencli_launcher_invalid",
            "The installed OpenCLI launcher cannot be resolved",
        ) from exc

    if not _IS_WINDOWS:
        return [str(launcher)]
    if launcher.suffix.lower() == ".exe":
        return [str(launcher)]
    if launcher.suffix.lower() not in _WINDOWS_SHIM_SUFFIXES:
        raise OpenCLILauncherError(
            "opencli_launcher_unsupported",
            "The Windows OpenCLI launcher is not an executable or known npm shim",
        )

    main_js = (launcher.parent / _OPENCLI_MAIN_RELATIVE_PATH).resolve()
    node = launcher.parent / "node.exe"
    if not node.is_file():
        node_on_path = shutil.which("node.exe") or shutil.which("node")
        node = Path(node_on_path).resolve() if node_on_path else node
    if not node.is_file() or node.name.lower() != "node.exe" or not main_js.is_file():
        raise OpenCLILauncherError(
            "opencli_launcher_unsupported",
            "The Windows OpenCLI npm shim has no trusted Node and package main.js",
        )
    return [str(node), str(main_js)]


def resolve_opencli_package_version(launcher_argv: Sequence[str]) -> str:
    """Prove the installed OpenCLI version from its bound npm package.

    Only a launcher containing the reviewed package ``dist/src/main.js`` is
    accepted. This ties the catalog version to the package whose JavaScript
    entry point will actually run instead of trusting a second PATH lookup,
    model input, an environment variable, or command output.
    """

    package_roots: set[Path] = set()
    if isinstance(launcher_argv, (str, bytes)):
        _raise_catalog_drift()
    for raw_path in launcher_argv:
        if not isinstance(raw_path, str) or not raw_path:
            continue
        try:
            candidate = Path(raw_path).resolve(strict=True)
        except (OSError, RuntimeError, ValueError):
            continue
        package_root = _package_root_for_main(candidate)
        if package_root is not None:
            package_roots.add(package_root)
    if len(package_roots) != 1:
        _raise_catalog_drift()

    package_root = package_roots.pop()
    package_json = package_root / "package.json"
    try:
        resolved_package_json = package_json.resolve(strict=True)
        if resolved_package_json.parent != package_root:
            _raise_catalog_drift()
        if (
            not resolved_package_json.is_file()
            or resolved_package_json.stat().st_size > _MAX_PACKAGE_JSON_BYTES
        ):
            _raise_catalog_drift()
        raw_package = resolved_package_json.read_bytes()
        package = json.loads(raw_package.decode("utf-8"))
    except OpenCLILauncherError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise OpenCLILauncherError(
            "opencli_catalog_drift",
            "The installed OpenCLI package version cannot be proven",
        ) from exc

    if not isinstance(package, dict):
        _raise_catalog_drift()
    name = package.get("name")
    version = package.get("version")
    if (
        name != _OPENCLI_PACKAGE_NAME
        or not isinstance(version, str)
        or not version
        or version != version.strip()
        or "\x00" in version
    ):
        _raise_catalog_drift()
    return version


def _package_root_for_main(candidate: Path) -> Path | None:
    if (
        candidate.name != "main.js"
        or candidate.parent.name != "src"
        or candidate.parent.parent.name != "dist"
    ):
        return None
    package_root = candidate.parents[2]
    if (
        package_root.name.lower() != "opencli"
        or package_root.parent.name.lower() != "@jackwener"
    ):
        return None
    try:
        expected_main = (package_root / "dist" / "src" / "main.js").resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    return package_root if expected_main == candidate else None


def _raise_catalog_drift() -> None:
    raise OpenCLILauncherError(
        "opencli_catalog_drift",
        "The installed OpenCLI package version cannot be proven",
    )


def _find_opencli_on_path() -> str | None:
    resolved = shutil.which("opencli")
    if resolved is not None or not _IS_WINDOWS:
        return resolved
    for name in ("opencli.cmd", "opencli.bat", "opencli.ps1"):
        resolved = shutil.which(name)
        if resolved is not None:
            return resolved
    return None


__all__ = [
    "OpenCLILauncherError",
    "resolve_opencli_launcher",
    "resolve_opencli_package_version",
]
