from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.opencli_skills.generate import (
    CATALOG_COMMAND_COUNT,
    CATALOG_SITE_COUNT,
    EXCLUDED_ADAPTERS,
    GENERATED_COMMAND_COUNT,
    GENERATED_SITE_COUNT,
    OPENCLI_VERSION,
    build_generation_model,
    generate,
    load_catalog,
    load_ownership,
    load_policies,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
INPUT_ROOT = REPO_ROOT / "scripts" / "opencli_skills"
CATALOG_PATH = INPUT_ROOT / "catalog" / f"opencli-{OPENCLI_VERSION}.json"
POLICY_ROOT = INPUT_ROOT / "sites"
OWNERSHIP_PATH = INPUT_ROOT / "ownership.yaml"
BUILTIN_SKILL_ROOT = (
    REPO_ROOT
    / "jiuwenswarm"
    / "resources"
    / "agent"
    / "workspace"
    / "skills"
    / "opencli-web"
)


def _tree_digest(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_frozen_catalog_matches_reviewed_opencli_release() -> None:
    catalog = load_catalog(CATALOG_PATH)

    assert catalog.opencli_version == OPENCLI_VERSION == "1.8.6"
    assert catalog.source_sha256 == (
        "310a143b41ea677de88f05bfd9c525e3b1e19c14f88d0377356508b161adf3e6"
    )
    assert len(catalog.commands) == CATALOG_COMMAND_COUNT == 1275
    assert (
        len({command.site for command in catalog.commands})
        == (CATALOG_SITE_COUNT)
        == 173
    )
    assert (
        catalog.canonical_sha256
        == hashlib.sha256(
            json.dumps(
                catalog.raw_commands,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
    )


def test_ownership_is_exact_and_unique() -> None:
    catalog = load_catalog(CATALOG_PATH)
    ownership = load_ownership(OWNERSHIP_PATH)
    assigned = [site for owner in ownership.owners.values() for site in owner]
    expected = sorted(
        {
            command.site
            for command in catalog.commands
            if command.site not in EXCLUDED_ADAPTERS and command.site != "xiaohongshu"
        }
    )

    assert len(assigned) == GENERATED_SITE_COUNT == 161
    assert len(set(assigned)) == len(assigned)
    assert sorted(assigned) == expected
    assert ownership.completed == ("xiaohongshu",)
    assert set(ownership.excluded) == EXCLUDED_ADAPTERS


def test_policies_cover_each_catalog_command_exactly_once() -> None:
    catalog = load_catalog(CATALOG_PATH)
    ownership = load_ownership(OWNERSHIP_PATH)
    policies = load_policies(POLICY_ROOT)
    model = build_generation_model(catalog, ownership, policies)

    assert len(model.sites) == GENERATED_SITE_COUNT + 1
    assert (
        sum(
            len(operation.commands)
            for site in model.sites.values()
            for operation in site.operations.values()
        )
        == GENERATED_COMMAND_COUNT + 25
        == 1123
    )

    for site_slug, site in model.sites.items():
        catalog_names = {
            command.name for command in catalog.commands if command.site == site_slug
        }
        covered = [
            command
            for operation in site.operations.values()
            for command in operation.commands
        ]
        assert len(covered) == len(set(covered)), site_slug
        assert set(covered) == catalog_names, site_slug


def test_physical_depth_follows_safety_boundary_not_command_count_alone() -> None:
    model = build_generation_model(
        load_catalog(CATALOG_PATH),
        load_ownership(OWNERSHIP_PATH),
        load_policies(POLICY_ROOT),
    )

    assert model.sites["rest-countries"].terminal == "site"
    assert set(model.sites["rest-countries"].operations) == {"public-data"}

    assert model.sites["wikipedia"].terminal == "operation"
    assert set(model.sites["wikipedia"].operations) == {
        "articles",
        "discovery",
    }
    assert model.sites["google"].terminal == "operation"
    assert set(model.sites["google"].operations) == {
        "public-data",
        "web-search",
    }

    # Flomo has only three commands, but they cross auth, private-account and
    # private-content boundaries, so a site-terminal contract is forbidden.
    assert model.sites["flomo"].terminal == "operation"
    assert set(model.sites["flomo"].operations) == {
        "account",
        "authentication",
        "memos",
    }


def test_generation_is_deterministic_and_links_are_complete(
    tmp_path: Path,
) -> None:
    model = build_generation_model(
        load_catalog(CATALOG_PATH),
        load_ownership(OWNERSHIP_PATH),
        load_policies(POLICY_ROOT),
    )
    first = tmp_path / "first"
    second = tmp_path / "second"

    first_result = generate(
        model,
        output_root=first,
        manual_skill_root=BUILTIN_SKILL_ROOT,
    )
    second_result = generate(
        model,
        output_root=second,
        manual_skill_root=BUILTIN_SKILL_ROOT,
    )

    assert first_result.site_count == second_result.site_count == 162
    assert first_result.command_count == second_result.command_count == 1123
    assert _tree_digest(first) == _tree_digest(second)

    manifest = json.loads(
        (first / "generated-manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["site_count"] == 162
    assert manifest["command_count"] == 1123
    assert manifest["files"] == {
        relative: digest
        for relative, digest in _tree_digest(first).items()
        if relative != "generated-manifest.json"
    }

    runtime = json.loads((first / "opencli-runtime.json").read_text(encoding="utf-8"))
    assert runtime["catalog"]["source_sha256"] == (
        "310a143b41ea677de88f05bfd9c525e3b1e19c14f88d0377356508b161adf3e6"
    )
    assert len(runtime["sites"]) == 162

    for site in model.sites.values():
        site_skill = first / "sites" / site.slug / "SKILL.md"
        assert site_skill.is_file(), site.slug
        if site.terminal == "site":
            assert not (site_skill.parent / "operations").exists()
        else:
            for operation in site.operations:
                assert (site_skill.parent / "operations" / f"{operation}.md").is_file()


def test_full_generation_matches_checked_in_tree(tmp_path: Path) -> None:
    model = build_generation_model(
        load_catalog(CATALOG_PATH),
        load_ownership(OWNERSHIP_PATH),
        load_policies(POLICY_ROOT),
    )
    generated = tmp_path / "opencli-web"
    generate(
        model,
        output_root=generated,
        manual_skill_root=BUILTIN_SKILL_ROOT,
    )

    expected = _tree_digest(generated)
    actual = _tree_digest(BUILTIN_SKILL_ROOT)
    assert actual == expected


@pytest.mark.parametrize(
    ("site", "command", "expected_state"),
    [
        ("wikipedia", "search", "enabled"),
        ("google", "news", "enabled"),
        ("google", "search", "disabled"),
        ("flomo", "memos", "quarantined"),
        ("zlibrary", "search", "quarantined"),
        ("xiaohongshu", "publish", "custom"),
    ],
)
def test_representative_execution_states(
    site: str,
    command: str,
    expected_state: str,
) -> None:
    model = build_generation_model(
        load_catalog(CATALOG_PATH),
        load_ownership(OWNERSHIP_PATH),
        load_policies(POLICY_ROOT),
    )
    command_policy = model.sites[site].command(command)
    assert command_policy.execution_state == expected_state


def test_reviewed_public_reads_exclude_credential_gated_false_positives() -> None:
    model = build_generation_model(
        load_catalog(CATALOG_PATH),
        load_ownership(OWNERSHIP_PATH),
        load_policies(POLICY_ROOT),
    )
    enabled = {
        f"{site.slug}/{command.name}"
        for site in model.sites.values()
        for command in site.commands.values()
        if command.execution_state == "enabled"
    }

    # The OpenCLI 1.8.6 adapter-source audit found 254 genuinely public,
    # browser-free reads. The generated catalog metadata alone overstates this
    # boundary for credential-gated APIs and misses four name-heuristic cases.
    assert len(enabled) == 254
    assert (
        hashlib.sha256(("\n".join(sorted(enabled)) + "\n").encode()).hexdigest()
        == "396899309f5d5251b5a7550f53f8ed8305769eac30bcf75811e5ced6ad30e977"
    )
    assert {
        "dockerhub/image",
        "hackernews/ask",
        "hackernews/new",
        "lesswrong/new",
    } <= enabled
    assert enabled.isdisjoint(
        {
            "confluence/page",
            "confluence/search",
            "jira/attachments",
            "jira/comments",
            "jira/issue",
            "jira/links",
            "jira/search",
            "paperreview/review",
            "spotify/search",
            "spotify/status",
            "weread-official/book",
            "weread-official/discover",
            "weread-official/list-apis",
            "weread-official/notes",
            "weread-official/readdata",
            "weread-official/review",
            "weread-official/search",
            "weread-official/shelf",
        }
    )

    paper_review = model.sites["paperreview"].command("review")
    assert paper_review.semantic_effect == "private_content_read"
    assert paper_review.auth == "required"
    assert paper_review.risk == "high"
    assert paper_review.execution_state == "disabled"
    assert paper_review.fallback_after == "none"

    jira_issue = model.sites["jira"].command("issue")
    assert jira_issue.semantic_effect == "private_content_read"
    assert jira_issue.auth == "required"
    assert jira_issue.execution_state == "quarantined"
    assert jira_issue.fallback_before == "none"
    assert jira_issue.fallback_after == "none"

    confluence_page = model.sites["confluence"].command("page")
    assert confluence_page.semantic_effect == "private_content_read"
    assert confluence_page.auth == "required"
    assert confluence_page.execution_state == "disabled"

    spotify_status = model.sites["spotify"].command("status")
    assert spotify_status.semantic_effect == "private_account_read"
    assert spotify_status.auth == "required"
    assert spotify_status.transport == "mixed"
    assert spotify_status.execution_state == "disabled"

    weread_notes = model.sites["weread-official"].command("notes")
    assert weread_notes.semantic_effect == "private_content_read"
    assert weread_notes.auth == "required"
    assert weread_notes.execution_state == "disabled"
