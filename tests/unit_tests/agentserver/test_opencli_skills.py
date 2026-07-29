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
from jiuwenswarm.common import utils as workspace_utils
from jiuwenswarm.common.utils import (
    CopyDiffResult,
    _install_default_builtin_skills,
    bootstrap_workspace,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
BUILTIN_SKILLS_DIR = (
    REPO_ROOT / "jiuwenswarm" / "resources" / "agent" / "workspace" / "skills"
)
MASTER_SKILL_DIR = BUILTIN_SKILLS_DIR / "opencli-web"
XIAOHONGSHU_MODULE_DIR = MASTER_SKILL_DIR / "sites" / "xiaohongshu"
XIAOHONGSHU_MODULE_PATH = "sites/xiaohongshu/SKILL.md"
PUBLISH_WRAPPER = XIAOHONGSHU_MODULE_DIR / "scripts" / "publish.py"
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


def _install_defaults(tmp_path: Path) -> Path:
    installed_skills_dir = tmp_path / "workspace" / "skills"
    _install_default_builtin_skills(
        builtin_dir=BUILTIN_SKILLS_DIR,
        user_skills_dir=installed_skills_dir,
        overwrite=False,
        cumulative_diff=CopyDiffResult([], [], []),
    )
    return installed_skills_dir


def _write_fake_opencli(
    path: Path,
    *,
    exit_code: int = 0,
    stderr_text: str = "",
) -> None:
    path.write_text(
        "import json\n"
        "import sys\n"
        "sys.stdout.reconfigure(encoding='utf-8')\n"
        "sys.stderr.reconfigure(encoding='utf-8')\n"
        "print(json.dumps({'argv': sys.argv[1:]}, ensure_ascii=False))\n"
        f"sys.stderr.write({json.dumps(stderr_text, ensure_ascii=False)})\n"
        f"raise SystemExit({exit_code})\n",
        encoding="utf-8",
    )


def _run_wrapper(
    tmp_path: Path,
    payload: dict,
    *,
    fake_exit_code: int = 0,
    fake_stderr: str = "",
    confirmation_dir: Path | None = None,
    wrapper: Path = PUBLISH_WRAPPER,
) -> tuple[subprocess.CompletedProcess[str], dict]:
    fake_opencli = tmp_path / f"fake_opencli_{fake_exit_code}.py"
    _write_fake_opencli(
        fake_opencli,
        exit_code=fake_exit_code,
        stderr_text=fake_stderr,
    )
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
        env={
            **os.environ,
            "JIUWENSWARM_OPENCLI_DAEMON_STATUS_URL": "http://127.0.0.1:1/status",
        },
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
    router_instructions = (MASTER_SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert '`shell_type: "auto"`' in router_instructions
    assert "Do not force `bash` or `sh`" in router_instructions

    agent_metadata = yaml.safe_load(
        (MASTER_SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    )
    assert agent_metadata["policy"]["allow_implicit_invocation"] is True
    assert "$opencli-web" in agent_metadata["interface"]["default_prompt"]

    installed_skills_dir = _install_defaults(tmp_path)
    installed_root = installed_skills_dir / "opencli-web"
    assert installed_root.is_dir()
    assert (installed_root / XIAOHONGSHU_MODULE_PATH).is_file()
    assert (installed_root / "scripts" / "opencli_runtime.py").is_file()
    for operation_path in XIAOHONGSHU_OPERATION_COMMANDS:
        assert (installed_root / "sites" / "xiaohongshu" / operation_path).is_file()
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


def test_existing_workspace_startup_reconciles_missing_default_skill(
    tmp_path,
    monkeypatch,
):
    workspace_dir = tmp_path / "existing-user-workspace"
    config_file = workspace_dir / "config" / "config.yaml"
    installed_skills_dir = workspace_dir / "agent" / "workspace" / "skills"
    config_file.parent.mkdir(parents=True)
    installed_skills_dir.mkdir(parents=True)
    config_file.write_text("preferred_language: zh\n", encoding="utf-8")

    for skill_name in ("skill-creator", "swarmskill-creator"):
        skill_dir = installed_skills_dir / skill_name
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {skill_name}\n---\nuser-owned sentinel\n",
            encoding="utf-8",
        )

    state_file = installed_skills_dir / "skills_state.json"
    state_file.write_text(
        json.dumps(
            {
                "marketplaces": [{"name": "preserved-marketplace"}],
                "installed_plugins": [
                    {"name": "skill-creator", "source": "builtin"},
                    {"name": "swarmskill-creator", "source": "builtin"},
                ],
                "local_skills": [{"name": "preserved-local-skill"}],
                "skill_configs": {"opencli-web": {"enabled": False}},
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    config_before = config_file.read_bytes()
    existing_skill_before = (
        installed_skills_dir / "skill-creator" / "SKILL.md"
    ).read_bytes()

    def _unexpected_prepare(*args, **kwargs):
        raise AssertionError("existing workspace must not run full initialization")

    monkeypatch.setattr(workspace_utils, "prepare_workspace", _unexpected_prepare)
    monkeypatch.setattr(
        workspace_utils,
        "get_builtin_skills_dir",
        lambda: BUILTIN_SKILLS_DIR,
    )

    first_diff = bootstrap_workspace(workspace_dir=workspace_dir)

    installed_root = installed_skills_dir / "opencli-web"
    assert installed_root.is_dir()
    assert (installed_root / XIAOHONGSHU_MODULE_PATH).is_file()
    assert config_file.read_bytes() == config_before
    assert (
        installed_skills_dir / "skill-creator" / "SKILL.md"
    ).read_bytes() == existing_skill_before
    assert first_diff.added_files

    state = json.loads(state_file.read_text(encoding="utf-8"))
    assert [p["name"] for p in state["installed_plugins"]].count("opencli-web") == 1
    assert state["skill_configs"]["opencli-web"]["enabled"] is False
    assert state["local_skills"] == [{"name": "preserved-local-skill"}]
    state_after_first_start = state_file.read_bytes()

    second_diff = bootstrap_workspace(workspace_dir=workspace_dir)

    assert second_diff == CopyDiffResult([], [], [])
    assert state_file.read_bytes() == state_after_first_start


def test_existing_workspace_startup_refreshes_managed_opencli_files(
    tmp_path,
    monkeypatch,
):
    workspace_dir = tmp_path / "existing-managed-workspace"
    config_file = workspace_dir / "config" / "config.yaml"
    installed_skills_dir = workspace_dir / "agent" / "workspace" / "skills"
    installed_root = installed_skills_dir / "opencli-web"
    config_file.parent.mkdir(parents=True)
    installed_root.mkdir(parents=True)
    config_file.write_text("preferred_language: zh\n", encoding="utf-8")
    (installed_root / "SKILL.md").write_text(
        "---\nname: opencli-web\n---\nstale managed content\n",
        encoding="utf-8",
    )
    user_extra = installed_root / "user-extra.txt"
    user_extra.write_text("preserve me\n", encoding="utf-8")

    state_file = installed_skills_dir / "skills_state.json"
    state_file.write_text(
        json.dumps(
            {
                "marketplaces": [],
                "installed_plugins": [
                    {"name": "opencli-web", "source": "builtin"},
                ],
                "local_skills": [],
                "skill_configs": {"opencli-web": {"enabled": False}},
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    state_before = state_file.read_bytes()
    builtin_dir = tmp_path / "builtin-skills"
    shutil.copytree(MASTER_SKILL_DIR, builtin_dir / "opencli-web")

    def _unexpected_prepare(*args, **kwargs):
        raise AssertionError("existing workspace must not run full initialization")

    monkeypatch.setattr(workspace_utils, "prepare_workspace", _unexpected_prepare)
    monkeypatch.setattr(
        workspace_utils,
        "get_builtin_skills_dir",
        lambda: builtin_dir,
    )

    first_diff = bootstrap_workspace(workspace_dir=workspace_dir)

    assert (installed_root / "SKILL.md").read_bytes() == (
        MASTER_SKILL_DIR / "SKILL.md"
    ).read_bytes()
    assert (installed_root / XIAOHONGSHU_MODULE_PATH).read_bytes() == (
        MASTER_SKILL_DIR / XIAOHONGSHU_MODULE_PATH
    ).read_bytes()
    assert (installed_root / PUBLISH_OPERATION_PATH).read_bytes() == (
        MASTER_SKILL_DIR / PUBLISH_OPERATION_PATH
    ).read_bytes()
    assert user_extra.read_text(encoding="utf-8") == "preserve me\n"
    assert state_file.read_bytes() == state_before
    assert str(installed_root / "SKILL.md") in first_diff.overwritten_files

    second_diff = bootstrap_workspace(workspace_dir=workspace_dir)

    assert second_diff == CopyDiffResult([], [], [])
    assert state_file.read_bytes() == state_before


def test_new_workspace_startup_keeps_full_initialization_path(tmp_path):
    workspace_dir = tmp_path / "new-user-workspace"

    diff = bootstrap_workspace(workspace_dir=workspace_dir)

    assert (workspace_dir / "config" / "config.yaml").is_file()
    installed_skills_dir = workspace_dir / "agent" / "workspace" / "skills"
    assert (installed_skills_dir / "opencli-web" / XIAOHONGSHU_MODULE_PATH).is_file()
    state = json.loads(
        (installed_skills_dir / "skills_state.json").read_text(encoding="utf-8")
    )
    installed_names = {
        item["name"]
        for item in state["installed_plugins"]
        if isinstance(item, dict) and "name" in item
    }
    assert {"skill-creator", "swarmskill-creator", "opencli-web"} <= installed_names
    assert diff.added_files


@pytest.mark.parametrize(
    "entrypoint",
    [
        REPO_ROOT / "jiuwenswarm" / "app.py",
        REPO_ROOT / "jiuwenswarm" / "server" / "app_agentserver.py",
        REPO_ROOT / "jiuwenswarm" / "gateway" / "app_gateway.py",
    ],
)
def test_service_entrypoints_use_shared_workspace_bootstrap(entrypoint):
    source = entrypoint.read_text(encoding="utf-8")

    assert re.search(r"\bbootstrap_workspace\([^)]*\)", source)


def test_opencli_skill_uses_progressive_disclosure_and_complete_command_catalog():
    master = (MASTER_SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    xiaohongshu = (XIAOHONGSHU_MODULE_DIR / "SKILL.md").read_text(encoding="utf-8")
    operation_documents = {
        relative_path: (XIAOHONGSHU_MODULE_DIR / relative_path).read_text(
            encoding="utf-8"
        )
        for relative_path in XIAOHONGSHU_OPERATION_COMMANDS
    }

    assert "any task involving a live website" in master
    assert XIAOHONGSHU_MODULE_PATH in master
    assert "relative_file_path" in master
    assert "browser_agent" in master
    assert "general-purpose" in master
    assert "opencli-web" in xiaohongshu
    assert "general-purpose" in xiaohongshu
    assert "site router" in xiaohongshu.lower()
    assert "exactly one" in xiaohongshu
    assert "relative_file_path" in xiaohongshu
    for operation_path in XIAOHONGSHU_OPERATION_COMMANDS:
        assert operation_path in xiaohongshu

    publishing = operation_documents["operations/publishing.md"]
    assert "social_post_confirm" in publishing
    assert "opencli_contract:" in publishing
    assert "xiaohongshu_guarded_publish" in publishing
    assert 'python -E "<opencli-web-directory>' not in publishing
    assert "opencli_adapter_incompatible" in publishing

    assert "references/" not in master
    assert "references/" not in xiaohongshu
    assert not list((MASTER_SKILL_DIR / "references").glob("*.md"))
    assert not list((XIAOHONGSHU_MODULE_DIR / "references").glob("*.md"))

    documented_commands: set[str] = set()
    for relative_path, expected_commands in XIAOHONGSHU_OPERATION_COMMANDS.items():
        current_commands = set(
            re.findall(
                r"^\| `([a-z-]+)` \|",
                operation_documents[relative_path],
                flags=re.MULTILINE,
            )
        )
        assert current_commands == expected_commands
        assert documented_commands.isdisjoint(current_commands)
        documented_commands.update(current_commands)
    assert documented_commands == XIAOHONGSHU_COMMANDS
    assert not re.findall(r"^\| `([a-z-]+)` \|", xiaohongshu, flags=re.MULTILINE)

    milestone_token = "M" + "1"
    for path in MASTER_SKILL_DIR.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".py", ".yaml"}:
            assert milestone_token not in path.read_text(encoding="utf-8")


@pytest.mark.asyncio
async def test_acceptance_trace_reads_operation_module_then_invokes_opencli(tmp_path):
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
    assert "opencli_contract:" in operation.data["skill_content"]
    trace.append(
        {
            "tool": "skill_tool",
            "skill": "opencli-web",
            "relative_file_path": PUBLISH_OPERATION_PATH,
        }
    )

    completed, result = _run_wrapper(
        tmp_path,
        {
            "title": "Route test",
            "content": "Main Skill to site router to operation contract to OpenCLI",
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
        {
            "tool": "skill_tool",
            "skill": "opencli-web",
            "relative_file_path": PUBLISH_OPERATION_PATH,
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
    assert "general-purpose" in prompt
    assert "relative_file_path" in prompt
    assert "site module is a router" in prompt
    assert "read exactly one listed operation module" in prompt
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


def test_publish_wrapper_blocks_known_broken_text_image_adapter_before_start(
    tmp_path,
    monkeypatch,
    capsys,
):
    wrapper = _load_publish_wrapper_module()
    package_root = tmp_path / "node_modules" / "@jackwener" / "opencli"
    main_js = package_root / "dist" / "src" / "main.js"
    publish_js = package_root / "clis" / "xiaohongshu" / "publish.js"
    main_js.parent.mkdir(parents=True)
    publish_js.parent.mkdir(parents=True)
    main_js.write_text("// fixture\n", encoding="utf-8")
    publish_js.write_text(
        "const __opencli_xhs_composer_media_count = true;\n"
        "const root = titleEl?.closest("
        '\'form, [class*="publish"], [class*="editor"], [class*="note"]\''
        ") || document.body;\n",
        encoding="utf-8",
    )
    (package_root / "package.json").write_text(
        json.dumps({"version": "1.8.6"}),
        encoding="utf-8",
    )
    payload_path = tmp_path / "payload.json"
    payload_path.write_text(
        json.dumps(
            {
                "title": "Draft test",
                "content": "Known adapter compatibility failure",
                "card_text": "test card",
            }
        ),
        encoding="utf-8",
    )
    runner = [str(tmp_path / "node.exe"), str(main_js)]
    subprocess_called = False

    def _unexpected_subprocess(*args, **kwargs):
        nonlocal subprocess_called
        subprocess_called = True
        raise AssertionError("known incompatible adapter must not start")

    monkeypatch.setattr(wrapper, "_resolve_opencli_argv", lambda executable: runner)
    monkeypatch.setattr(wrapper.subprocess, "run", _unexpected_subprocess)

    exit_code = wrapper.main(
        [
            "--payload",
            str(payload_path),
            "--opencli-bin",
            "fixture-opencli",
        ]
    )
    result = json.loads(capsys.readouterr().out)

    assert exit_code != 0
    assert subprocess_called is False
    assert result["ok"] is False
    assert result["error"]["code"] == "opencli_adapter_incompatible"
    assert "1.8.6" in result["error"]["detail"]
    assert result["attempted"] is False
    assert result["fallback_allowed"] is True

    confirmation_dir = tmp_path / "confirmations"
    payload_path.write_text(
        json.dumps(
            {
                "title": "Publish test",
                "content": "Do not consume confirmation during preflight",
                "card_text": "test card",
                "mode": "publish",
                "confirmation": {
                    "action": "social_post_confirm",
                    "id": "known-adapter-preflight",
                },
            }
        ),
        encoding="utf-8",
    )
    publish_exit_code = wrapper.main(
        [
            "--payload",
            str(payload_path),
            "--opencli-bin",
            "fixture-opencli",
            "--confirmation-dir",
            str(confirmation_dir),
        ]
    )
    publish_result = json.loads(capsys.readouterr().out)

    assert publish_exit_code != 0
    assert publish_result["error"]["code"] == "opencli_adapter_incompatible"
    assert publish_result["attempted"] is False
    assert publish_result["fallback_allowed"] is False
    assert not confirmation_dir.exists()

    image_request = wrapper._parse_payload(
        {
            "title": "Image draft",
            "content": "The image path remains supported",
            "images": [str(tmp_path / "cover.png")],
        }
    )
    assert (
        wrapper._detect_text_image_adapter_issue(
            image_request,
            runner,
            user_clis_dir=tmp_path / "user-clis",
        )
        is None
    )

    text_request = wrapper._parse_payload(
        {
            "title": "Text draft",
            "content": "A future fixed adapter remains usable",
            "card_text": "test card",
        }
    )
    publish_js.write_text("// fixed media proof\n", encoding="utf-8")
    assert (
        wrapper._detect_text_image_adapter_issue(
            text_request,
            runner,
            user_clis_dir=tmp_path / "user-clis",
        )
        is None
    )


def test_publish_wrapper_emits_ascii_safe_json_for_non_ascii_child_errors(tmp_path):
    completed, result = _run_wrapper(
        tmp_path,
        {
            "title": "Draft test",
            "content": "Preserve a structured non-ASCII error",
            "images": [str(tmp_path / "cover.png")],
        },
        fake_exit_code=7,
        fake_stderr="文字配图媒体校验失败",
    )

    assert completed.returncode == 7
    assert completed.stdout.isascii()
    assert result["error"]["detail"] == "文字配图媒体校验失败"


@pytest.mark.skipif(os.name != "nt", reason="Windows shell environment regression")
def test_windows_auto_shell_runs_wrapper_with_ignored_python_environment(tmp_path):
    from openjiuwen.core.sys_operation.local.shell_operation import ShellOperation
    from openjiuwen.core.sys_operation.local.utils import OperationUtils
    from openjiuwen.core.sys_operation.shell import ShellType

    command = f'python -E "{PUBLISH_WRAPPER}" --help'
    plan, use_shell, _ = ShellOperation._resolve_execution_plan(
        command,
        ShellType.AUTO,
    )
    completed = subprocess.run(
        plan,
        shell=use_shell,
        cwd=tmp_path,
        env=OperationUtils.prepare_environment(
            {"PYTHONHOME": str(tmp_path / "incompatible-python-home")}
        ),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "usage:" in completed.stdout.lower()


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
