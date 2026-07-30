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
from openjiuwen.harness.tools import SkillTool

from jiuwenswarm.agents.harness.common.rails.runtime_prompt_rail import (
    RuntimePromptRail,
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
async def test_web_runtime_prompt_automatically_routes_supported_sites_opencli_first():
    builder = SystemPromptBuilder(language="en")
    rail = RuntimePromptRail(language="en", channel="web")
    rail.init(_FakeAgent(builder))
    ctx = AgentCallbackContext(
        agent=None,
        inputs=None,
        session=_FakeSession(),
        extra={},
    )

    await rail.before_model_call(ctx)

    prompt = builder.build()
    assert "installed and enabled `opencli-web` Skill" in prompt
    assert "do not search for, install, or ask the user to select it" in prompt
    assert "general-purpose" in prompt
    assert "relative_file_path" in prompt
    assert "points back to the site file" in prompt
    assert "otherwise read exactly one listed operation module" in prompt
    assert "Every command listed in that terminal contract is available" in prompt
    assert "exact OpenCLI CLI command documented there" in prompt
    assert "dedicated wrapper" not in prompt
    assert "provable pre-dispatch infrastructure failure" in prompt
    assert "Never run OpenCLI and `browser_agent` concurrently" in prompt
    assert "A listed command grants capability, not user consent" in prompt
    assert "`high` or `critical`" in prompt
    assert "social_post_confirm" in prompt
    assert "must not retry with `browser_agent`" in prompt
    assert '`shell_type: "auto"`' in prompt
    assert "opencli_execute" not in prompt
