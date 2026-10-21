# Claude Code Plugins

---

## Concepts

JiuwenSwarm can load plugins written for [Claude Code](https://code.claude.com/docs/en/plugins) without converting them. You copy the plugin folder into a plugins directory; JiuwenSwarm picks up its **subagents** and **skills** the next time an agent is created.

A Claude Code plugin is a folder with this layout:

```text
<plugin-name>/
├── .claude-plugin/
│   └── plugin.json        # manifest: name, version, description, author
├── agents/                # subagent definitions (*.md)       ✅ supported
├── skills/                # skills (<name>/SKILL.md)          ✅ supported
├── commands/              # slash commands (*.md)             ❌ ignored for now
├── hooks/hooks.json       # lifecycle hooks                   ❌ ignored for now
└── .mcp.json              # MCP servers                       ❌ ignored for now
```

Tested plugins (from [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)):

| Plugin | Contains | Status |
|---|---|---|
| `code-simplifier` | 1 subagent | ✅ Works — callable as `code-simplifier:code-simplifier` |
| `frontend-design` | 1 skill | ✅ Works — loaded automatically on UI tasks |

---

## Install a plugin step by step

### Step 1: Check what the plugin contains

Before installing, open the plugin folder and confirm it only uses supported parts (see [Scope and limitations](#scope-and-limitations)):

```bash
find <plugin-folder> -type f
```

- `agents/*.md` and `skills/*/SKILL.md` will work.
- If the plugin's main feature lives in `commands/`, `hooks/` or `.mcp.json`, that part will not run yet.

> **Security:** plugins are instructions for the agent, and the agent acts with your permissions. Only install plugins from sources you trust, and read the `.md` files first.

### Step 2: Get the plugin files

Example: fetch only the two official plugins with a sparse clone.

```bash
git clone --filter=blob:none --sparse https://github.com/anthropics/claude-plugins-official.git
cd claude-plugins-official
git sparse-checkout set plugins/code-simplifier plugins/frontend-design
```

The plugins are now in `claude-plugins-official/plugins/<name>/`.

### Step 3: Choose the install scope

| Scope | Directory | Applies to |
|---|---|---|
| User | `~/.jiuwenswarm/plugins/<name>/` | Every project for this user |
| Project | `<project>/.jiuwenswarm/plugins/<name>/` | Only that project (can be committed and shared with the team) |

- `~/.jiuwenswarm` is the data directory; if you set `JIUWENSWARM_DATA_DIR`, use that path instead.
- If the same plugin name exists in both, the **project** copy wins.

### Step 4: Copy the plugin folder

Copy the whole plugin folder (keep `.claude-plugin/` and the `agents/` / `skills/` sub-folders as they are):

```bash
# User scope
mkdir -p ~/.jiuwenswarm/plugins
cp -r plugins/code-simplifier ~/.jiuwenswarm/plugins/
cp -r plugins/frontend-design ~/.jiuwenswarm/plugins/

# Or project scope
mkdir -p <project>/.jiuwenswarm/plugins
cp -r plugins/code-simplifier <project>/.jiuwenswarm/plugins/
```

Expected layout:

```text
~/.jiuwenswarm/plugins/
├── code-simplifier/
│   ├── .claude-plugin/plugin.json
│   └── agents/code-simplifier.md
└── frontend-design/
    ├── .claude-plugin/plugin.json
    └── skills/frontend-design/SKILL.md
```

Notes:

- The plugin's name comes from `name` in `.claude-plugin/plugin.json`. If there is no manifest, the folder name is used (the folder must then contain `agents/` or `skills/`).
- A symlink to a cloned repo also works, which makes updating easier (`ln -s /path/to/repo/plugins/code-simplifier ~/.jiuwenswarm/plugins/code-simplifier`).

### Step 5: Verify that JiuwenSwarm sees the plugin

From the JiuwenSwarm repo, using its virtual environment:

```bash
.venv/bin/python -c "
from jiuwenswarm.common.claude_plugins import discover_claude_plugins, claude_plugin_skill_dirs
from jiuwenswarm.server.runtime.agent_config_service import AgentConfigService
print('plugins:', [p.name for p in discover_claude_plugins('.')])
print('skill dirs:', claude_plugin_skill_dirs('.'))
print('agents:', [a.name for a in AgentConfigService('.').list_agents() if a.source == 'plugin'])
"
```

Expected output for the two example plugins:

```text
plugins: ['code-simplifier', 'frontend-design']
skill dirs: ['/home/<you>/.jiuwenswarm/plugins/frontend-design/skills']
agents: ['code-simplifier:code-simplifier']
```

### Step 6: Start a new session

Plugins are read when an agent is built. Start a new chat session (or restart the services) after installing, updating or disabling a plugin:

```bash
jiuwenswarm-start app        # or restart jiuwenswarm-agentserver + jiuwenswarm-gateway
```

### Step 7: Use the plugin

**Subagents** are registered as `<plugin-name>:<agent-name>`. Ask for them by name, or let the agent pick them from the `Agent` tool list:

```bash
jiuwenswarm chat --mode code.normal --cwd <project> \
  "Use the Agent tool with subagent_type 'code-simplifier:code-simplifier' to simplify grade.py"
```

**Skills** keep the name from their `SKILL.md`. With `skill_mode: all` (default) the agent sees them and loads them by itself when the task matches, e.g.:

```bash
jiuwenswarm chat --mode code.normal --cwd <project> \
  "Write hero.html: a hero section for a pottery studio in Kyoto"
# the agent calls skill_tool → frontend-design before writing the file
```

---

## Manage installed plugins

### Disable a plugin

All discovered plugins are enabled. To turn one off without deleting it, add to `~/.jiuwenswarm/config/config.yaml`:

```yaml
claude_plugins:
  code-simplifier:
    enabled: false
```

To turn off a single plugin agent instead of the whole plugin, use the existing subagent switch:

```yaml
react:
  subagents:
    "code-simplifier:code-simplifier":
      enabled: false
```

### Update a plugin

Replace the folder with the newer version (or `git pull` if you used a symlink), then start a new session.

### Uninstall a plugin

```bash
rm -rf ~/.jiuwenswarm/plugins/<name>
```

### Edit a plugin agent

Plugin agents are read-only in the `/agents` UI and API (edit/delete returns an error). Edit the plugin's `agents/*.md` file directly, or copy it to `~/.jiuwenswarm/agents/` as your own agent and change it there.

---

## Scope and limitations

### What is supported

| Plugin part | Support | How it maps to JiuwenSwarm |
|---|---|---|
| `.claude-plugin/plugin.json` | ✅ Partial | Only `name` (plus `version`/`description` for display) is read |
| `agents/*.md` | ✅ | Custom subagents named `<plugin>:<agent>`, lowest priority after user/project/local agents |
| `skills/<name>/SKILL.md` | ✅ | Added as an extra skill scan directory |
| `commands/*.md` | ❌ | Ignored — slash commands are not registered |
| `hooks/hooks.json` | ❌ | Ignored — hooks do not run |
| `.mcp.json` | ❌ | Ignored — MCP servers are not started |
| Marketplace (`/plugin install`, `marketplace.json`) | ❌ | No install command — copy folders manually |

### Known limitations

1. **Only the default folders are read.** Custom paths declared in `plugin.json` (e.g. `"agents": "./custom/"`, `"skills": [...]`) are ignored; only `agents/` and `skills/` at the plugin root are scanned.
2. **Model aliases are ignored.** `model: sonnet | opus | haiku | inherit` in an agent file means "use the session's model". Other values are looked up as JiuwenSwarm model names and fall back to the session model if not found.
3. **Tool names must exist in JiuwenSwarm.** `tools:` in agent frontmatter accepts both a list and Claude's comma-separated string. Known names (`Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`, `LS`, `WebSearch`, `WebFetch`, `TodoWrite`, …) are mapped to JiuwenSwarm tools; Claude-only tools (e.g. `NotebookEdit`, `Task`, `mcp__*` tools from the plugin's own MCP servers) are silently left out, so an agent restricted to such tools may end up with fewer tools than intended. Agents with no `tools:` line get all tools.
4. **Skills are not namespaced.** A plugin skill is listed under its own name (`frontend-design`), not `plugin:skill`. If it has the same name as a skill you already have, both may appear; rename one to avoid confusion.
5. **`${CLAUDE_PLUGIN_ROOT}` is not expanded.** Skills or agents that reference scripts via this variable will not find them.
6. **Claude-Code-specific instructions stay as written.** Prompts may mention `CLAUDE.md` or Claude Code tools; JiuwenSwarm passes the text unchanged, and the agent interprets it as best it can.
7. **No hot reload.** Changes take effect in new sessions only (see [Step 6](#step-6-start-a-new-session)).

### Choosing plugins that will work today

A plugin works fully if all of its functionality is in `agents/` and/or `skills/`. Before installing, run `find <plugin> -type f` (Step 1): if you see `commands/`, `hooks/` or `.mcp.json`, expect those parts to be missing.

---

## Troubleshooting

| Symptom | Check |
|---|---|
| Plugin not in Step 5 output | Folder is directly under `plugins/` (not `plugins/plugins/<name>`); `plugin.json` is valid JSON; plugin not disabled under `claude_plugins` |
| Agent not offered in chat | Started a new session? `react.subagents` not set to `enabled: false` for `<plugin>:<agent>`? Agent file has `---` frontmatter with `name:` |
| Skill never loaded | `SKILL.md` is at `skills/<name>/SKILL.md`; `skill_mode` in `config.yaml` lists skills to the agent; try asking for it by name |
| Warnings in logs | Search the agent server log for `Claude plugin` (bad manifest, failed discovery) |
