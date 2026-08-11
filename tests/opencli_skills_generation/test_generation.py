from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from scripts.opencli_skills.generate import (
    CATALOG_COMMAND_COUNT,
    CATALOG_SITE_COUNT,
    CatalogCommand,
    CommandPolicy,
    EXCLUDED_ADAPTERS,
    GENERATED_COMMAND_COUNT,
    GENERATED_SITE_COUNT,
    GenerationError,
    OPENCLI_VERSION,
    OperationPolicy,
    _command_invocation,
    _validate_command_policy,
    _validate_site_terminal,
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


def _browser_read_policy(
    *,
    semantic_effect: str,
    risk: str,
    auth: str,
    transport: str,
    strategy: str,
    sensitive_output: tuple[str, ...],
    fallback_after: str,
    fallback_before: str = "browser_agent",
) -> CommandPolicy:
    return CommandPolicy(
        catalog=CatalogCommand(
            raw={
                "site": "example",
                "name": "read",
                "description": "Read an example page.",
                "access": "read",
                "strategy": strategy,
                "browser": True,
                "args": [],
            }
        ),
        operation="content",
        semantic_effect=semantic_effect,
        risk=risk,
        auth=auth,
        transport=transport,
        fallback_before=fallback_before,
        fallback_after=fallback_after,
        file_inputs=(),
        file_outputs=(),
        sensitive_output=sensitive_output,
        notes="",
        args=(),
    )


def _tree_digest(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_private_commands_cannot_fallback_after_dispatch() -> None:
    private = _browser_read_policy(
        semantic_effect="private_content_read",
        risk="medium",
        auth="required",
        transport="browser_cookie",
        strategy="cookie",
        sensitive_output=("private content", "account identifiers"),
        fallback_after="none",
    )

    _validate_command_policy(private)

    with pytest.raises(GenerationError, match="cannot auto-fallback"):
        _validate_command_policy(
            replace(private, fallback_after="browser_agent")
        )


def test_browser_read_commands_cannot_use_a_site_terminal() -> None:
    public = _browser_read_policy(
        semantic_effect="public_read",
        risk="low",
        auth="none",
        transport="browser_dom",
        strategy="public",
        sensitive_output=(),
        fallback_after="browser_agent",
    )
    operation = OperationPolicy(
        slug="content",
        purpose="Read example content.",
        commands=("read",),
    )

    with pytest.raises(GenerationError, match="site-terminal contract"):
        _validate_site_terminal(
            "example",
            {"content": operation},
            {"read": public},
        )
def test_frozen_catalog_matches_pinned_opencli_snapshot() -> None:
    catalog = load_catalog(CATALOG_PATH)

    assert catalog.opencli_version == OPENCLI_VERSION == "1.8.6"
    assert catalog.source_sha256 == (
        "c126b09ea1efe2b059676cdd5f0be1f090e09fe013651889269419ab339aceab"
    )
    assert len(catalog.commands) == CATALOG_COMMAND_COUNT == 1331
    assert (
        len({command.site for command in catalog.commands})
        == (CATALOG_SITE_COUNT)
        == 176
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

    assert len(assigned) == GENERATED_SITE_COUNT == 164
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
        == 1179
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
        raw_site = policies[site_slug]
        assert raw_site["schema_version"] == 2
        assert "review" not in raw_site
        for command in raw_site["commands"].values():
            assert "execution_state" not in command
            assert "executor" not in command
            assert "confirmation" not in command


def test_bilibili_favorite_overrides_incorrect_upstream_access() -> None:
    model = build_generation_model(
        load_catalog(CATALOG_PATH),
        load_ownership(OWNERSHIP_PATH),
        load_policies(POLICY_ROOT),
    )
    site = model.sites["bilibili"]
    favorite = site.command("favorite")

    # Preserve the frozen upstream fact while enforcing the source-audited policy.
    assert favorite.catalog.access == "write"
    assert favorite.operation == "private-content"
    assert favorite.semantic_effect == "private_content_read"
    assert favorite.risk == "medium"
    assert favorite.sensitive_output == (
        "private content",
        "account identifiers",
    )
    assert "favorite" in site.operations["private-content"].commands
    assert "favorite" not in site.operations["account-actions"].commands


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
        "private-content",
        "public-data",
        "web-search",
    }

    # Flomo has only three commands, but they cross auth, private-account and
    # private-content boundaries, so a site-terminal contract is forbidden.
    assert model.sites["flomo"].terminal == "operation"
    assert set(model.sites["flomo"].operations) == {
        "account",
        "authentication",
        "private-content",
    }


def test_xiaohongshu_note_commands_preserve_full_signed_urls() -> None:
    model = build_generation_model(
        load_catalog(CATALOG_PATH),
        load_ownership(OWNERSHIP_PATH),
        load_policies(POLICY_ROOT),
    )
    site = model.sites["xiaohongshu"]

    for command_name in ("note", "comments"):
        command = site.command(command_name)
        invocation = _command_invocation(site, command)
        assert '"<full-note-url-with-xsec-token>"' in invocation
        assert "original full Xiaohongshu note URL containing xsec_token" in (
            command.notes
        )
        assert "never extract or substitute a bare note ID" in command.notes

    download = site.command("download")
    assert '"<full-note-url-with-xsec-token-or-xhslink>"' in (
        _command_invocation(site, download)
    )
    assert "or an xhslink short URL" in download.notes
    assert "never extract or substitute a bare note ID" in download.notes


def test_xiaohongshu_discovery_resolves_unsigned_citations() -> None:
    model = build_generation_model(
        load_catalog(CATALOG_PATH),
        load_ownership(OWNERSHIP_PATH),
        load_policies(POLICY_ROOT),
    )
    site = model.sites["xiaohongshu"]
    ask_notes = site.command("ask").notes

    assert "only when it contains a non-empty xsec_token" in ask_notes
    assert "resolve every unsigned source with search" in ask_notes
    assert "require the returned note ID to match" in ask_notes
    assert "Never expose a bare /explore/<note-id> URL" in ask_notes

    for command_name in ("feed", "search"):
        notes = site.command(command_name).notes
        assert "Preserve every returned note URL unchanged" in notes
        assert "non-empty xsec_token and complete query string" in notes
        assert "never shorten it" in notes


def test_xiaohongshu_social_actions_verify_visible_profile_identity() -> None:
    model = build_generation_model(
        load_catalog(CATALOG_PATH),
        load_ownership(OWNERSHIP_PATH),
        load_policies(POLICY_ROOT),
    )
    site = model.sites["xiaohongshu"]

    for command_name in ("follow", "unfollow"):
        command = site.command(command_name)
        assert '"<full-profile-url>"' in _command_invocation(site, command)
        assert "visible nickname" in command.notes
        assert "visible 小红书号" in command.notes
        assert "only as an internal profile ID" in command.notes
        assert "stop if" in command.notes

    follow_notes = site.command("follow").notes
    assert "normalize only that delimiter to ?" in follow_notes
    assert "invoke follow exactly once" in follow_notes
    assert "separate confirmation before a later unfollow" in follow_notes

    unfollow_notes = site.command("unfollow").notes
    assert "invoke unfollow exactly once" in unfollow_notes
    assert "do not retry" in unfollow_notes
    assert "inspect the visible profile button read-only" in unfollow_notes


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

    assert first_result.site_count == second_result.site_count == 165
    assert first_result.command_count == second_result.command_count == 1179
    assert _tree_digest(first) == _tree_digest(second)

    manifest = json.loads(
        (first / "generated-manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["site_count"] == 165
    assert manifest["command_count"] == 1179
    assert manifest["files"] == {
        relative: digest
        for relative, digest in _tree_digest(first).items()
        if relative != "generated-manifest.json"
    }

    assert not (first / "opencli-runtime.json").exists()

    root_skill = (first / "SKILL.md").read_text(encoding="utf-8")
    assert "| Website | Aliases | Domains | Site module |" in root_skill
    assert "relative_file_path" not in root_skill
    assert "browser_agent" not in root_skill

    terminal_site = (first / "sites" / "apple-podcasts" / "index.md").read_text(
        encoding="utf-8"
    )
    assert not terminal_site.startswith("---")
    assert "`sites/apple-podcasts/index.md`" in terminal_site
    assert "opencli apple-podcasts search" in terminal_site

    routed_site = (first / "sites" / "google" / "index.md").read_text(
        encoding="utf-8"
    )
    routed_operation = (
        first / "sites" / "google" / "operations" / "web-search.md"
    ).read_text(encoding="utf-8")
    assert "`sites/google/operations/web-search.md`" in routed_site
    assert "opencli google search" not in routed_site
    assert "opencli google search" in routed_operation

    generated_markdown = "\n".join(
        path.read_text(encoding="utf-8") for path in first.rglob("*.md")
    )
    assert "opencli_execute" not in generated_markdown
    assert "opencli_contract:" not in generated_markdown
    assert "| Command | State |" not in generated_markdown
    assert "Not available through OpenCLI" not in generated_markdown
    assert not list(first.glob("sites/*/SKILL.md"))

    for site in model.sites.values():
        site_index = first / "sites" / site.slug / "index.md"
        assert site_index.is_file(), site.slug
        if site.terminal == "site":
            assert not (site_index.parent / "operations").exists()
        else:
            for operation in site.operations:
                assert (
                    site_index.parent / "operations" / f"{operation}.md"
                ).is_file()


def test_every_catalog_command_has_an_execution_contract(tmp_path: Path) -> None:
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

    exposed = 0
    for site in model.sites.values():
        for operation in site.operations.values():
            terminal = (
                generated / "sites" / site.slug / "index.md"
                if site.terminal == "site"
                else generated
                / "sites"
                / site.slug
                / "operations"
                / f"{operation.slug}.md"
            )
            content = terminal.read_text(encoding="utf-8")
            for command_name in operation.commands:
                command = site.commands[command_name]
                invocation = _command_invocation(site, command).replace(
                    "|", "\\|"
                )
                assert f"`{invocation}`" in content
                exposed += 1

    assert exposed == 1179


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
    ("site", "command", "effect", "risk"),
    [
        ("google", "search", "public_read", "low"),
        ("flomo", "memos", "private_content_read", "medium"),
        ("zlibrary", "search", "private_content_read", "medium"),
        ("xiaohongshu", "publish", "public_write", "high"),
    ],
)
def test_representative_capabilities_keep_risk_metadata(
    site: str,
    command: str,
    effect: str,
    risk: str,
) -> None:
    model = build_generation_model(
        load_catalog(CATALOG_PATH),
        load_ownership(OWNERSHIP_PATH),
        load_policies(POLICY_ROOT),
    )
    command_policy = model.sites[site].command(command)
    assert command_policy.semantic_effect == effect
    assert command_policy.risk == risk
