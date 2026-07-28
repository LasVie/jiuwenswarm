from __future__ import annotations

import asyncio
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml
from openjiuwen.core.single_agent.skills.skill_manager import Skill
from openjiuwen.core.single_agent.rail.base import AgentCallbackContext
from openjiuwen.harness.prompts import SystemPromptBuilder
from openjiuwen.harness.prompts.prompt_attachment_manager import PromptAttachmentManager
from openjiuwen.harness.tools import SkillTool

from jiuwenswarm.agents.harness.common.rails.runtime_prompt_rail import RuntimePromptRail
from jiuwenswarm.server.runtime.skill.skill_manager import SkillManager


REPO_ROOT = Path(__file__).resolve().parents[3]
BUILTIN_SKILLS_DIR = (
    REPO_ROOT / "jiuwenswarm" / "resources" / "agent" / "workspace" / "skills"
)
MASTER_SKILL_DIR = BUILTIN_SKILLS_DIR / "opencli-web"
XIAOHONGSHU_SKILL_DIR = BUILTIN_SKILLS_DIR / "opencli-xiaohongshu"
PUBLISH_WRAPPER = XIAOHONGSHU_SKILL_DIR / "scripts" / "publish.py"


class _FakeSession:
    def get_session_id(self) -> str:
        return "sess-opencli-m1"


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
    spec.loader.exec_module(module)
    return module


def test_opencli_skills_are_valid_separately_installable_builtins(tmp_path):
    for skill_dir, expected_name in (
        (MASTER_SKILL_DIR, "opencli-web"),
        (XIAOHONGSHU_SKILL_DIR, "opencli-xiaohongshu"),
    ):
        metadata = _read_frontmatter(skill_dir)
        assert metadata["name"] == expected_name
        assert set(metadata) == {"name", "description"}
        assert (skill_dir / "agents" / "openai.yaml").is_file()

    manager = SkillManager(workspace_dir=str(tmp_path / "workspace"))
    master_result = asyncio.run(
        manager.handle_skills_install_builtin({"name": "opencli-web"})
    )
    assert master_result["success"] is True
    assert not (tmp_path / "workspace" / "skills" / "opencli-xiaohongshu").exists()

    site_result = asyncio.run(
        manager.handle_skills_install_builtin({"name": "opencli-xiaohongshu"})
    )
    assert site_result["success"] is True
    assert (tmp_path / "workspace" / "skills" / "opencli-web").is_dir()
    assert (tmp_path / "workspace" / "skills" / "opencli-xiaohongshu").is_dir()


def test_opencli_skill_descriptions_support_progressive_disclosure():
    master = (MASTER_SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    xiaohongshu = (XIAOHONGSHU_SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

    assert "any task involving a live website" in master
    assert "opencli-xiaohongshu" in master
    assert "browser_agent" in master
    assert "opencli-web" in xiaohongshu
    assert "social_post_confirm" in xiaohongshu
    assert "scripts/publish.py" in xiaohongshu


@pytest.mark.asyncio
async def test_m1_acceptance_trace_reads_both_skills_then_invokes_opencli(
    tmp_path,
):
    manager = SkillManager(workspace_dir=str(tmp_path / "workspace"))
    for name in ("opencli-web", "opencli-xiaohongshu"):
        installed = await manager.handle_skills_install_builtin({"name": name})
        assert installed["success"] is True

    installed_skills_dir = tmp_path / "workspace" / "skills"
    skills = [
        Skill(
            name=name,
            description=_read_frontmatter(installed_skills_dir / name)["description"],
            directory=installed_skills_dir / name,
        )
        for name in ("opencli-web", "opencli-xiaohongshu")
    ]
    skill_tool = SkillTool(_LocalOperation(), lambda: skills, language="en")
    trace: list[dict] = []

    master = await skill_tool.invoke({"skill_name": "opencli-web"})
    assert master.success is True
    assert "opencli-xiaohongshu" in master.data["skill_content"]
    trace.append({"tool": "skill_tool", "skill": "opencli-web"})

    site = await skill_tool.invoke({"skill_name": "opencli-xiaohongshu"})
    assert site.success is True
    assert "scripts/publish.py" in site.data["skill_content"]
    trace.append({"tool": "skill_tool", "skill": "opencli-xiaohongshu"})

    completed, result = _run_wrapper(
        tmp_path,
        {
            "title": "M1 轨迹",
            "content": "主 Skill 到站点 Skill 再到 OpenCLI",
            "card_text": "fake adapter",
        },
        wrapper=(
            installed_skills_dir
            / "opencli-xiaohongshu"
            / "scripts"
            / "publish.py"
        ),
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
        {"tool": "skill_tool", "skill": "opencli-xiaohongshu"},
        {"tool": "opencli", "site": "xiaohongshu", "command": "publish"},
    ]
    assert all(item["tool"] != "browser_agent" for item in trace)


@pytest.mark.asyncio
async def test_web_runtime_prompt_routes_supported_sites_opencli_first():
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
    assert "read `opencli-web` first" in prompt
    assert "matching OpenCLI site skill" in prompt
    assert "provable pre-execution infrastructure failure" in prompt
    assert "Never run OpenCLI and `browser_agent` concurrently" in prompt
    assert "social_post_confirm" in prompt
    assert "must not retry with `browser_agent`" in prompt


def test_publish_wrapper_defaults_to_draft_and_preserves_argument_boundaries(tmp_path):
    content = "正文; echo SHOULD_NOT_RUN"
    completed, result = _run_wrapper(
        tmp_path,
        {
            "title": "M1 测试",
            "content": content,
            "images": [r"C:\media\one image.png"],
            "topics": ["OpenCLI", "智能体"],
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
    assert argv[argv.index("--topics") + 1] == "OpenCLI,智能体"
    assert "SHOULD_NOT_RUN" not in completed.stderr


def test_publish_wrapper_consumes_confirmation_once_and_never_browser_falls_back(
    tmp_path,
):
    confirmation_dir = tmp_path / "confirmations"
    payload = {
        "title": "M1 发布",
        "content": "只用于 fake OpenCLI 的确定性测试",
        "card_text": ["第一页", "第二页"],
        "mode": "publish",
        "confirmation": {
            "action": "social_post_confirm",
            "id": "confirm-m1-001",
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
    assert first["result"]["argv"][
        first["result"]["argv"].index("--draft") + 1
    ] == "false"
    assert second_completed.returncode != 0
    assert second["ok"] is False
    assert second["error"]["code"] == "confirmation_already_used"
    assert second["attempted"] is False
    assert second["fallback_allowed"] is False
    markers = list(confirmation_dir.glob("*.json"))
    assert len(markers) == 1
    marker_text = markers[0].read_text(encoding="utf-8")
    assert "confirm-m1-001" not in marker_text
    assert payload["content"] not in marker_text


def test_publish_wrapper_rejects_publish_without_final_confirmation(tmp_path):
    completed, result = _run_wrapper(
        tmp_path,
        {
            "title": "M1 发布",
            "content": "不得在缺少最终确认时发布",
            "card_text": "确认门测试",
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
                "title": "M1 草稿",
                "content": "基础设施失败测试",
                "card_text": "测试卡片",
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
            "title": "M1 草稿",
            "content": "OpenCLI 已启动后的失败测试",
            "card_text": "测试卡片",
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
        assert Path(runner[1]).as_posix().endswith(
            "/node_modules/@jackwener/opencli/dist/src/main.js"
        )
