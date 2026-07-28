---
name: opencli-web
description: Use automatically at the start of any task involving a live website or webpage, including searching, reading, navigation, data extraction, form filling, login, posting, publishing, commenting, or account actions, even when the user does not mention OpenCLI. Route supported site operations through the bundled OpenCLI site module before using browser_agent.
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
4. Let that module select the exact OpenCLI command, arguments, output format,
   confirmation gate, and fallback behavior.
5. Use `browser_agent` only when no exact route exists or the selected module
   explicitly permits fallback.

Do not search for or install the nested site module as a separate Skill. It is a
file bundled inside `opencli-web`.

## Supported websites

| Website | Supported capability groups | Site module |
|---|---|---|
| Xiaohongshu / 小红书 (`www.xiaohongshu.com`, `creator.xiaohongshu.com`) | Account and login, discovery, note data, downloads, creator analytics, drafts, publishing, follows, and deletion | `sites/xiaohongshu/SKILL.md` |

Read [references/sites.md](references/sites.md) when domain aliases, capability
boundaries, or module loading details are needed.

## Enforce one automation path

- Never run OpenCLI and `browser_agent` concurrently for the same operation.
- A route exists only when both the site and the operation are documented by
  the selected module. Do not infer write support from a read command.
- Invoke only the exact OpenCLI command or guarded wrapper documented by the
  loaded site module. Inspecting `opencli <site> <command> --help -f yaml` is
  allowed; discovering an undocumented command does not authorize its use.
- Preserve all channel-specific confirmation gates. A site module cannot waive
  a required user approval or A2UI confirmation.
- If a write process starts, do not repeat the operation through
  `browser_agent`, even after a timeout or ambiguous result. Prefer a supported
  read-only verification; otherwise stop and report uncertainty.
- A missing executable, disabled or unreadable module, unsupported operation,
  or other provable pre-execution infrastructure failure is fallback-safe.
- Read-only OpenCLI failures may fall back to `browser_agent` when that does not
  risk duplicating a side effect.

Use `opencli list -f json` only to inspect locally installed adapter
capabilities. Add a reviewed site module before routing production work to a
new adapter.
