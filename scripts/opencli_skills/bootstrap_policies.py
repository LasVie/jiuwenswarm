#!/usr/bin/env python3
"""Bootstrap OpenCLI site capability policies from the frozen catalog.

Every catalog command is exposed through the generated Skill.  The generated
policy adds routing, semantic risk, fallback, file, and sensitive-output data;
it does not maintain a second command execution allowlist.
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Sequence

import yaml

from scripts.opencli_skills.generate import (
    EXCLUDED_ADAPTERS,
    OPENCLI_VERSION,
    CatalogCommand,
    load_catalog,
    load_ownership,
)


_AUTH = re.compile(r"(^|[-_])(login|logout|signin|signout|auth)([-_]|$)")
_DESTRUCTIVE = re.compile(
    r"(^|[-_])(delete|remove|clear|destroy|refund|admin|ban|block|revoke|"
    r"unfollow|cancel)([-_]|$)"
)
_MESSAGE = re.compile(
    r"(^|[-_])(send|message|dm|reply|comment|connect|contact|invite)([-_]|$)"
)
_PUBLIC_WRITE = re.compile(
    r"(^|[-_])(publish|post|submit|create|edit|update|upload)([-_]|$)"
)
_REVERSIBLE = re.compile(
    r"(^|[-_])(like|favorite|favourite|save|pin|follow|subscribe|cart|"
    r"bookmark|daily)([-_]|$)"
)
_LOCAL_WRITE = re.compile(
    r"(^|[-_])(download|export|screenshot|transcript|archive)([-_]|$)"
)
_QUOTA = re.compile(
    r"(^|[-_])(ask|generate|image|deep-research|research|new|chat|"
    r"summarize|translate)([-_]|$)"
)
_ARBITRARY = re.compile(r"(^|[-_])(eval|execute|shell|script|code)([-_]|$)")
_ACCOUNT = re.compile(r"(^|[-_])(whoami|account|profile|me|identity|user-info)([-_]|$)")
_ANALYTICS = re.compile(
    r"(^|[-_])(stats|analytics|metrics|ranking|rankings|trends|insights|"
    r"performance)([-_]|$)"
)
_DISCOVERY = re.compile(
    r"(^|[-_])(search|suggest|random|trending|feed|browse|discover|list|"
    r"catalog|categories|news)([-_]|$)"
)
_FINANCIAL_SITE = {
    "binance",
    "barchart",
    "eastmoney",
    "mercury",
    "sinafinance",
    "tdx",
    "ths",
    "xueqiu",
    "yahoo-finance",
}


def _transport(command: CatalogCommand) -> str:
    if command.strategy == "public" and not command.browser:
        return "public_http"
    if command.strategy == "cookie":
        return "browser_cookie"
    if command.strategy == "intercept":
        return "browser_intercept"
    if command.strategy == "local":
        return "local"
    if command.browser:
        return "browser_dom"
    return "mixed"


def _classify(command: CatalogCommand) -> dict[str, Any]:
    name = command.name
    transport = _transport(command)
    auth = "none" if transport == "public_http" else "required"
    effect = "public_read"
    risk = "low"
    operation = "content"

    if _AUTH.search(name):
        effect, risk, auth, operation = (
            "auth_session_change",
            "high",
            "interactive",
            "authentication",
        )
    elif _ARBITRARY.search(name):
        effect, risk, operation = (
            "arbitrary_execution",
            "critical",
            "arbitrary-execution",
        )
    elif _DESTRUCTIVE.search(name):
        effect, risk, operation = (
            "destructive_or_admin",
            "critical",
            "destructive-actions",
        )
    elif command.access == "write" and command.site in _FINANCIAL_SITE:
        effect, risk, operation = (
            "financial_write",
            "critical",
            "financial-actions",
        )
    elif _MESSAGE.search(name) and command.access == "write":
        effect, risk, operation = (
            "message_send",
            "high",
            "messaging",
        )
    elif _PUBLIC_WRITE.search(name) and command.access == "write":
        effect, risk, operation = (
            "public_write",
            "high",
            "publishing",
        )
    elif _REVERSIBLE.search(name) and command.access == "write":
        effect, risk, operation = (
            "reversible_remote_write",
            "high",
            "account-actions",
        )
    elif _LOCAL_WRITE.search(name):
        effect, risk, operation = (
            "local_write",
            "high",
            "file-operations",
        )
    elif _QUOTA.search(name):
        effect, risk, operation = (
            "quota_consumption",
            "high",
            "generation",
        )
    elif command.access == "write":
        effect, risk, operation = (
            "reversible_remote_write",
            "high",
            "write-actions",
        )
    elif transport != "public_http":
        if _ACCOUNT.search(name):
            effect, operation = "private_account_read", "account"
        else:
            effect, operation = "private_content_read", "private-content"
        risk = "medium"
    elif _ACCOUNT.search(name):
        operation = "account"
    elif _ANALYTICS.search(name):
        operation = "analytics"
    elif _DISCOVERY.search(name):
        operation = "discovery"

    if effect == "public_read" and command.site in _FINANCIAL_SITE:
        notes = "Market-data read only; no trading authority and not investment advice."
    else:
        notes = ""

    retryable_public_read = (
        effect == "public_read"
        and risk == "low"
        and auth == "none"
        and command.access == "read"
    )
    fallback_before = "browser_agent"
    fallback_after = "browser_agent" if retryable_public_read else "none"

    if effect == "arbitrary_execution":
        fallback_before = "none"
        fallback_after = "none"
    if command.site == "xiaohongshu":
        fallback_after = "none"
        if name == "publish":
            effect = "public_write"
            risk = "high"
            auth = "required"
            operation = "publishing"

    sensitive = []
    if effect == "private_account_read":
        sensitive = ["account identifiers"]
    elif effect == "private_content_read":
        sensitive = ["private content", "account identifiers"]
    file_inputs: list[str] = []
    file_outputs: list[str] = []
    if effect == "local_write":
        file_outputs = ["workspace-relative output"]
    if command.access == "write" and _PUBLIC_WRITE.search(name):
        file_inputs = ["workspace-relative input when declared by adapter"]
    if command.site == "xiaohongshu" and name == "publish":
        file_inputs = ["/images/*"]

    return {
        "operation": operation,
        "semantic_effect": effect,
        "risk": risk,
        "auth": auth,
        "transport": transport,
        "fallback_before": fallback_before,
        "fallback_after": fallback_after,
        "file_inputs": file_inputs,
        "file_outputs": file_outputs,
        "sensitive_output": sensitive,
        "notes": notes,
    }


def _special_operation(site: str, command: str, inferred: str) -> str:
    overrides = {
        "wikipedia": {
            "page": "articles",
            "summary": "articles",
            "search": "discovery",
            "random": "discovery",
            "trending": "discovery",
        },
        "google": {
            "news": "public-data",
            "suggest": "public-data",
            "trends": "public-data",
            "search": "web-search",
        },
        "flomo": {
            "login": "authentication",
            "whoami": "account",
            "memos": "memos",
        },
        "xiaohongshu": {
            "login": "account",
            "whoami": "account",
            "ask": "discovery",
            "feed": "discovery",
            "search": "discovery",
            "comments": "notes",
            "download": "notes",
            "liked": "notes",
            "note": "notes",
            "notifications": "notes",
            "saved": "notes",
            "user": "notes",
            "creator-note-detail": "creator-analytics",
            "creator-notes": "creator-analytics",
            "creator-notes-summary": "creator-analytics",
            "creator-profile": "creator-analytics",
            "creator-stats": "creator-analytics",
            "draft-clear": "drafts",
            "draft-delete": "drafts",
            "draft-open": "drafts",
            "drafts": "drafts",
            "publish": "publishing",
            "delete-note": "social-actions",
            "follow": "social-actions",
            "unfollow": "social-actions",
        },
    }
    return overrides.get(site, {}).get(command, inferred)


def _purpose(operation: str) -> str:
    return {
        "account": "Read account identity or account-scoped metadata.",
        "account-actions": "Change reversible account relationship or saved state.",
        "analytics": "Read aggregate metrics, trends, or rankings.",
        "arbitrary-execution": "Adapter entry points that can execute arbitrary input.",
        "articles": "Read encyclopedia pages and summaries.",
        "authentication": "Open, change, or clear an authenticated browser session.",
        "content": "Read site content and metadata.",
        "creator-analytics": "Read creator account and note performance metrics.",
        "destructive-actions": "Delete, remove, revoke, or perform administrative changes.",
        "discovery": "Search, browse, recommend, or discover site content.",
        "drafts": "Read or change local or remote draft state.",
        "file-operations": "Create or download workspace files.",
        "financial-actions": "Financial or reimbursement state changes.",
        "generation": "Generate remote content, start AI work, or consume quota.",
        "memos": "Read private memo content.",
        "messaging": "Send messages, replies, comments, invitations, or contacts.",
        "notes": "Read Xiaohongshu note and notification data.",
        "private-content": "Read content that depends on an authenticated account.",
        "public-data": "Read low-risk public data without browser state.",
        "publishing": "Publish, create, edit, or upload remote content.",
        "social-actions": "Change social relationships or delete published content.",
        "web-search": "Read browser-rendered web search results.",
        "write-actions": "Change remote service state.",
    }.get(operation, f"Use the reviewed {operation} capability boundary.")


def _arg_overrides(site: str, command: str) -> dict[str, Any]:
    overrides: dict[tuple[str, str], dict[str, Any]] = {
        ("wikipedia", "page"): {
            "lang": {"pattern": "^[a-z]{2,3}(?:-[a-z0-9]+)?$"},
            "paragraphs": {"minimum": 0},
        },
        ("wikipedia", "search"): {
            "limit": {"minimum": 1, "maximum": 50},
            "lang": {"pattern": "^[a-z]{2,3}(?:-[a-z0-9]+)?$"},
        },
        ("wikipedia", "trending"): {
            "limit": {"minimum": 1, "maximum": 50},
            "lang": {"pattern": "^[a-z]{2,3}(?:-[a-z0-9]+)?$"},
        },
        ("google", "news"): {
            "limit": {"minimum": 1, "maximum": 100},
            "lang": {"pattern": "^[A-Za-z]{2,3}(?:-[A-Za-z0-9]+)?$"},
            "region": {"pattern": "^[A-Z]{2}$"},
        },
        ("google", "search"): {
            "limit": {"minimum": 1, "maximum": 100},
        },
        ("google", "trends"): {
            "limit": {"minimum": 1, "maximum": 100},
            "region": {"pattern": "^[A-Z]{2}$"},
        },
        ("flomo", "login"): {
            "timeout": {"minimum": 1, "maximum": 1800},
        },
        ("flomo", "memos"): {
            "limit": {"minimum": 1, "maximum": 200},
            "since": {"minimum": 0},
            "slug": {"pattern": "^[A-Za-z0-9_-]{1,256}$"},
        },
    }
    return overrides.get((site, command), {})


def _is_compact_terminal(command_specs: Iterable[dict[str, Any]]) -> bool:
    specs = list(command_specs)
    return len(specs) <= 3 and all(
        spec["semantic_effect"] == "public_read"
        and spec["risk"] == "low"
        and spec["auth"] == "none"
        and spec["transport"] == "public_http"
        and not spec["file_inputs"]
        and not spec["file_outputs"]
        for spec in specs
    )


def bootstrap_policies(
    catalog_path: Path,
    ownership_path: Path,
    output_root: Path,
) -> None:
    catalog = load_catalog(catalog_path)
    load_ownership(ownership_path)
    sites = sorted(
        {
            command.site
            for command in catalog.commands
            if command.site not in EXCLUDED_ADAPTERS
        }
    )
    output_root.mkdir(parents=True, exist_ok=True)
    for site in sites:
        commands = list(catalog.site_commands(site))
        command_specs: dict[str, dict[str, Any]] = {}
        for command in commands:
            spec = _classify(command)
            spec["operation"] = _special_operation(
                site, command.name, spec["operation"]
            )
            overrides = _arg_overrides(site, command.name)
            if overrides:
                spec["arg_overrides"] = overrides
            command_specs[command.name] = spec

        compact = _is_compact_terminal(command_specs.values())
        if compact:
            for spec in command_specs.values():
                spec["operation"] = "public-data"

        grouped: dict[str, list[str]] = defaultdict(list)
        for command_name, spec in command_specs.items():
            grouped[spec["operation"]].append(command_name)
        operations = {
            operation: {
                "purpose": _purpose(operation),
                "commands": sorted(command_names),
            }
            for operation, command_names in sorted(grouped.items())
        }
        domains = sorted(
            {
                str(command.raw["domain"])
                for command in commands
                if command.raw.get("domain")
            }
        )
        policy = {
            "schema_version": 2,
            "catalog_version": f"opencli-{OPENCLI_VERSION}",
            "site": site,
            "display_name": site.replace("-", " ").title(),
            "domains": domains,
            "aliases": [],
            "terminal": "site" if compact else "operation",
            "operations": operations,
            "commands": {name: command_specs[name] for name in sorted(command_specs)},
        }
        destination = output_root / f"{site}.yaml"
        destination.write_text(
            yaml.safe_dump(
                policy,
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False,
                width=1000,
            ),
            encoding="utf-8",
            newline="\n",
        )


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--catalog",
        type=Path,
        default=root / "catalog" / f"opencli-{OPENCLI_VERSION}.json",
    )
    parser.add_argument(
        "--ownership",
        type=Path,
        default=root / "ownership.yaml",
    )
    parser.add_argument("--output", type=Path, default=root / "sites")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    bootstrap_policies(args.catalog, args.ownership, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
