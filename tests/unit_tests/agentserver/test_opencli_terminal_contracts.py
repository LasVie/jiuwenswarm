from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest
from openjiuwen.core.single_agent.rail.base import (
    AgentCallbackContext,
    ToolCallInputs,
)
from openjiuwen.harness.tools import ToolOutput

from jiuwenswarm.agents.harness.common.opencli.contracts import (
    OpenCLIContractError,
    load_operation_contract,
    load_terminal_contract,
    load_terminal_contract_by_path,
)
from jiuwenswarm.agents.harness.common.opencli.disclosure import (
    DisclosureReceiptStore,
)
from jiuwenswarm.agents.harness.common.opencli.manifest import (
    OpenCLIManifestError,
    load_runtime_manifest,
)
from jiuwenswarm.agents.harness.common.opencli.rail import (
    OpenCLIDisclosureRail,
)
from jiuwenswarm.agents.harness.common.opencli.security import (
    load_skill_enabled_snapshot,
)


_SITE = "rest-countries"
_OPERATION = "public-data"
_SITE_TERMINAL = f"sites/{_SITE}/SKILL.md"
_OPERATION_TERMINAL = f"sites/{_SITE}/operations/{_OPERATION}.md"


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _command_manifest() -> dict[str, object]:
    return {
        "executor": "generic_manifest_read",
        "execution_state": "enabled",
        "semantic_effect": "public_read",
        "risk": "low",
        "auth": "none",
        "transport": "public_http",
        "strategy": "public",
        "browser": False,
        "opencli_version": "1.8.6",
        "access": "read",
        "args": [
            {
                "name": "name",
                "type": "string",
                "required": True,
                "help": "Country name",
                "default": None,
                "positional": False,
                "valueRequired": True,
                "choices": [],
                "constraints": {
                    "max_length": 100,
                },
            }
        ],
        "confirmation": "none",
        "fallback": {
            "before_dispatch": "browser_agent",
            "after_failure": "browser_agent",
        },
        "file_inputs": [],
        "file_outputs": [],
        "sensitive_output": [],
    }


def _runtime_manifest(
    terminal_bytes: bytes,
    *,
    terminal_kind: str = "site",
) -> dict[str, object]:
    terminal_path = _SITE_TERMINAL if terminal_kind == "site" else _OPERATION_TERMINAL
    return {
        "schema_version": 1,
        "generator_version": "1",
        "catalog": {
            "opencli_version": "1.8.6",
            "source_sha256": "1" * 64,
            "canonical_sha256": "2" * 64,
            "command_count": 1,
        },
        "sites": {
            _SITE: {
                "display_name": "REST Countries",
                "policy_sha256": "3" * 64,
                "terminal": terminal_kind,
                "operations": {
                    _OPERATION: {
                        "purpose": "Read public country data.",
                        "terminal": {
                            "kind": terminal_kind,
                            "path": terminal_path,
                            "sha256": _sha256(terminal_bytes),
                        },
                        "policy_sha256": "4" * 64,
                        "commands": {
                            "name": _command_manifest(),
                        },
                    }
                },
            }
        },
    }


