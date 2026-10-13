#!/usr/bin/env python3
# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""Build the reproducible OpenCLI site-adapter runtime archive and catalog.

The archive, manifest and catalog are committed to the repository. Release
builds consume those files directly and therefore never need npm access.

The catalog is generated here, at build time, from the package's own
``cli-manifest.json``. The runtime never spawns OpenCLI to discover commands,
so user plugin initialisation can never run during discovery.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import shutil
import stat
import subprocess
import tempfile
import zipfile
from pathlib import Path
from typing import Any


LOGGER = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = PROJECT_ROOT / "third_party" / "opencli"
RESOURCE_DIR = PROJECT_ROOT / "jiuwenswarm" / "resources" / "runtime" / "opencli"
PACKAGE_NAME = "@jackwener/opencli"
PACKAGE_VERSION = "1.8.8"
MINIMUM_NODE_VERSION = "20.18.1"
PACKAGE_RELATIVE_DIR = "node_modules/@jackwener/opencli"
# Our own entry (third_party/opencli/entry.mjs) wraps the package's
# dist/src/main.js so OpenCLI parses argv correctly under Electron Node mode.
CLI_RELATIVE_PATH = "entry.mjs"
ARCHIVE_NAME = f"opencli-{PACKAGE_VERSION}.zip"
MANIFEST_NAME = "manifest.json"
CATALOG_NAME = "catalog.json"
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
NPM_INSTALL_ARGUMENTS = (
    "ci",
    "--omit=dev",
    "--omit=optional",
    "--ignore-scripts",
    "--no-audit",
    "--no-fund",
    "--bin-links=false",
)
# Only these manifest fields are carried into the product catalog.
_ARG_FIELDS = ("name", "type", "required", "positional", "choices", "default", "help")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _resolve_executable(name: str, explicit: str | None) -> str:
    candidate = explicit or shutil.which(name)
    if not candidate:
        raise RuntimeError(f"{name} was not found in PATH")
    return str(Path(candidate).resolve())


def _version_tuple(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.strip().lstrip("v").split("-", 1)[0].split("."))


def _isolated_env(home: Path) -> dict[str, str]:
    """Run OpenCLI with a private HOME so user adapters/plugins never load."""
    env = os.environ.copy()
    for key in list(env):
        if key.startswith("OPENCLI_"):
            env.pop(key)
    env["HOME"] = str(home)
    env["USERPROFILE"] = str(home)
    return env


