from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

import pytest

from scripts.opencli_skills.verify_wheel import (
    OPENCLI_SKILL_PREFIX,
    REQUIRED_RUNTIME_MEMBERS,
    WheelVerificationError,
    main,
    verify_wheel,
)


EXPECTED_SITE_COUNT = 162
EXPECTED_COMMAND_COUNT = 1123


def _json_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
        + "\n"
    ).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _valid_wheel_entries() -> dict[str, bytes]:
    skill_files = {"SKILL.md": b"---\nname: opencli-web\n---\n"}
    runtime_sites: dict[str, object] = {}
    command_index = 0

    for site_index in range(EXPECTED_SITE_COUNT):
        site = f"site-{site_index:03d}"
        site_path = f"sites/{site}/SKILL.md"
        site_content = f"---\nname: {site}\n---\n".encode()
        skill_files[site_path] = site_content
        site_command_count = EXPECTED_COMMAND_COUNT // EXPECTED_SITE_COUNT + (
            site_index < EXPECTED_COMMAND_COUNT % EXPECTED_SITE_COUNT
        )
        commands = {}
        for _ in range(site_command_count):
            command = f"command-{command_index:04d}"
            commands[command] = {"execution_state": "disabled"}
            command_index += 1
        runtime_sites[site] = {
            "display_name": site,
            "operations": {
                "public-data": {
                    "commands": commands,
                    "policy_sha256": "1" * 64,
                    "purpose": "Synthetic wheel verification fixture.",
                    "terminal": {
                        "kind": "site",
                        "path": site_path,
                        "sha256": _sha256(site_content),
                    },
                }
            },
            "policy_sha256": "1" * 64,
            "terminal": "site",
        }

    assert command_index == EXPECTED_COMMAND_COUNT
    runtime = {
        "schema_version": 1,
        "generator_version": "1",
        "catalog": {
            "opencli_version": "1.8.6",
            "source_sha256": "2" * 64,
            "canonical_sha256": "3" * 64,
            "command_count": EXPECTED_COMMAND_COUNT,
        },
        "sites": runtime_sites,
    }
    skill_files["opencli-runtime.json"] = _json_bytes(runtime)
    managed_files = {
        relative: _sha256(content) for relative, content in sorted(skill_files.items())
    }
    managed = {
        "schema_version": 1,
        "generator_version": "1",
        "opencli_version": "1.8.6",
        "catalog_sha256": "2" * 64,
        "policy_sha256": "4" * 64,
        "site_count": EXPECTED_SITE_COUNT,
        "command_count": EXPECTED_COMMAND_COUNT,
        "file_count": len(managed_files),
        "files": managed_files,
    }
    skill_files["generated-manifest.json"] = _json_bytes(managed)

    entries = {
        f"{OPENCLI_SKILL_PREFIX}{relative}": content
        for relative, content in skill_files.items()
    }
    for required_member in REQUIRED_RUNTIME_MEMBERS:
        entries[required_member] = b'"""Synthetic runtime module."""\n'
    entries["jiuwenswarm-0.0.dist-info/WHEEL"] = (
        b"Wheel-Version: 1.0\nTag: py3-none-any\n"
    )
    return entries


def _write_wheel(
    tmp_path: Path,
    entries: dict[str, bytes],
    *,
    name: str = "jiuwenswarm-0.0-py3-none-any.whl",
) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    wheel_path = tmp_path / name
    with zipfile.ZipFile(wheel_path, "w", compression=zipfile.ZIP_DEFLATED) as wheel:
        for member, content in sorted(entries.items()):
            wheel.writestr(member, content)
    return wheel_path


def _rewrite_managed_hashes(entries: dict[str, bytes]) -> None:
    manifest_member = f"{OPENCLI_SKILL_PREFIX}generated-manifest.json"
    manifest = json.loads(entries[manifest_member].decode("utf-8"))
    owned = {
        member.removeprefix(OPENCLI_SKILL_PREFIX): _sha256(content)
        for member, content in sorted(entries.items())
        if member.startswith(OPENCLI_SKILL_PREFIX) and member != manifest_member
    }
    manifest["file_count"] = len(owned)
    manifest["files"] = owned
    entries[manifest_member] = _json_bytes(manifest)


