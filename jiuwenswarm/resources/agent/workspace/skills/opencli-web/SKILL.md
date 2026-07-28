---
name: opencli-web
description: Use automatically at the start of any task involving a live website or webpage, including searching, reading, navigation, data extraction, form filling, login, posting, publishing, commenting, or account actions, even when the user does not mention OpenCLI. Route supported site operations through the bundled site router and operation contract before using browser_agent.
---

# OpenCLI Web Router

Use this preinstalled Skill as the automatic entry point for every live website
task. The user does not need to find, install, enable, or select a site Skill.

## Route automatically

1. Read `opencli-web` before starting `browser_agent`.
2. Match both the website and the requested operation against the supported
   websites below.
3. For an exact match, use the Skill tool again with `skill_name` set to
   `opencli-web` and `relative_file_path` set to the listed site module.
4. Treat the site module as a router. Let it select one operation module for
   the requested capability group.
5. In the main agent, use the Skill tool a third time with `skill_name` set to
   `opencli-web` and `relative_file_path` set to that operation module's full
   path.
6. Execute only the command, arguments, output format, confirmation gate, and
   fallback behavior documented by the loaded operation module.
7. Use `browser_agent` only when no exact route exists or the loaded operation
   module explicitly permits fallback.

Do not search for or install nested site or operation modules as separate
Skills. They are files bundled inside `opencli-web`.

Keep Skill disclosure in the main agent. Never use `task_tool`,
`sessions_spawn`, a `general-purpose` subagent, `browser_agent`, or a filesystem
tool to read files under the installed `opencli-web` directory. The Skill tool
is the authorized reader for every listed site and operation module path.

The bundled files in this router are application-managed and refreshed during
JiuwenSwarm startup. Do not customize the installed copy; keep unrelated custom
Skills in their own directories.

## Supported websites

| Website | Supported capability groups | Site module |
|---|---|---|
| Xiaohongshu / 小红书 (`www.xiaohongshu.com`, `creator.xiaohongshu.com`) | Account and login, discovery, note data, downloads, creator analytics, drafts, publishing, follows, and deletion | `sites/xiaohongshu/SKILL.md` |

## Execute documented commands

- On Windows, invoke documented OpenCLI adapter commands and guarded wrapper
  scripts with the main agent's BashTool using `shell_type: "auto"`, unless the
  loaded operation module explicitly requires another shell.
- Do not force `bash` or `sh` merely to run Python, invoke OpenCLI, or translate
  Windows paths.
- On Windows, run bundled Python wrapper scripts as
  `python -E "<absolute-script-path>" ...` so an inherited `PYTHONHOME` cannot
  bind a different Python executable to an incompatible standard library.
- Preserve quoted absolute Windows paths and argument boundaries exactly as
  documented by the loaded operation module.
- Do not invoke `scripts/opencli_runtime.py` separately. A documented guarded
  wrapper must run the shared readiness check internally before adapter
  dispatch and classify typed OpenCLI connection failures itself.

## Enforce one automation path

- Never run OpenCLI and `browser_agent` concurrently for the same operation.
- A route exists only when the root router lists the site, the site router
  lists the capability group, and the selected operation module documents the
  exact command. Do not infer write support from a read command.
- Invoke only the exact OpenCLI command or guarded wrapper documented by the
  loaded operation module. Inspecting
  `opencli <site> <command> --help -f yaml` is allowed after disclosure;
  discovering an undocumented command does not authorize its use.
- Preserve all channel-specific confirmation gates. An operation module cannot
  waive a required user approval or A2UI confirmation.
- If a write process starts, do not repeat the operation through
  `browser_agent`, even after a timeout or ambiguous result. Prefer a supported
  read-only verification; otherwise stop and report uncertainty.
- A missing executable, disabled or unreadable module, unsupported operation,
  or other provable pre-execution infrastructure failure is fallback-safe.
- Read-only OpenCLI failures may fall back to `browser_agent` when that does not
  risk duplicating a side effect.

Use `opencli list -f json` only to inspect locally installed adapter
capabilities. Add reviewed site and operation modules before routing production
work to a new adapter.