def _install_manifest_skill(
    tmp_path: Path,
    *,
    terminal_kind: str = "site",
) -> tuple[Path, Path, dict[str, object]]:
    skills_root = tmp_path / "skills"
    skill_root = skills_root / "opencli-web"
    terminal_path = (
        skill_root / _SITE_TERMINAL
        if terminal_kind == "site"
        else skill_root / _OPERATION_TERMINAL
    )
    terminal_path.parent.mkdir(parents=True)
    terminal_bytes = b"---\nname: rest-countries\n---\n\n# Public country data\n"
    terminal_path.write_bytes(terminal_bytes)
    manifest = _runtime_manifest(
        terminal_bytes,
        terminal_kind=terminal_kind,
    )
    (skill_root / "opencli-runtime.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return skills_root, skill_root, manifest


def _write_legacy_operation(tmp_path: Path) -> tuple[Path, Path]:
    skills_root = tmp_path / "skills"
    operation_path = (
        skills_root
        / "opencli-web"
        / "sites"
        / "xiaohongshu"
        / "operations"
        / "publishing.md"
    )
    operation_path.parent.mkdir(parents=True)
    operation_path.write_text(
        """---
opencli_contract:
  version: 1
  site: xiaohongshu
  operation: publishing
  commands:
    publish:
      executor: xiaohongshu_guarded_publish
---

# Publishing
""",
        encoding="utf-8",
    )
    return skills_root, operation_path


def _tool_context(
    *,
    relative_path: str,
    skill_root: Path,
    content: str,
    success: bool = True,
    tool_name: str = "skill_tool",
) -> AgentCallbackContext:
    return AgentCallbackContext(
        agent=None,
        inputs=ToolCallInputs(
            tool_name=tool_name,
            tool_args={
                "skill_name": "opencli-web",
                "relative_file_path": relative_path,
            },
            tool_result=ToolOutput(
                success=success,
                data={
                    "skill_directory": str(skill_root),
                    "skill_content": content,
                },
            ),
        ),
        session=None,
    )


def test_manifest_site_terminal_loads_exact_reviewed_command(
    tmp_path: Path,
) -> None:
    skills_root, skill_root, _ = _install_manifest_skill(tmp_path)

    runtime = load_runtime_manifest(skill_root)
    contract = load_terminal_contract(
        skills_root,
        _SITE,
        _OPERATION,
    )
    by_path = load_terminal_contract_by_path(
        skills_root,
        _SITE_TERMINAL,
    )
    command = contract.command_contract("name")

    assert runtime.catalog.opencli_version == "1.8.6"
    assert contract.manifest_backed is True
    assert contract.terminal_kind == "site"
    assert contract.terminal_relative_path == _SITE_TERMINAL
    assert contract.operation_relative_path == _SITE_TERMINAL
    assert contract.terminal_sha256 == _sha256(
        (skill_root / _SITE_TERMINAL).read_bytes()
    )
    assert contract.policy_sha256 == "4" * 64
    assert by_path == contract
    assert command.executor == "generic_manifest_read"
    assert command.execution_state == "enabled"
    assert command.semantic_effect == "public_read"
    assert command.args[0]["name"] == "name"
    assert command.fallback.before_dispatch == "browser_agent"
    assert command.file_inputs == ()


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value.update({"unknown": True}),
        lambda value: value["sites"][_SITE].update({"unknown": True}),
        lambda value: value["sites"][_SITE]["operations"][_OPERATION].update(
            {"unknown": True}
        ),
        lambda value: value["sites"][_SITE]["operations"][_OPERATION]["commands"][
            "name"
        ].update({"unknown": True}),
        lambda value: value["sites"][_SITE]["operations"][_OPERATION]["commands"][
            "name"
        ]["args"][0].update({"unknown": True}),
        lambda value: value["sites"][_SITE]["operations"][_OPERATION]["commands"][
            "name"
        ]["fallback"].update({"unknown": True}),
    ],
)
def test_runtime_manifest_rejects_unknown_fields(
    tmp_path: Path,
    mutation,
) -> None:
    _, skill_root, manifest = _install_manifest_skill(tmp_path)
    mutated = deepcopy(manifest)
    mutation(mutated)
    (skill_root / "opencli-runtime.json").write_text(
        json.dumps(mutated),
        encoding="utf-8",
    )

    with pytest.raises(
        OpenCLIManifestError,
        match="unexpected fields",
    ):
        load_runtime_manifest(skill_root)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("execution_state", "reviewed"),
        ("semantic_effect", "read"),
        ("risk", "urgent"),
        ("auth", "cookie"),
        ("transport", "http"),
        ("executor", "shell"),
        ("confirmation", "model_id"),
        ("access", "execute"),
        ("browser", "false"),
        ("sensitive_output", True),
    ],
)
def test_runtime_manifest_rejects_invalid_command_policy_values(
    tmp_path: Path,
    field: str,
    value: object,
) -> None:
    _, skill_root, manifest = _install_manifest_skill(tmp_path)
    manifest["sites"][_SITE]["operations"][_OPERATION]["commands"]["name"][field] = (
        value
    )
    (skill_root / "opencli-runtime.json").write_text(
        json.dumps(manifest),
        encoding="utf-8",
    )

    with pytest.raises(OpenCLIManifestError):
        load_runtime_manifest(skill_root)


