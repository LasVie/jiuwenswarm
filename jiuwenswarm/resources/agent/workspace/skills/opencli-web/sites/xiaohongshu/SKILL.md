---
name: opencli-xiaohongshu
description: Use through the preinstalled opencli-web Skill as the Xiaohongshu or 小红书 site router for account access, discovery, note data, creator analytics, drafts, publishing, follows, and deletion.
---

# OpenCLI Xiaohongshu Router

This is a bundled site router, not an independently installed Skill. Load it
with the Skill tool by passing:

```json
{
  "skill_name": "opencli-web",
  "relative_file_path": "sites/xiaohongshu/SKILL.md"
}
```

Keep every routing, fallback, shell, and confirmation rule from `opencli-web`
in force. This file selects an operation contract; it intentionally does not
authorize or describe exact adapter commands.

## Select one operation contract

1. Match the user's request to exactly one capability group below.
2. In the main agent, call the Skill tool again with `skill_name` set to
   `opencli-web` and `relative_file_path` set to the selected module's full
   path.
3. Read exactly one operation module unless the user explicitly requests
   capabilities from multiple groups.
4. Follow only the loaded operation module's command, arguments, access class,
   confirmation gate, and fallback rules.
5. If that module declares an `opencli_contract`, call `opencli_execute`
   directly from this main Agent immediately after the Skill-tool read. The
   execution tool rejects missing, expired, different-Agent, and stale-file
   disclosure receipts.

Do not use `task_tool`, `sessions_spawn`, a `general-purpose` subagent,
`browser_agent`, or a filesystem tool to read or analyze an operation module.
Do not execute an OpenCLI adapter command from this router alone.

| Capability group | Match when the request needs | Access | Operation module |
|---|---|---|---|
| Account | Login or identify the current account | read/write | `sites/xiaohongshu/operations/account.md` |
| Discovery | Ask Xiaohongshu, search notes, or read the recommendation feed | read/write | `sites/xiaohongshu/operations/discovery.md` |
| Notes | Read notes, comments, profiles, reactions, notifications, or download media | read | `sites/xiaohongshu/operations/notes.md` |
| Creator analytics | Read creator profile, aggregate metrics, note metrics, or trends | read | `sites/xiaohongshu/operations/creator-analytics.md` |
| Drafts | List, inspect, delete, or clear local drafts | read/write | `sites/xiaohongshu/operations/drafts.md` |
| Publishing | Create a guarded image/text draft; public publish remains fail-closed until a trusted runtime confirmation receipt is available | write | `sites/xiaohongshu/operations/publishing.md` |
| Social actions | Follow, unfollow, or delete a published note | write | `sites/xiaohongshu/operations/social-actions.md` |

If no row exactly matches both the requested capability and intended side
effect, treat the OpenCLI route as unsupported and return to the fallback rules
in `opencli-web`. Never infer one operation from a nearby group.

## Apply common adapter rules

- For a structured operation, let `opencli_execute` validate the installed
  operation hash, command, payload boundary, and reviewed executor. Do not
  inspect or invoke its underlying wrapper with a shell.
- For an operation not yet migrated to the structured tool, confirm its command
  against the installed schema with
  `opencli xiaohongshu <command> --help -f yaml`.
- If the installed schema conflicts with the loaded contract, do not guess or
  copy an undocumented option from the adapter. Treat the OpenCLI route as
  unsupported.
- Prefer `-f json` for machine-readable results. Browser-backed commands also
  accept `--window foreground|background`,
  `--site-session ephemeral|persistent`, and `--keep-tab true|false`.
- Preserve required Web-channel A2UI gates. An operation module cannot waive a
  required user approval.
- Once any write command starts, never retry the same operation through
  `browser_agent`. Use a documented read operation to verify the outcome or
  stop and report uncertainty.

## Handle output

- Treat a non-zero exit status as failure even if stdout contains partial data.
- Do not include credentials, cookies, tokens, or full browser traces in user
  output or logs.
- For write commands, report whether execution started. Never silently retry an
  operation that may already have changed account state.
- Preserve exact URLs and IDs needed by a later write and show the target at
  the confirmation gate.
