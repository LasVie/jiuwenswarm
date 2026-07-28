---
name: opencli-xiaohongshu
description: Use through the preinstalled opencli-web Skill for any Xiaohongshu or 小红书 task covered by the OpenCLI adapter, including login, search, reading notes and comments, downloads, creator analytics, drafts, publishing, follows, and deletion.
---

# OpenCLI Xiaohongshu

This is a bundled site module, not an independently installed Skill. Load it
with the Skill tool by passing:

```json
{
  "skill_name": "opencli-web",
  "relative_file_path": "sites/xiaohongshu/SKILL.md"
}
```

Keep the routing and fallback rules from `opencli-web` in force. This module is
self-contained: it includes the complete reviewed command catalog and publish
contract. Do not use `task_tool`, `sessions_spawn`, a `general-purpose`
subagent, `browser_agent`, or a filesystem tool to read or analyze files in the
installed Skill directory.

## Choose an exact operation

Before execution, confirm the installed adapter schema with:

```text
opencli xiaohongshu <command> --help -f yaml
```

If the command is absent from the catalog below or the installed schema
conflicts with it, do not guess. Treat the OpenCLI route as unsupported and
return to the fallback rules in `opencli-web`.

Use `-f json` for machine-readable results. Browser-backed commands also accept
`--window foreground|background`, `--site-session ephemeral|persistent`, and
`--keep-tab true|false`.

| Command | Access | Exact usage | Purpose and important options |
|---|---|---|---|
| `ask` | write | `opencli xiaohongshu ask <query> [--timeout <seconds>] [--source-limit <count>] -f json` | Ask 小红书点点 and return an answer with sources. Defaults: timeout 90, source limit 10. |
| `comments` | read | `opencli xiaohongshu comments <note-url> [--limit <count>] [--with-replies true\|false] -f json` | Read comments and optional nested replies. Supply the full note URL with `xsec_token`; limit defaults to 20 and is capped at 50. |
| `creator-note-detail` | read | `opencli xiaohongshu creator-note-detail <note-id> -f json` | Read one creator note's content metrics, traffic sources, audience profile, and trends. |
| `creator-notes` | read | `opencli xiaohongshu creator-notes [--limit <count>] -f json` | List creator notes and per-note views, likes, saves, and comments. Limit defaults to 20. |
| `creator-notes-summary` | read | `opencli xiaohongshu creator-notes-summary [--limit <count>] [--timeout <seconds>] -f json` | Summarize recent creator notes and key metrics. Defaults: limit 3, timeout 180. |
| `creator-profile` | read | `opencli xiaohongshu creator-profile -f json` | Read the current creator account profile, followers, following, likes, and growth level. |
| `creator-stats` | read | `opencli xiaohongshu creator-stats [--period seven\|thirty] -f json` | Read creator totals and daily trends for seven or thirty days. |
| `delete-note` | write | `opencli xiaohongshu delete-note <note-id> [--execute true] -f json` | Verify a published note target by default. After final confirmation, `--execute true` deletes it. |
| `download` | read | `opencli xiaohongshu download <note-url-or-xhslink> [--output <directory>] -f json` | Download a note's images and videos. The default output is `./xiaohongshu-downloads`; confirm the destination first. |
| `draft-clear` | write | `opencli xiaohongshu draft-clear [--type image\|video\|article\|audio\|all] [--execute true] -f json` | Count matching local drafts by default. After final confirmation, `--execute true` clears them. |
| `draft-delete` | write | `opencli xiaohongshu draft-delete <draft-id> [--type image\|video\|article\|audio] [--execute true] -f json` | Verify one local draft by default. After final confirmation, `--execute true` deletes it. |
| `draft-open` | read | `opencli xiaohongshu draft-open <draft-id> [--type image\|video\|article\|audio] -f json` | Read one local draft's title, content, images, and update time. |
| `drafts` | read | `opencli xiaohongshu drafts [--type image\|video\|article\|audio] -f json` | List local drafts of the selected type. |
| `feed` | read | `opencli xiaohongshu feed [--limit <count>] -f json` | Read the home recommendation feed. Limit defaults to 20. |
| `follow` | write | `opencli xiaohongshu follow <user-id-or-profile-url> -f json` | Follow a user immediately. Require final confirmation for the exact account. |
| `liked` | read | `opencli xiaohongshu liked [--id <user-id-or-profile-url>] [--limit <count>] -f json` | List liked notes for the current or specified user. Limit defaults to 20. |
| `login` | write | `opencli xiaohongshu login [--timeout <seconds>] --window foreground --site-session persistent -f json` | Open login and wait for the user to authenticate. Timeout defaults to 300 seconds. |
| `note` | read | `opencli xiaohongshu note <note-url> -f json` | Read note content and engagement data. Supply the full note URL with `xsec_token`. |
| `notifications` | read | `opencli xiaohongshu notifications [--type mentions\|likes\|connections] [--limit <count>] -f json` | Read account notifications. Defaults: type `mentions`, limit 20. |
| `publish` | write | `python -E "<opencli-web-directory>/sites/xiaohongshu/scripts/publish.py" --payload "<payload.json>"` | Create an image/text draft or publish after `social_post_confirm`. Always use the guarded wrapper and the contract below. |
| `saved` | read | `opencli xiaohongshu saved [--id <user-id-or-profile-url>] [--limit <count>] -f json` | List saved notes for the current or specified user. Limit defaults to 20. |
| `search` | read | `opencli xiaohongshu search <query> [--limit <count>] -f json` | Search notes. Limit defaults to 20. |
| `unfollow` | write | `opencli xiaohongshu unfollow <user-id-or-profile-url> -f json` | Unfollow a user immediately. Require final confirmation for the exact account. |
| `user` | read | `opencli xiaohongshu user <user-id-or-profile-url> [--limit <count>] -f json` | Read public notes from a user profile. Limit defaults to 15. |
| `whoami` | read | `opencli xiaohongshu whoami --site-session persistent -f json` | Show the currently authenticated Xiaohongshu account. |