def test_runtime_manifest_rejects_catalog_command_count_mismatch(
    tmp_path: Path,
) -> None:
    _, skill_root, manifest = _install_manifest_skill(tmp_path)
    manifest["catalog"]["command_count"] = 2
    (skill_root / "opencli-runtime.json").write_text(
        json.dumps(manifest),
        encoding="utf-8",
    )

    with pytest.raises(OpenCLIManifestError, match="command count"):
        load_runtime_manifest(skill_root)


def test_manifest_rejects_wrong_terminal_kind_path_and_content_hash(
    tmp_path: Path,
) -> None:
    skills_root, skill_root, manifest = _install_manifest_skill(tmp_path)
    operation = manifest["sites"][_SITE]["operations"][_OPERATION]
    operation["terminal"]["path"] = _OPERATION_TERMINAL
    (skill_root / "opencli-runtime.json").write_text(
        json.dumps(manifest),
        encoding="utf-8",
    )

    with pytest.raises(OpenCLIManifestError, match="terminal path"):
        load_runtime_manifest(skill_root)

    _, skill_root, _ = _install_manifest_skill(
        tmp_path / "hash",
        terminal_kind="site",
    )
    (skill_root / _SITE_TERMINAL).write_text(
        "# modified after generation\n",
        encoding="utf-8",
    )

    with pytest.raises(
        OpenCLIContractError,
        match="content hash",
    ):
        load_terminal_contract(
            tmp_path / "hash" / "skills",
            _SITE,
            _OPERATION,
        )

    with pytest.raises(OpenCLIContractError):
        load_terminal_contract_by_path(
            skills_root,
            f"sites/{_SITE}/operations/not-registered.md",
        )


def test_legacy_operation_v1_remains_compatible(
    tmp_path: Path,
) -> None:
    skills_root, operation_path = _write_legacy_operation(tmp_path)

    legacy = load_operation_contract(
        skills_root,
        "xiaohongshu",
        "publishing",
    )
    terminal = load_terminal_contract(
        skills_root,
        "xiaohongshu",
        "publishing",
    )
    by_path = load_terminal_contract_by_path(
        skills_root,
        "sites/xiaohongshu/operations/publishing.md",
    )

    assert terminal == legacy == by_path
    assert terminal.manifest_backed is False
    assert terminal.terminal_kind == "operation"
    assert terminal.terminal_path == operation_path.resolve()
    assert terminal.policy_sha256 == terminal.operation_sha256
    assert terminal.command_contract("publish").execution_state == "custom"


def test_present_invalid_manifest_never_falls_back_to_legacy_v1(
    tmp_path: Path,
) -> None:
    skills_root, operation_path = _write_legacy_operation(tmp_path)
    manifest_path = skills_root / "opencli-web" / "opencli-runtime.json"
    manifest_path.mkdir()

    with pytest.raises(OpenCLIContractError):
        load_terminal_contract(
            skills_root,
            "xiaohongshu",
            "publishing",
        )

    assert operation_path.is_file()


@pytest.mark.parametrize(
    ("raw_state", "expected_enabled", "expected_valid", "expected_code"),
    [
        (
            {"skill_configs": {"opencli-web": {"enabled": True}}},
            True,
            True,
            "ok",
        ),
        (
            {"skill_configs": {"opencli-web": {"enabled": False}}},
            False,
            True,
            "opencli_skill_disabled",
        ),
        (
            {"skill_configs": {"opencli-web": {"enabled": "false"}}},
            False,
            False,
            "opencli_skill_state_invalid",
        ),
        (
            {"skill_configs": []},
            False,
            False,
            "opencli_skill_state_invalid",
        ),
        ([], False, False, "opencli_skill_state_invalid"),
    ],
)
def test_enabled_snapshot_is_strict_and_hashes_exact_state_bytes(
    tmp_path: Path,
    raw_state: object,
    expected_enabled: bool,
    expected_valid: bool,
    expected_code: str,
) -> None:
    state_bytes = json.dumps(raw_state).encode("utf-8")
    (tmp_path / "skills_state.json").write_bytes(state_bytes)

    snapshot = load_skill_enabled_snapshot(tmp_path)

    assert snapshot.enabled is expected_enabled
    assert snapshot.valid is expected_valid
    assert snapshot.code == expected_code
    assert snapshot.state_sha256 == _sha256(state_bytes)


