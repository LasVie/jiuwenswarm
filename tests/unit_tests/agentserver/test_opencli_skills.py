from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml
from openjiuwen.core.single_agent.rail.base import AgentCallbackContext
from openjiuwen.core.single_agent.skills.skill_manager import Skill
from openjiuwen.harness.prompts import SystemPromptBuilder
from openjiuwen.harness.prompts.prompt_attachment_manager import PromptAttachmentManager
from openjiuwen.harness.tools import SkillTool

from jiuwenswarm.agents.harness.common.rails.runtime_prompt_rail import (
    RuntimePromptRail,
)
from jiuwenswarm.common.utils import CopyDiffResult, _install_default_builtin_skills


REPO_ROOT = Path(__file__).resolve().parents[3]
BUILTIN_SKILLS_DIR = (
    REPO_ROOT / "jiuwenswarm" / "resources" / "agent" / "workspace" / "skills"
)
MASTER_SKILL_DIR = BUILTIN_SKILLS_DIR / "opencli-web"
XIAOHONGSHU_MODULE_DIR = MASTER_SKILL_DIR / "sites" / "xiaohongshu"
XIAOHONGSHU_MODULE_PATH = "sites/xiaohongshu/SKILL.md"
PUBLISH_WRAPPER = XIAOHONGSHU_MODULE_DIR / "scripts" / "publish.py"
XIAOHONGSHU_COMMANDS = {
    "ask",
    "comments",
    "creator-note-detail",
    "creator-notes",
    "creator-notes-summary",
    "creator-profile",
    "creator-stats",
    "delete-note",
    "download",
    "draft-clear",
    "draft-delete",
    "draft-open",
    "drafts",
    "feed",
    "follow",
    "liked",
    "login",
    "note",
    "notifications",
    "publish",
    "saved",
    "search",
    "unfollow",
    "user",
    "whoami",
}


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


def _install_defaults(tmp_path: Path) -> Path:
    installed_skills_dir = tmp_path / "workspace" / "skills"
    _install_default_builtin_skills(
        builtin_dir=BUILTIN_SKILLS_DIR,
        user_skills_dir=installed_skills_dir,
        overwrite=False,
        cumulative_diff=CopyDiffResult([], [], []),
    )
    return installed_skills_dir


def _write_fake_opencli(path: Path, *, exit_code: int = 0) -> None:
    path.write_text(
        "import json\n"
        "import sys\n"
        "sys.stdout.reconfigure(encoding='utf-8')\n"
        "print(json.dumps({'argv': sys.argv[1:]}, ensure_ascii=False))\n"
        f"raise SystemExit({exit_code})\n",
        encoding="utf-8",
    )


def _run_wrapper(
    tmp_path: Path,
    payload: dict,
    *,
    fake_exit_code: int = 0,
    confirmation_dir: Path | None = None,
    wrapper: Path = PUBLISH_WRAPPER,
) -> tuple[subprocess.CompletedProcess[str], dict]:
    fake_opencli = tmp_path / f"fake_opencli_{fake_exit_code}.py"
    _write_fake_opencli(fake_opencli, exit_code=fake_exit_code)
    payload_path = tmp_path / "payload.json"
    payload_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    command = [
        sys.executable,
        str(wrapper),
        "--payload",
        str(payload_path),
        "--opencli-bin",
        sys.executable,
        "--opencli-prefix-arg",
        str(fake_opencli),
    ]
    if confirmation_dir is not None:
        command.extend(["--confirmation-dir", str(confirmation_dir)])

    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        shell=False,
    )
    return completed, json.loads(completed.stdout)