## Run read operations

1. Collect only the inputs required by the selected command.
2. Prefer structured output with `-f json`.
3. Run one exact documented command and inspect its exit status and output.
4. A read failure may fall back to `browser_agent` if no write occurred and the
   browser route is otherwise allowed.

`download` is classified as read by OpenCLI but writes files locally. Confirm
the output directory and avoid overwriting user files.

## Gate write operations

OpenCLI classifies `ask`, `login`, `follow`, `unfollow`, `delete-note`,
`draft-delete`, `draft-clear`, and `publish` as writes.

- `login` requires the user to complete authentication in the foreground
  browser session. Never request or handle a password in chat.
- `delete-note`, `draft-delete`, and `draft-clear` default to dry-run. Run the
  dry-run first, show the exact target, obtain final confirmation, and only then
  repeat once with `--execute true`.
- `follow` and `unfollow` change the account immediately. Obtain final A2UI
  confirmation for the exact user before one execution.
- Once any write command starts, never retry it with `browser_agent`. Use a
  documented read operation to verify the outcome or report uncertainty.

## Draft and publish contract

Publishing uses the guarded wrapper rather than a direct `opencli` invocation.
Pass one UTF-8 JSON object through `--payload`.

| Field | Required | Shape | Notes |
|---|---|---|---|
| title | yes | string | Non-empty, at most 20 characters |
| content | yes | string | Non-empty |
| images | one media form | list of strings | 1-9 `.jpg`, `.jpeg`, `.png`, `.gif`, or `.webp` paths |
| card_text | one media form | string or list of strings | Mutually exclusive with `images`; list entries become `|||`-separated cards |
| card_style | no | string | Valid only with `card_text` |
| topics | no | list of strings | No `#` or commas |
| mode | no | `"draft"` or `"publish"` | Defaults to `"draft"` |
| confirmation | publish only | object | Requires action `social_post_confirm` and a stable unique `id` |

