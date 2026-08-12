from __future__ import annotations

import re
import shutil
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml
from openjiuwen.core.single_agent.rail.base import AgentCallbackContext
from openjiuwen.core.single_agent.skills.skill_manager import Skill
from openjiuwen.harness.prompts import SystemPromptBuilder
from openjiuwen.harness.prompts.prompt_attachment_manager import (
    PromptAttachmentManager,
)
from openjiuwen.harness.rails import SkillUseRail
from openjiuwen.harness.tools import SkillTool

from jiuwenswarm.agents.harness.common import web_agent as web_agent_module
from jiuwenswarm.agents.harness.common.rails.browser_task_prompt_rail import (
    BrowserTaskPromptRail,
)
from jiuwenswarm.agents.harness.common.rails.web_tool_routing_rail import (
    WebToolRoutingRail,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
BUILTIN_SKILLS_DIR = (
    REPO_ROOT / "jiuwenswarm" / "resources" / "agent" / "workspace" / "skills"
)
MASTER_SKILL_DIR = BUILTIN_SKILLS_DIR / "opencli-web"
XIAOHONGSHU_MODULE_DIR = MASTER_SKILL_DIR / "sites" / "xiaohongshu"
XIAOHONGSHU_MODULE_PATH = "sites/xiaohongshu/index.md"
XIAOHONGSHU_OPERATION_COMMANDS = {
    "operations/account.md": {"login", "whoami"},
    "operations/discovery.md": {"ask", "feed", "search"},
    "operations/notes.md": {
        "comments",
        "download",
        "liked",
        "note",
        "notifications",
        "saved",
        "user",
    },
    "operations/creator-analytics.md": {
        "creator-note-detail",
        "creator-notes",
        "creator-notes-summary",
        "creator-profile",
        "creator-stats",
    },
    "operations/drafts.md": {
        "draft-clear",
        "draft-delete",
        "draft-open",
        "drafts",
    },
    "operations/publishing.md": {"publish"},
    "operations/social-actions.md": {"delete-note", "follow", "unfollow"},
}
XIAOHONGSHU_COMMANDS = set().union(*XIAOHONGSHU_OPERATION_COMMANDS.values())
PUBLISH_OPERATION_PATH = "sites/xiaohongshu/operations/publishing.md"


class _FakeSession:
    def get_session_id(self) -> str:
        return "sess-opencli-web"


class _FakeAgent:
    def __init__(self, builder: SystemPromptBuilder) -> None:
        self.system_prompt_builder = builder
        self.prompt_attachment_manager = PromptAttachmentManager()


class _LocalFileSystem:
    async def read_file(self, path: str):
        try:
            content = Path(path).read_text(encoding="utf-8")
        except OSError as exc:
            return SimpleNamespace(code=1, data=None, message=str(exc))
        return SimpleNamespace(
            code=0,
            data=SimpleNamespace(content=content),
            message="",
        )


class _LocalOperation:
    def __init__(self) -> None:
        self._file_system = _LocalFileSystem()

    def fs(self) -> _LocalFileSystem:
        return self._file_system


def _read_frontmatter(skill_dir: Path) -> dict[str, str]:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    _, frontmatter, _ = text.split("---", 2)
    return yaml.safe_load(frontmatter)


def _install_opencli_fixture(tmp_path: Path) -> Path:
    installed_skills_dir = tmp_path / "workspace" / "skills"
    shutil.copytree(MASTER_SKILL_DIR, installed_skills_dir / "opencli-web")
    return installed_skills_dir


def _extract_markdown_section(prompt: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^{re.escape(heading)}\n\n.*?(?=^# |\Z)",
        prompt,
    )
    assert match is not None
    return match.group(0)


def _extract_labeled_bullets(section: str) -> dict[str, str]:
    return {
        label: body
        for label, body in re.findall(
            r"(?m)^- ([^:]+): (.+)$",
            section,
        )
    }


def test_opencli_web_builtin_resource_has_nested_xiaohongshu_module():
    assert _read_frontmatter(MASTER_SKILL_DIR)["name"] == "opencli-web"
    site_index = (XIAOHONGSHU_MODULE_DIR / "index.md").read_text(encoding="utf-8")
    assert site_index.startswith("# Xiaohongshu\n")
    assert not site_index.startswith("---")
    router_instructions = (MASTER_SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "| Website | Aliases | Domains | Site module |" in router_instructions
    assert XIAOHONGSHU_MODULE_PATH in router_instructions
    assert "shell_type" not in router_instructions

    agent_metadata = yaml.safe_load(
        (MASTER_SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    )
    assert agent_metadata["policy"]["allow_implicit_invocation"] is True
    assert "$opencli-web" in agent_metadata["interface"]["default_prompt"]
    assert not list(MASTER_SKILL_DIR.rglob("*.py"))
    for operation_path in XIAOHONGSHU_OPERATION_COMMANDS:
        assert (XIAOHONGSHU_MODULE_DIR / operation_path).is_file()


def test_opencli_skill_uses_progressive_disclosure_and_complete_command_catalog():
    master = (MASTER_SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    xiaohongshu = (XIAOHONGSHU_MODULE_DIR / "index.md").read_text(
        encoding="utf-8"
    )
    operation_documents = {
        relative_path: (XIAOHONGSHU_MODULE_DIR / relative_path).read_text(
            encoding="utf-8"
        )
        for relative_path in XIAOHONGSHU_OPERATION_COMMANDS
    }

    assert "| Website | Aliases | Domains | Site module |" in master
    assert XIAOHONGSHU_MODULE_PATH in master
    assert "## Operations" in xiaohongshu
    assert "| Operation | Purpose | Commands | Terminal contract |" in xiaohongshu
    assert "general-purpose" not in master
    assert "general-purpose" not in xiaohongshu
    assert "relative_file_path" not in master
    assert "relative_file_path" not in xiaohongshu
    for operation_path in XIAOHONGSHU_OPERATION_COMMANDS:
        assert operation_path in xiaohongshu

    publishing = operation_documents["operations/publishing.md"]
    assert "`opencli xiaohongshu publish " in publishing
    assert "scripts/publish.py" not in publishing
    assert "opencli_adapter_incompatible" not in publishing
    assert "opencli_contract:" not in publishing
    assert "opencli_execute" not in publishing

    social_actions = operation_documents["operations/social-actions.md"]
    assert 'follow "<full-profile-url>"' in social_actions
    assert 'unfollow "<full-profile-url>"' in social_actions
    assert "visible nickname and visible 小红书号" in social_actions
    assert "only as an internal profile ID" in social_actions
    assert "invoke follow exactly once" in social_actions
    assert "invoke unfollow exactly once" in social_actions
    assert "do not retry" in social_actions

    assert "references/" not in master
    assert "references/" not in xiaohongshu
    assert not list((MASTER_SKILL_DIR / "references").glob("*.md"))
    assert not list((XIAOHONGSHU_MODULE_DIR / "references").glob("*.md"))

    documented_commands: set[str] = set()
    for relative_path, expected_commands in XIAOHONGSHU_OPERATION_COMMANDS.items():
        current_commands = set(
            re.findall(
                r"^\| `([a-z-]+)` \| `[a-z_]+` /",
                operation_documents[relative_path],
                flags=re.MULTILINE,
            )
        )
        assert current_commands == expected_commands
        assert documented_commands.isdisjoint(current_commands)
        documented_commands.update(current_commands)
    assert documented_commands == XIAOHONGSHU_COMMANDS
    assert not re.findall(
        r"^\| `([a-z-]+)` \| `[a-z_]+` /",
        xiaohongshu,
        flags=re.MULTILINE,
    )

    milestone_token = "M" + "1"
    for path in MASTER_SKILL_DIR.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".py", ".yaml"}:
            assert milestone_token not in path.read_text(encoding="utf-8")


@pytest.mark.asyncio
async def test_acceptance_trace_reads_native_publish_contract_before_shell_execution(
    tmp_path,
):
    installed_skills_dir = _install_opencli_fixture(tmp_path)
    installed_root = installed_skills_dir / "opencli-web"
    skills = [
        Skill(
            name="opencli-web",
            description=_read_frontmatter(installed_root)["description"],
            directory=installed_root,
        )
    ]
    skill_tool = SkillTool(_LocalOperation(), lambda: skills, language="en")
    trace: list[dict] = []

    master = await skill_tool.invoke({"skill_name": "opencli-web"})
    assert master.success is True
    assert XIAOHONGSHU_MODULE_PATH in master.data["skill_content"]
    trace.append({"tool": "skill_tool", "skill": "opencli-web"})

    site = await skill_tool.invoke(
        {
            "skill_name": "opencli-web",
            "relative_file_path": XIAOHONGSHU_MODULE_PATH,
        }
    )
    assert site.success is True
    assert "operations/publishing.md" in site.data["skill_content"]
    trace.append(
        {
            "tool": "skill_tool",
            "skill": "opencli-web",
            "relative_file_path": XIAOHONGSHU_MODULE_PATH,
        }
    )

    operation = await skill_tool.invoke(
        {
            "skill_name": "opencli-web",
            "relative_file_path": PUBLISH_OPERATION_PATH,
        }
    )
    assert operation.success is True
    assert "`opencli xiaohongshu publish " in operation.data["skill_content"]
    assert "scripts/publish.py" not in operation.data["skill_content"]
    trace.append(
        {
            "tool": "skill_tool",
            "skill": "opencli-web",
            "relative_file_path": PUBLISH_OPERATION_PATH,
        }
    )
    trace.append(
        {
            "tool": "bash",
            "command": "opencli xiaohongshu publish ... -f json",
        }
    )

    assert trace == [
        {"tool": "skill_tool", "skill": "opencli-web"},
        {
            "tool": "skill_tool",
            "skill": "opencli-web",
            "relative_file_path": XIAOHONGSHU_MODULE_PATH,
        },
        {
            "tool": "skill_tool",
            "skill": "opencli-web",
            "relative_file_path": PUBLISH_OPERATION_PATH,
        },
        {
            "tool": "bash",
            "command": "opencli xiaohongshu publish ... -f json",
        },
    ]
    assert all(item["tool"] != "browser_agent" for item in trace)


@pytest.mark.asyncio
async def test_acceptance_trace_discloses_each_needed_operation_sequentially(
    tmp_path,
):
    installed_skills_dir = _install_opencli_fixture(tmp_path)
    installed_root = installed_skills_dir / "opencli-web"
    skill_tool = SkillTool(
        _LocalOperation(),
        lambda: [
            Skill(
                name="opencli-web",
                description=_read_frontmatter(installed_root)["description"],
                directory=installed_root,
            )
        ],
        language="en",
    )

    reads = [
        ("opencli-web", None),
        ("opencli-web", XIAOHONGSHU_MODULE_PATH),
        ("opencli-web", "sites/xiaohongshu/operations/discovery.md"),
        ("opencli-web", "sites/xiaohongshu/operations/notes.md"),
    ]
    contents: list[str] = []
    for skill_name, relative_path in reads:
        arguments = {"skill_name": skill_name}
        if relative_path is not None:
            arguments["relative_file_path"] = relative_path
        result = await skill_tool.invoke(arguments)
        assert result.success is True
        contents.append(result.data["skill_content"])

    assert "`search`" in contents[2]
    assert "`comments`" in contents[3]
    assert [relative_path for _, relative_path in reads[2:]] == [
        "sites/xiaohongshu/operations/discovery.md",
        "sites/xiaohongshu/operations/notes.md",
    ]


@pytest.mark.asyncio
async def test_parent_and_web_agent_rails_define_one_hop_opencli_routing_contract():
    web_builder = SystemPromptBuilder(language="en")
    web_agent = _FakeAgent(web_builder)
    routing_rail = WebToolRoutingRail()
    routing_rail.init(web_agent)

    parent_builder = SystemPromptBuilder(language="en")
    browser_rail = BrowserTaskPromptRail(channel="web")
    browser_rail.system_prompt_builder = parent_builder
    browser_rail.tools = [object()]
    ctx = AgentCallbackContext(
        agent=None,
        inputs=None,
        session=_FakeSession(),
        extra={},
    )

    await routing_rail.before_model_call(ctx)
    await browser_rail.before_model_call(ctx)

    web_prompt = web_builder.build()
    parent_prompt = parent_builder.build()
    opencli_policy = _extract_markdown_section(web_prompt, "# Web Tool Routing Policy")
    browser_policy = _extract_markdown_section(parent_prompt, "## Browser/Web Agent Delegation")
    bullets = _extract_labeled_bullets(opencli_policy)

    assert len(opencli_policy.split()) <= 310
    assert len(browser_policy.split()) <= 160
    assert set(bullets) == {
        "Scope",
        "Disclosure",
        "Execution",
        "Concurrency",
        "Consent",
        "Fallback/retry",
    }
    assert all(
        term in bullets["Scope"]
        for term in (
            "Browser/Web Agent",
            "live-site",
            "`opencli-web`",
            "local Playwright",
            "discussion",
            "local web development",
            "purpose-built non-browser",
            "Do not call `task_tool`",
        )
    )
    assert all(
        term in bullets["Disclosure"]
        for term in (
            "this agent alone",
            "relative_file_path",
            "each operation needed",
            "one at a time",
            "full listed path",
            "No unrelated modules",
            "subagent delegation",
            "filesystem reads",
        )
    )
    assert "exactly one listed operation module" not in web_prompt
    assert all(
        term in bullets["Execution"]
        for term in (
            "adapter capability",
            "not readiness",
            "authentication",
            "consent",
            "exact documented command and arguments",
            "opaque URLs",
            "query strings and fragments",
            "separate shell arguments",
            "unchanged absolute paths",
            'shell_type: "auto"',
        )
    )
    assert all(
        term in bullets["Concurrency"]
        for term in (
            "independent OpenCLI calls",
            "concurrently",
            "journal",
            "tab/session leases",
            "persistent writes",
            "Preserve dependencies",
            "Never overlap OpenCLI and local Playwright",
            "`session_busy`",
            "ambiguous writes",
            "fallback/retry",
        )
    )
    assert "at most one OpenCLI command" not in web_prompt
    assert all(
        term in bullets["Consent"]
        for term in (
            "high",
            "critical",
            "side-effecting",
            "explicit user approval",
            "material non-secret arguments",
            "Parent delegation is not approval",
            "confirmation_required",
            "signed-URL secrets",
            "only at execution",
        )
    )
    assert all(
        term in bullets["Fallback/retry"]
        for term in (
            "local Playwright tools",
            "capability is absent",
            "terminal row permits",
            "adapter process did not start",
            "possible or unclear",
            "fallback_after",
            "COMMAND_EXEC",
            "ARGUMENT",
            "read at most once",
            "never automatically retry writes",
            "fallback_after=none",
            "no Playwright fallback",
            "verify read-only",
        )
    )

    assert "call `task_tool` once" in browser_policy
    assert "owns OpenCLI-first matching" in browser_policy
    assert "main agent must not read `opencli-web`" in browser_policy
    assert "purpose-built non-browser capabilities" in browser_policy
    assert "does not inherit the full parent conversation" in browser_policy
    assert "confirmation_required" in browser_policy
    assert "social_post_" not in browser_policy
    assert "gmail_" not in browser_policy
    assert "hotel_" not in browser_policy
    assert "opencli_execute" not in web_prompt + parent_prompt


def test_web_agent_config_mounts_opencli_skill_and_routing_on_browser_agent(
    monkeypatch,
    tmp_path,
):
    skill_dir = tmp_path / "opencli-web"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: opencli-web\n---\n", encoding="utf-8")
    captured = {}

    def fake_browser_builder(model, **kwargs):
        captured["model"] = model
        captured["kwargs"] = kwargs
        return SimpleNamespace(**kwargs)

    monkeypatch.setattr(web_agent_module, "_build_browser_agent_config", fake_browser_builder)
    model = object()

    web_agent_module.build_web_agent_config(
        model,
        skills_dir=tmp_path,
        workspace="/tmp/workspace",
    )

    rails = captured["kwargs"]["rails"]
    assert captured["model"] is model
    assert len(rails) == 2
    assert isinstance(rails[0], SkillUseRail)
    assert rails[0].enabled_skills == {"opencli-web"}
    assert rails[0].include_tools is True
    assert isinstance(rails[1], WebToolRoutingRail)


@pytest.mark.parametrize("disabled", [[], ["opencli-web"]])
def test_web_agent_config_keeps_plain_playwright_fallback_when_opencli_unavailable(
    monkeypatch,
    tmp_path,
    disabled,
):
    if disabled:
        skill_dir = tmp_path / "opencli-web"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: opencli-web\n---\n", encoding="utf-8")
    captured = {}

    def fake_browser_builder(_model, **kwargs):
        captured.update(kwargs)
        return SimpleNamespace(**kwargs)

    monkeypatch.setattr(web_agent_module, "_build_browser_agent_config", fake_browser_builder)

    web_agent_module.build_web_agent_config(
        object(),
        skills_dir=tmp_path,
        disabled_skills=disabled,
    )

    assert captured["rails"] is None