def test_missing_enabled_state_defaults_enabled_with_stable_snapshot(
    tmp_path: Path,
) -> None:
    first = load_skill_enabled_snapshot(tmp_path)
    second = load_skill_enabled_snapshot(tmp_path)

    assert first == second
    assert first.enabled is True
    assert first.valid is True
    assert first.code == "opencli_skill_state_missing_default_enabled"
    assert len(first.state_sha256) == 64


def test_bound_receipt_validates_every_security_fingerprint_once() -> None:
    binding = {
        "terminal_relative_path": _SITE_TERMINAL,
        "terminal_sha256": "1" * 64,
        "policy_sha256": "2" * 64,
        "enabled_state_sha256": "3" * 64,
    }
    store = DisclosureReceiptStore()
    store.grant_bound(
        scope="main",
        site=_SITE,
        operation=_OPERATION,
        **binding,
    )

    accepted = store.consume_bound(
        scope="main",
        site=_SITE,
        operation=_OPERATION,
        **binding,
    )
    replay = store.consume_bound(
        scope="main",
        site=_SITE,
        operation=_OPERATION,
        **binding,
    )

    assert accepted.accepted is True
    assert replay.accepted is False
    assert replay.code == "opencli_disclosure_required"


@pytest.mark.parametrize(
    ("field", "replacement", "expected_code"),
    [
        (
            "terminal_relative_path",
            _OPERATION_TERMINAL,
            "opencli_disclosure_terminal_changed",
        ),
        (
            "terminal_sha256",
            "9" * 64,
            "opencli_disclosure_changed",
        ),
        (
            "policy_sha256",
            "9" * 64,
            "opencli_disclosure_policy_changed",
        ),
        (
            "enabled_state_sha256",
            "9" * 64,
            "opencli_disclosure_state_changed",
        ),
    ],
)
def test_bound_receipt_rejects_changed_binding(
    field: str,
    replacement: str,
    expected_code: str,
) -> None:
    binding = {
        "terminal_relative_path": _SITE_TERMINAL,
        "terminal_sha256": "1" * 64,
        "policy_sha256": "2" * 64,
        "enabled_state_sha256": "3" * 64,
    }
    store = DisclosureReceiptStore()
    store.grant_bound(
        scope="main",
        site=_SITE,
        operation=_OPERATION,
        **binding,
    )
    changed = dict(binding)
    changed[field] = replacement

    result = store.consume_bound(
        scope="main",
        site=_SITE,
        operation=_OPERATION,
        **changed,
    )

    assert result.accepted is False
    assert result.code == expected_code


def test_legacy_receipt_api_remains_compatible() -> None:
    store = DisclosureReceiptStore()
    store.grant(
        scope="main",
        site="xiaohongshu",
        operation="publishing",
        operation_sha256="abc",
    )

    result = store.consume(
        scope="main",
        site="xiaohongshu",
        operation="publishing",
        operation_sha256="abc",
    )

    assert result.accepted is True