Unknown fields and ambiguous media combinations are rejected before OpenCLI
starts.

Example draft:

```json
{
  "title": "OpenCLI draft",
  "content": "A deterministic draft.",
  "images": ["C:\\media\\cover.png"],
  "topics": ["OpenCLI", "agents"]
}
```

Example publish payload after final confirmation:

```json
{
  "title": "OpenCLI post",
  "content": "A confirmed post.",
  "card_text": ["First card", "Second card"],
  "mode": "publish",
  "confirmation": {
    "action": "social_post_confirm",
    "id": "session-and-action-specific-id"
  }
}
```

### Create a draft

1. Collect the exact title, content, media or text cards, and topics.
2. On the Web channel, show draft variants with `social_post_draft_select`.
3. After the user approves draft creation, write the selected values to a UTF-8
   JSON payload in the current session project directory. Omit `mode` or set it
   to `"draft"`.
4. Invoke the wrapper once with its absolute installed path:

   ```text
   python -E "<opencli-web-directory>/sites/xiaohongshu/scripts/publish.py" --payload "<payload.json>"
   ```

   Use the main agent's BashTool with `shell_type: "auto"`; do not force Git
   Bash on Windows, keep the documented `-E` interpreter flag, and do not
   delegate wrapper execution to a subagent.
5. Inspect the JSON envelope and report the draft result. Stop before public
   publishing.

Never invoke `opencli xiaohongshu publish` directly. The wrapper validates the
payload, defaults to draft mode, preserves argument boundaries, and classifies
fallback safety. Its `--confirmation-dir`, `--opencli-bin`, and
`--opencli-prefix-arg` options are internal/test controls and must not be
supplied during ordinary agent execution.

### Interpret wrapper output

The wrapper writes exactly one JSON envelope to stdout:

```json
{
  "ok": true,
  "mode": "draft",
  "attempted": true,
  "fallback_allowed": false,
  "result": {}
}
```

`attempted` means the OpenCLI process was started. Once a write attempt starts,
a failure or timeout remains non-fallback-safe. For publish mode, the
confirmation ID is represented by a one-time SHA-256 marker; the original ID
and post content are not written to that marker.

If `error.code` is `opencli_adapter_incompatible`, the wrapper detected the
known incompatible text-card media check before starting OpenCLI:

- Treat `attempted: false` as definitive; do not rerun the same text-card
  payload.
- For a draft with `fallback_allowed: true`, invoke `browser_agent` once with
  the same approved draft. If browser execution is unavailable, ask the user
  for image media and use a new `images` payload through this wrapper.
- For public publish, do not switch execution paths automatically. Obtain a
  fresh `social_post_confirm` confirmation for the exact path and content
  before any later attempt.
- Continue using OpenCLI normally for `images` payloads. A future adapter whose
  source no longer contains the incompatible check passes this preflight.

## Public publish gate

1. Render final A2UI confirmation with `social_post_confirm`. Its context must
   exactly match the selected title, content, media or text cards, and topics.
2. Only after confirmation, set `"mode": "publish"` and include:

   ```json
   {
     "confirmation": {
       "action": "social_post_confirm",
       "id": "stable-unique-confirmation-id"
     }
   }
   ```

3. Run `scripts/publish.py` exactly once for that confirmation ID.
4. Respect `social_post_cancel` by stopping without running the wrapper.

If publishing times out or returns an ambiguous failure, do not retry and do
not switch to `browser_agent`. Verify with a documented read command when
possible; otherwise report that the outcome is unknown and require a new,
explicit confirmation before any later attempt.

## Output handling

- Treat a non-zero exit status as failure even if stdout contains partial data.
- Do not include credentials, cookies, tokens, or full browser traces in user
  output or logs.
- For write commands, report whether execution started. Never silently retry an
  operation that may already have changed account state.
- When a read command returns URLs or IDs needed by a later write, preserve the
  exact values and show the target to the user at the confirmation gate.