def _validate_runtime(node: str, home: Path) -> None:
    node_result = subprocess.run(
        [node, "--version"], capture_output=True, text=True, timeout=10, check=False
    )
    node_version = (node_result.stdout or node_result.stderr).strip()
    if node_result.returncode != 0 or _version_tuple(node_version) < _version_tuple(MINIMUM_NODE_VERSION):
        raise RuntimeError(f"Node.js {MINIMUM_NODE_VERSION}+ is required; found {node_version!r}")

    package_json = SOURCE_DIR / PACKAGE_RELATIVE_DIR / "package.json"
    cli = SOURCE_DIR / CLI_RELATIVE_PATH
    if not package_json.is_file() or not cli.is_file():
        raise RuntimeError(f"Installed OpenCLI entry point is missing: {cli}")
    installed = json.loads(package_json.read_text(encoding="utf-8"))
    if installed.get("version") != PACKAGE_VERSION:
        raise RuntimeError(f"Expected {PACKAGE_NAME}@{PACKAGE_VERSION}, found {installed.get('version')!r}")

    result = subprocess.run(
        [node, str(cli), "--version"],
        cwd=SOURCE_DIR,
        env=_isolated_env(home),
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if result.returncode != 0 or PACKAGE_VERSION not in result.stdout:
        detail = (result.stderr or result.stdout).strip()[-1000:]
        raise RuntimeError(f"OpenCLI --version verification failed: {detail}")


def _electron_app_sites(node: str, home: Path) -> list[str]:
    """Read upstream's built-in desktop (Electron) app registry."""
    module = (SOURCE_DIR / PACKAGE_RELATIVE_DIR / "dist" / "src" / "electron-apps.js").resolve()
    script = (
        f"import({json.dumps(module.as_uri())})"
        ".then(m => process.stdout.write(JSON.stringify(Object.keys(m.builtinApps || {}))))"
    )
    result = subprocess.run(
        [node, "-e", script],
        cwd=SOURCE_DIR,
        env=_isolated_env(home),
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Could not read OpenCLI electron app registry: {result.stderr.strip()[-500:]}")
    sites = json.loads(result.stdout)
    if not isinstance(sites, list):
        raise RuntimeError("OpenCLI electron app registry is not a list")
    return sorted(str(site) for site in sites)


def build_catalog(manifest: list[dict[str, Any]], electron_app_sites: list[str]) -> dict[str, Any]:
    """Keep website adapters only, in the product's source-neutral schema."""
    excluded_sites = set(electron_app_sites)
    commands: list[dict[str, Any]] = []
    excluded_local = 0
    for entry in manifest:
        site = str(entry.get("site") or "").strip()
        name = str(entry.get("name") or "").strip()
        if not site or not name or site in excluded_sites:
            continue
        if entry.get("strategy") == "local":
            excluded_local += 1
            continue
        access = "write" if entry.get("access") == "write" else "read"
        args = []
        for arg in entry.get("args") or []:
            if not isinstance(arg, dict) or not arg.get("name"):
                continue
            args.append({field: arg.get(field) for field in _ARG_FIELDS if arg.get(field) is not None})
        commands.append(
            {
                "site": site,
                "command": name,
                "description": str(entry.get("description") or ""),
                "access": access,
                "needs_browser": entry.get("browser") is True,
                "args": args,
                "columns": [str(column) for column in entry.get("columns") or []],
                "domain": str(entry.get("domain") or ""),
            }
        )
    commands.sort(key=lambda item: (item["site"], item["command"]))
    return {
        "schema_version": 1,
        "source": "opencli",
        "version": PACKAGE_VERSION,
        "excluded": {
            "electron_app_sites": sorted(excluded_sites),
            "local_strategy_commands": excluded_local,
        },
        "commands": commands,
    }


def _production_provenance(lock: dict[str, Any]) -> list[dict[str, str]]:
    provenance: list[dict[str, str]] = []
    packages = lock.get("packages")
    if not isinstance(packages, dict):
        raise RuntimeError("package-lock.json does not contain a packages map")
    for package_path, metadata in sorted(packages.items()):
        if not package_path.startswith("node_modules/") or not isinstance(metadata, dict):
            continue
        if metadata.get("dev") is True or metadata.get("optional") is True:
            continue
        package_json_path = SOURCE_DIR / package_path / "package.json"
        package_json: dict[str, Any] = {}
        if package_json_path.is_file():
            package_json = json.loads(package_json_path.read_text(encoding="utf-8"))
        provenance.append(
            {
                "name": str(package_json.get("name") or package_path.removeprefix("node_modules/")),
                "version": str(metadata.get("version") or package_json.get("version") or ""),
                "license": str(package_json.get("license") or metadata.get("license") or "UNKNOWN"),
                "resolved": str(metadata.get("resolved") or ""),
                "integrity": str(metadata.get("integrity") or ""),
            }
        )
    return provenance


def _is_generated_npm_path(relative: Path) -> bool:
    """Return whether *relative* is platform-dependent npm install metadata."""
    if relative.as_posix() == ".package-lock.json":
        return True
    parts = relative.parts
    return any(
        part == ".bin" and (index == 0 or parts[index - 1] == "node_modules")
        for index, part in enumerate(parts)
    )


def _archive_files(node_modules: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(node_modules.rglob("*"), key=lambda item: item.relative_to(node_modules).as_posix()):
        relative = path.relative_to(node_modules)
        if _is_generated_npm_path(relative):
            continue
        if path.is_symlink():
            raise RuntimeError(f"Symbolic links must not be bundled: {path.relative_to(SOURCE_DIR).as_posix()}")
        if path.is_file():
            files.append(path)
    return files


def _write_deterministic_zip(output: Path) -> None:
    files = [SOURCE_DIR / CLI_RELATIVE_PATH, *_archive_files(SOURCE_DIR / "node_modules")]
    output.parent.mkdir(parents=True, exist_ok=True)
    temp_output = output.with_suffix(output.suffix + ".tmp")
    temp_output.unlink(missing_ok=True)
    with zipfile.ZipFile(temp_output, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(SOURCE_DIR).as_posix(), ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            with path.open("rb") as source:
                archive.writestr(info, source.read(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    os.replace(temp_output, output)


def _write_json(path: Path, payload: dict[str, Any], *, indent: int | None = 2) -> None:
    path.write_text(
        json.dumps(payload, indent=indent, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def build(*, npm_executable: str | None = None, node_executable: str | None = None) -> None:
    npm = _resolve_executable("npm", npm_executable)
    node = _resolve_executable("node", node_executable)
    lock_path = SOURCE_DIR / "package-lock.json"
    if not lock_path.is_file():
        raise RuntimeError(f"Missing {lock_path}. Generate and review the lockfile before building the archive.")

    build_env = os.environ.copy()
    build_env.update({"npm_config_audit": "false", "npm_config_fund": "false"})
    subprocess.run([npm, *NPM_INSTALL_ARGUMENTS], cwd=SOURCE_DIR, env=build_env, check=True)

    with tempfile.TemporaryDirectory(prefix="jiuwenswarm-opencli-home-") as home_dir:
        home = Path(home_dir)
        _validate_runtime(node, home)
        electron_app_sites = _electron_app_sites(node, home)

    upstream_manifest_path = SOURCE_DIR / PACKAGE_RELATIVE_DIR / "cli-manifest.json"
    upstream_manifest = json.loads(upstream_manifest_path.read_text(encoding="utf-8"))
    if not isinstance(upstream_manifest, list):
        raise RuntimeError("OpenCLI cli-manifest.json must be a list")
    catalog = build_catalog(upstream_manifest, electron_app_sites)

    RESOURCE_DIR.mkdir(parents=True, exist_ok=True)
    catalog_path = RESOURCE_DIR / CATALOG_NAME
    _write_json(catalog_path, catalog, indent=1)
    archive_path = RESOURCE_DIR / ARCHIVE_NAME
    _write_deterministic_zip(archive_path)

    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    manifest = {
        "schema_version": 1,
        "package": PACKAGE_NAME,
        "version": PACKAGE_VERSION,
        "minimum_node_version": MINIMUM_NODE_VERSION,
        "cli_relative_path": CLI_RELATIVE_PATH,
        "archive": ARCHIVE_NAME,
        "archive_sha256": _sha256(archive_path),
        "catalog": CATALOG_NAME,
        "catalog_sha256": _sha256(catalog_path),
        "provenance": {
            "source_manifest": "third_party/opencli/package.json",
            "source_lockfile": "third_party/opencli/package-lock.json",
            "source_lockfile_sha256": _sha256(lock_path),
            "install_command": f"npm {' '.join(NPM_INSTALL_ARGUMENTS)}",
            "dependencies": _production_provenance(lock),
        },
    }
    _write_json(RESOURCE_DIR / MANIFEST_NAME, manifest)
    LOGGER.info(
        "Wrote %s (%d commands, %d sites)",
        ARCHIVE_NAME,
        len(catalog["commands"]),
        len({item["site"] for item in catalog["commands"]}),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--npm", help="Path to npm/npm.cmd")
    parser.add_argument("--node", help="Path to node executable")
    args = parser.parse_args()
    try:
        build(npm_executable=args.npm, node_executable=args.node)
    except (OSError, RuntimeError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        LOGGER.error("error: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    raise SystemExit(main())