def test_verify_wheel_accepts_complete_opencli_resources(tmp_path: Path) -> None:
    wheel_path = _write_wheel(tmp_path, _valid_wheel_entries())

    result = verify_wheel(wheel_path)

    assert result.site_count == EXPECTED_SITE_COUNT
    assert result.command_count == EXPECTED_COMMAND_COUNT
    assert result.managed_file_count == EXPECTED_SITE_COUNT + 2
    assert result.wheel_path == wheel_path.resolve()


@pytest.mark.parametrize(
    "relative_path",
    [
        "SKILL.md",
        "opencli-runtime.json",
        "generated-manifest.json",
    ],
)
def test_verify_wheel_rejects_missing_required_skill_resources(
    tmp_path: Path,
    relative_path: str,
) -> None:
    entries = _valid_wheel_entries()
    del entries[f"{OPENCLI_SKILL_PREFIX}{relative_path}"]
    wheel_path = _write_wheel(tmp_path, entries)

    with pytest.raises(WheelVerificationError, match="missing required"):
        verify_wheel(wheel_path)


@pytest.mark.parametrize("corruption", ["hash", "unmanaged"])
def test_verify_wheel_rejects_incomplete_managed_hash_coverage(
    tmp_path: Path,
    corruption: str,
) -> None:
    entries = _valid_wheel_entries()
    if corruption == "hash":
        entries[f"{OPENCLI_SKILL_PREFIX}SKILL.md"] = b"tampered\n"
    else:
        entries[f"{OPENCLI_SKILL_PREFIX}unmanaged.txt"] = b"not inventoried\n"
    wheel_path = _write_wheel(tmp_path, entries)

    with pytest.raises(WheelVerificationError, match="managed"):
        verify_wheel(wheel_path)


@pytest.mark.parametrize(
    "member",
    [
        "jiuwenswarm/example/__pycache__/module.cpython-311.pyc",
        "jiuwenswarm/resources/accidental.pyo",
    ],
)
def test_verify_wheel_rejects_cached_bytecode_anywhere(
    tmp_path: Path,
    member: str,
) -> None:
    entries = _valid_wheel_entries()
    entries[member] = b"cached bytecode"
    wheel_path = _write_wheel(tmp_path, entries)

    with pytest.raises(WheelVerificationError, match="cached bytecode"):
        verify_wheel(wheel_path)


@pytest.mark.parametrize("drift", ["sites", "commands"])
def test_verify_wheel_recounts_runtime_inventory(
    tmp_path: Path,
    drift: str,
) -> None:
    entries = _valid_wheel_entries()
    runtime_member = f"{OPENCLI_SKILL_PREFIX}opencli-runtime.json"
    runtime = json.loads(entries[runtime_member].decode("utf-8"))
    if drift == "sites":
        runtime["sites"].pop("site-161")
    else:
        runtime["sites"]["site-000"]["operations"]["public-data"]["commands"].pop(
            "command-0000"
        )
    entries[runtime_member] = _json_bytes(runtime)
    _rewrite_managed_hashes(entries)
    wheel_path = _write_wheel(tmp_path, entries)

    with pytest.raises(WheelVerificationError, match=drift):
        verify_wheel(wheel_path)


def test_wheel_verifier_cli_accepts_an_actual_path_and_reports_json(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    wheel_path = _write_wheel(
        tmp_path / "directory with spaces",
        _valid_wheel_entries(),
    )

    assert main([str(wheel_path)]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["ok"] is True
    assert output["site_count"] == EXPECTED_SITE_COUNT
    assert output["command_count"] == EXPECTED_COMMAND_COUNT
    assert output["wheel_path"] == str(wheel_path.resolve())

    assert main([str(tmp_path / "missing.whl")]) == 1
    assert "verification failed" in capsys.readouterr().err.lower()
