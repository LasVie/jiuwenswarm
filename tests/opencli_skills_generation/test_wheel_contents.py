from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

import pytest

from scripts.opencli_skills.verify_wheel import (
    OPENCLI_SKILL_PREFIX,
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

    for site_index in range(EXPECTED_SITE_COUNT):
        site = f"site-{site_index:03d}"
        site_path = f"sites/{site}/index.md"
        site_content = f"# {site}\n".encode()
        skill_files[site_path] = site_content
    managed_files = {
        relative: _sha256(content) for relative, content in sorted(skill_files.items())
    }
    managed = {
        "schema_version": 1,
        "generator_version": "2",
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
    assert result.managed_file_count == EXPECTED_SITE_COUNT + 1
    assert result.wheel_path == wheel_path.resolve()


@pytest.mark.parametrize(
    "relative_path",
    [
        "SKILL.md",
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
def test_verify_wheel_rejects_inventory_count_drift(
    tmp_path: Path,
    drift: str,
) -> None:
    entries = _valid_wheel_entries()
    if drift == "sites":
        del entries[f"{OPENCLI_SKILL_PREFIX}sites/site-161/index.md"]
        _rewrite_managed_hashes(entries)
    else:
        manifest_member = f"{OPENCLI_SKILL_PREFIX}generated-manifest.json"
        manifest = json.loads(entries[manifest_member].decode("utf-8"))
        manifest["command_count"] -= 1
        entries[manifest_member] = _json_bytes(manifest)
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