@pytest.mark.asyncio
@pytest.mark.parametrize("terminal_kind", ["site", "operation"])
async def test_rail_grants_manifest_terminal_bound_to_enabled_state(
    tmp_path: Path,
    terminal_kind: str,
) -> None:
    skills_root, skill_root, _ = _install_manifest_skill(
        tmp_path,
        terminal_kind=terminal_kind,
    )
    terminal_relative_path = (
        _SITE_TERMINAL if terminal_kind == "site" else _OPERATION_TERMINAL
    )
    state_bytes = json.dumps(
        {"skill_configs": {"opencli-web": {"enabled": True}}}
    ).encode("utf-8")
    (skills_root / "skills_state.json").write_bytes(state_bytes)
    contract = load_terminal_contract(
        skills_root,
        _SITE,
        _OPERATION,
    )
    store = DisclosureReceiptStore()
    rail = OpenCLIDisclosureRail(
        scope="main",
        skills_root=skills_root,
        receipt_store=store,
    )

    await rail.after_tool_call(
        _tool_context(
            relative_path=terminal_relative_path,
            skill_root=skill_root,
            content=(skill_root / terminal_relative_path).read_text(encoding="utf-8"),
        )
    )

    receipt = store.consume_bound(
        scope="main",
        site=_SITE,
        operation=_OPERATION,
        terminal_relative_path=contract.terminal_relative_path,
        terminal_sha256=contract.terminal_sha256,
        policy_sha256=contract.policy_sha256,
        enabled_state_sha256=_sha256(state_bytes),
    )
    assert receipt.accepted is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("state_bytes", "relative_path", "tool_name", "success"),
    [
        (
            b'{"skill_configs":{"opencli-web":{"enabled":false}}}',
            _SITE_TERMINAL,
            "skill_tool",
            True,
        ),
        (b"{invalid", _SITE_TERMINAL, "skill_tool", True),
        (
            b'{"skill_configs":{"opencli-web":{"enabled":true}}}',
            _OPERATION_TERMINAL,
            "skill_tool",
            True,
        ),
        (
            b'{"skill_configs":{"opencli-web":{"enabled":true}}}',
            _SITE_TERMINAL,
            "list_files",
            True,
        ),
        (
            b'{"skill_configs":{"opencli-web":{"enabled":true}}}',
            _SITE_TERMINAL,
            "skill_tool",
            False,
        ),
    ],
)
async def test_rail_fails_closed_for_disabled_invalid_or_inexact_disclosure(
    tmp_path: Path,
    state_bytes: bytes,
    relative_path: str,
    tool_name: str,
    success: bool,
) -> None:
    skills_root, skill_root, _ = _install_manifest_skill(tmp_path)
    (skills_root / "skills_state.json").write_bytes(state_bytes)
    store = DisclosureReceiptStore()
    rail = OpenCLIDisclosureRail(
        scope="main",
        skills_root=skills_root,
        receipt_store=store,
    )

    await rail.after_tool_call(
        _tool_context(
            relative_path=relative_path,
            skill_root=skill_root,
            content=(skill_root / _SITE_TERMINAL).read_text(encoding="utf-8"),
            tool_name=tool_name,
            success=success,
        )
    )
    contract = load_terminal_contract(
        skills_root,
        _SITE,
        _OPERATION,
    )
    result = store.consume_bound(
        scope="main",
        site=_SITE,
        operation=_OPERATION,
        terminal_relative_path=contract.terminal_relative_path,
        terminal_sha256=contract.terminal_sha256,
        policy_sha256=contract.policy_sha256,
        enabled_state_sha256=load_skill_enabled_snapshot(skills_root).state_sha256,
    )

    assert result.accepted is False
    assert result.code == "opencli_disclosure_required"


@pytest.mark.asyncio
async def test_rail_receipt_is_invalid_after_policy_or_state_change(
    tmp_path: Path,
) -> None:
    skills_root, skill_root, manifest = _install_manifest_skill(tmp_path)
    initial_state = b'{"skill_configs":{"opencli-web":{"enabled":true}}}'
    (skills_root / "skills_state.json").write_bytes(initial_state)
    store = DisclosureReceiptStore()
    rail = OpenCLIDisclosureRail(
        scope="main",
        skills_root=skills_root,
        receipt_store=store,
    )
    await rail.after_tool_call(
        _tool_context(
            relative_path=_SITE_TERMINAL,
            skill_root=skill_root,
            content=(skill_root / _SITE_TERMINAL).read_text(encoding="utf-8"),
        )
    )

    manifest["sites"][_SITE]["operations"][_OPERATION]["policy_sha256"] = "9" * 64
    (skill_root / "opencli-runtime.json").write_text(
        json.dumps(manifest),
        encoding="utf-8",
    )
    (skills_root / "skills_state.json").write_bytes(
        b'{"skill_configs":{"opencli-web":{"enabled":false}}}'
    )
    changed_contract = load_terminal_contract(
        skills_root,
        _SITE,
        _OPERATION,
    )
    changed_state = load_skill_enabled_snapshot(skills_root)

    result = store.consume_bound(
        scope="main",
        site=_SITE,
        operation=_OPERATION,
        terminal_relative_path=changed_contract.terminal_relative_path,
        terminal_sha256=changed_contract.terminal_sha256,
        policy_sha256=changed_contract.policy_sha256,
        enabled_state_sha256=changed_state.state_sha256,
    )

    assert result.accepted is False
    assert result.code == "opencli_disclosure_policy_changed"