def _load_publish_wrapper_module():
    module_name = "_jiuwenswarm_opencli_xiaohongshu_publish_test"
    spec = importlib.util.spec_from_file_location(module_name, PUBLISH_WRAPPER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


def test_opencli_web_is_preinstalled_with_nested_xiaohongshu_module(tmp_path):
    assert _read_frontmatter(MASTER_SKILL_DIR)["name"] == "opencli-web"
    assert _read_frontmatter(XIAOHONGSHU_MODULE_DIR)["name"] == "opencli-xiaohongshu"

    agent_metadata = yaml.safe_load(
        (MASTER_SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    )
    assert agent_metadata["policy"]["allow_implicit_invocation"] is True
    assert "$opencli-web" in agent_metadata["interface"]["default_prompt"]

    installed_skills_dir = _install_defaults(tmp_path)
    installed_root = installed_skills_dir / "opencli-web"
    assert installed_root.is_dir()
    assert (installed_root / XIAOHONGSHU_MODULE_PATH).is_file()
    assert not (installed_skills_dir / "opencli-xiaohongshu").exists()

    state = json.loads(
        (installed_skills_dir / "skills_state.json").read_text(encoding="utf-8")
    )
    installed_names = {
        item["name"]
        for item in state["installed_plugins"]
        if isinstance(item, dict) and "name" in item
    }
    assert "opencli-web" in installed_names
    assert "opencli-xiaohongshu" not in installed_names
    assert (
        state.get("skill_configs", {}).get("opencli-web", {"enabled": True})["enabled"]
        is True
    )


def test_opencli_skill_uses_progressive_disclosure_and_complete_command_catalog():
    master = (MASTER_SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    xiaohongshu = (XIAOHONGSHU_MODULE_DIR / "SKILL.md").read_text(encoding="utf-8")
    catalog = (XIAOHONGSHU_MODULE_DIR / "references" / "command-catalog.md").read_text(
        encoding="utf-8"
    )

    assert "any task involving a live website" in master
    assert XIAOHONGSHU_MODULE_PATH in master
    assert "relative_file_path" in master
    assert "browser_agent" in master
    assert "opencli-web" in xiaohongshu
    assert "social_post_confirm" in xiaohongshu
    assert "scripts/publish.py" in xiaohongshu

    documented_commands = set(
        re.findall(r"^\| `([a-z-]+)` \|", catalog, flags=re.MULTILINE)
    )
    assert documented_commands == XIAOHONGSHU_COMMANDS

    milestone_token = "M" + "1"
    for path in MASTER_SKILL_DIR.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".py", ".yaml"}:
            assert milestone_token not in path.read_text(encoding="utf-8")


@pytest.mark.asyncio
async def test_acceptance_trace_reads_nested_site_module_then_invokes_opencli(tmp_path):
    installed_skills_dir = _install_defaults(tmp_path)
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
    assert "scripts/publish.py" in site.data["skill_content"]
    trace.append(
        {
            "tool": "skill_tool",
            "skill": "opencli-web",
            "relative_file_path": XIAOHONGSHU_MODULE_PATH,
        }
    )

    completed, result = _run_wrapper(
        tmp_path,
        {
            "title": "Route test",
            "content": "Main Skill to site module to OpenCLI",
            "card_text": "fake adapter",
        },
        wrapper=installed_root / "sites" / "xiaohongshu" / "scripts" / "publish.py",
    )
    assert completed.returncode == 0
    trace.append(
        {
            "tool": "opencli",
            "site": result["result"]["argv"][0],
            "command": result["result"]["argv"][1],
        }
    )

    assert trace == [
        {"tool": "skill_tool", "skill": "opencli-web"},
        {
            "tool": "skill_tool",
            "skill": "opencli-web",
            "relative_file_path": XIAOHONGSHU_MODULE_PATH,
        },
        {"tool": "opencli", "site": "xiaohongshu", "command": "publish"},
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
    assert "`opencli-web` is preinstalled by default" in prompt
    assert "do not search for, install, or ask the user to select it" in prompt
    assert "relative_file_path" in prompt
    assert "provable pre-execution infrastructure failure" in prompt
    assert "Never run OpenCLI and `browser_agent` concurrently" in prompt
    assert "social_post_confirm" in prompt
    assert "must not retry with `browser_agent`" in prompt


def test_publish_wrapper_defaults_to_draft_and_preserves_argument_boundaries(tmp_path):
    content = "Body; echo SHOULD_NOT_RUN"
    completed, result = _run_wrapper(
        tmp_path,
        {
            "title": "Draft test",
            "content": content,
            "images": [r"C:\media\one image.png"],
            "topics": ["OpenCLI", "agents"],
        },
    )

    assert completed.returncode == 0
    assert result["ok"] is True
    assert result["mode"] == "draft"
    assert result["attempted"] is True
    assert result["fallback_allowed"] is False
    argv = result["result"]["argv"]
    assert argv[:3] == ["xiaohongshu", "publish", content]
    assert argv[argv.index("--draft") + 1] == "true"
    assert argv[argv.index("--images") + 1] == r"C:\media\one image.png"
    assert argv[argv.index("--topics") + 1] == "OpenCLI,agents"
    assert "SHOULD_NOT_RUN" not in completed.stderr


def test_publish_wrapper_consumes_confirmation_once_and_never_browser_falls_back(
    tmp_path,
):
    confirmation_dir = tmp_path / "confirmations"
    payload = {
        "title": "Publish test",
        "content": "Deterministic fake OpenCLI test",
        "card_text": ["first card", "second card"],
        "mode": "publish",
        "confirmation": {
            "action": "social_post_confirm",
            "id": "confirm-opencli-001",
        },
    }

    first_completed, first = _run_wrapper(
        tmp_path,
        payload,
        confirmation_dir=confirmation_dir,
    )
    second_completed, second = _run_wrapper(
        tmp_path,
        payload,
        confirmation_dir=confirmation_dir,
    )

    assert first_completed.returncode == 0
    assert first["ok"] is True
    assert first["mode"] == "publish"
    assert (
        first["result"]["argv"][first["result"]["argv"].index("--draft") + 1] == "false"
    )
    assert second_completed.returncode != 0
    assert second["ok"] is False
    assert second["error"]["code"] == "confirmation_already_used"
    assert second["attempted"] is False
    assert second["fallback_allowed"] is False
    markers = list(confirmation_dir.glob("*.json"))
    assert len(markers) == 1
    marker_text = markers[0].read_text(encoding="utf-8")
    assert "confirm-opencli-001" not in marker_text
    assert payload["content"] not in marker_text


def test_publish_wrapper_rejects_publish_without_final_confirmation(tmp_path):
    completed, result = _run_wrapper(
        tmp_path,
        {
            "title": "Publish test",
            "content": "Do not publish without final confirmation",
            "card_text": "confirmation gate",
            "mode": "publish",
        },
    )

    assert completed.returncode != 0
    assert result["ok"] is False
    assert result["error"]["code"] == "confirmation_required"
    assert result["attempted"] is False
    assert result["fallback_allowed"] is False


def test_publish_wrapper_allows_fallback_only_before_opencli_starts(tmp_path):
    payload_path = tmp_path / "payload.json"
    payload_path.write_text(
        json.dumps(
            {
                "title": "Draft test",
                "content": "Infrastructure failure test",
                "card_text": "test card",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    missing = tmp_path / "missing-opencli"
    completed = subprocess.run(
        [
            sys.executable,
            str(PUBLISH_WRAPPER),
            "--payload",
            str(payload_path),
            "--opencli-bin",
            str(missing),
        ],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        shell=False,
    )
    result = json.loads(completed.stdout)

    assert completed.returncode != 0
    assert result["ok"] is False
    assert result["attempted"] is False
    assert result["fallback_allowed"] is True
    assert result["error"]["code"] == "opencli_not_found"


def test_publish_wrapper_blocks_fallback_after_opencli_process_starts(tmp_path):
    completed, result = _run_wrapper(
        tmp_path,
        {
            "title": "Draft test",
            "content": "Failure after OpenCLI starts",
            "card_text": "test card",
        },
        fake_exit_code=7,
    )

    assert completed.returncode == 7
    assert result["ok"] is False
    assert result["attempted"] is True
    assert result["fallback_allowed"] is False
    assert result["error"]["code"] == "opencli_failed"


@pytest.mark.skipif(
    shutil.which("opencli") is None,
    reason="OpenCLI is not installed in this test environment",
)
def test_publish_wrapper_resolves_installed_opencli_without_a_shell():
    wrapper = _load_publish_wrapper_module()

    runner = wrapper._resolve_opencli_argv("opencli")

    assert runner
    assert Path(runner[0]).suffix.lower() not in {".cmd", ".bat", ".ps1"}
    resolved_launcher = Path(shutil.which("opencli") or "")
    if os.name == "nt" and resolved_launcher.suffix.lower() in {".cmd", ".bat"}:
        assert Path(runner[0]).name.lower() == "node.exe"
        assert (
            Path(runner[1])
            .as_posix()
            .endswith("/node_modules/@jackwener/opencli/dist/src/main.js")
        )
