# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Claude Code 插件加载 — 直接读取 Claude Code 格式的插件目录.

插件目录结构（与 Claude Code 一致）::

    <plugin>/
      .claude-plugin/plugin.json   # 清单（可选，缺省时用目录名作为插件名）
      agents/*.md                  # 子 agent 定义
      skills/<name>/SKILL.md       # skill

搜索位置（同名时项目级覆盖用户级）：
- user:    ~/.jiuwenswarm/plugins/<name>/
- project: <workspace>/.jiuwenswarm/plugins/<name>/

默认全部启用，可在 config.yaml 中关闭::

    claude_plugins:
      code-simplifier:
        enabled: false
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

from jiuwenswarm.common.utils import get_user_workspace_dir

logger = logging.getLogger(__name__)

_MANIFEST_RELPATH = Path(".claude-plugin") / "plugin.json"

# Claude Code 的模型别名在 jiuwenswarm 中无对应模型，按 inherit 处理（沿用父 agent 模型）。
CLAUDE_MODEL_ALIASES: frozenset[str] = frozenset({"inherit", "sonnet", "opus", "haiku"})


@dataclass
class ClaudePlugin:
    """一个已发现的 Claude Code 插件。"""

    name: str
    root: Path
    version: str | None = None
    description: str | None = None

    @property
    def agents_dir(self) -> Path:
        return self.root / "agents"

    @property
    def skills_dir(self) -> Path:
        return self.root / "skills"


def get_user_plugins_dir() -> Path:
    return get_user_workspace_dir() / "plugins"


def get_project_plugins_dir(workspace_dir: Path | str) -> Path:
    return Path(workspace_dir) / ".jiuwenswarm" / "plugins"


def _load_plugin(plugin_dir: Path) -> ClaudePlugin | None:
    manifest_path = plugin_dir / _MANIFEST_RELPATH
    manifest: dict = {}
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8")) or {}
        except (OSError, ValueError):
            logger.warning("Failed to parse Claude plugin manifest: %s", manifest_path, exc_info=True)
            return None
        if not isinstance(manifest, dict):
            logger.warning("Claude plugin manifest is not an object: %s", manifest_path)
            return None
    elif not (plugin_dir / "agents").is_dir() and not (plugin_dir / "skills").is_dir():
        return None
    name = str(manifest.get("name") or plugin_dir.name).strip()
    if not name:
        return None
    return ClaudePlugin(
        name=name,
        root=plugin_dir,
        version=manifest.get("version"),
        description=manifest.get("description"),
    )


def _disabled_plugin_names(config_base: dict | None) -> set[str]:
    if config_base is None:
        try:
            from jiuwenswarm.common.config import get_config

            config_base = get_config()
        except Exception:  # noqa: BLE001
            logger.debug("Failed to load config for claude_plugins", exc_info=True)
            return set()
    section = config_base.get("claude_plugins") if isinstance(config_base, dict) else None
    if not isinstance(section, dict):
        return set()
    return {
        name for name, cfg in section.items()
        if isinstance(cfg, dict) and cfg.get("enabled") is False
    }


def discover_claude_plugins(
    workspace_dir: Path | str | None = None,
    config_base: dict | None = None,
) -> list[ClaudePlugin]:
    """返回已启用的 Claude Code 插件，同名时项目级覆盖用户级。"""
    roots = [get_user_plugins_dir()]
    if workspace_dir is not None:
        roots.append(get_project_plugins_dir(workspace_dir))

    found: dict[str, ClaudePlugin] = {}
    for root in roots:
        if not root.is_dir():
            continue
        for plugin_dir in sorted(p for p in root.iterdir() if p.is_dir()):
            plugin = _load_plugin(plugin_dir)
            if plugin is not None:
                found[plugin.name] = plugin

    disabled = _disabled_plugin_names(config_base)
    return [p for name, p in found.items() if name not in disabled]


def claude_plugin_skill_dirs(
    workspace_dir: Path | str | None = None,
    config_base: dict | None = None,
) -> list[str]:
    """已启用插件的 skills/ 目录（可直接作为 SkillUseRail 的扫描根）。"""
    return [
        str(p.skills_dir)
        for p in discover_claude_plugins(workspace_dir, config_base)
        if p.skills_dir.is_dir()
    ]


__all__ = [
    "CLAUDE_MODEL_ALIASES",
    "ClaudePlugin",
    "claude_plugin_skill_dirs",
    "discover_claude_plugins",
    "get_project_plugins_dir",
    "get_user_plugins_dir",
]
