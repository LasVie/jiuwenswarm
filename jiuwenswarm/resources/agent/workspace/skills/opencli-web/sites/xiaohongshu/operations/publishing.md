---
opencli_contract:
  version: 1
  site: xiaohongshu
  operation: publishing
  commands:
    publish:
      executor: xiaohongshu_guarded_publish
---

# Xiaohongshu Publishing Operation

This operation contract is selected by the Xiaohongshu site router. It
authorizes only the command listed below. Keep all parent routing, shell,
confirmation, and fallback rules in force.

| Command | Access | Exact usage | Purpose and important options |
|---|---|---|---|
| `publish` | write | `opencli_execute(site="xiaohongshu", operation="publishing", command="publish", payload_path="<payload.json>")` | Create an image/text draft through the guarded executor. Public `mode: publish` is rejected until the runtime supplies a trusted, scope- and payload-bound confirmation receipt. |

Never invoke `opencli xiaohongshu publish`, the bundled Python wrapper, or
`scripts/opencli_runtime.py` directly. Call `opencli_execute` from the same main
Agent that just read this operation file. The structured tool validates this
file's hash and one-use disclosure receipt, snapshots the payload and any image
files into owned staging, and launches the guarded executor without a shell.
The original payload and media are never passed to the child process.

## Build the payload

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
| confirmation | reserved | object | A model-supplied action or ID is never sufficient authority. Public publish remains rejected until a trusted runtime receipt is wired. |

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

Reserved publish payload shape (documented for the future trusted-receipt
integration; it is not currently executable):

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

## Create a draft

1. Collect the exact title, content, media or text cards, and topics.
2. On the Web channel, show draft variants with `social_post_draft_select`.
3. After the user approves draft creation, write the selected values to a UTF-8
   JSON payload in the current session project directory. Omit `mode` or set it
   to `"draft"`.
4. Immediately after this Skill-tool read, invoke exactly once:

   ```json
   {
     "site": "xiaohongshu",
     "operation": "publishing",
     "command": "publish",
     "payload_path": "<payload.json>"
   }
   ```

   Use `opencli_execute` in the main Agent. Do not delegate the call and do not
   substitute BashTool, PowerShell, execute-code, a direct Python command, or a
   direct OpenCLI command.
5. Inspect the JSON envelope and report the draft result. Stop before public
   publishing.

The wrapper's `--confirmation-dir`, `--opencli-bin`, and
`--opencli-prefix-arg` options are internal/test controls and must not be
supplied during ordinary agent execution.

## Interpret wrapper output

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

`attempted` means OpenCLI adapter dispatch may have started. A daemon process
may be started while `attempted` remains `false` when OpenCLI returns the typed
pre-dispatch `BROWSER_CONNECT` error. Once adapter dispatch may have started, a
failure or timeout remains non-fallback-safe. The current public tool rejects
publish mode before OpenCLI starts. A model-generated confirmation ID,
including one copied from this document, cannot bypass that gate.

Before invoking OpenCLI, the wrapper queries daemon `/status` directly:

- If the daemon is not running, the wrapper continues and lets the real OpenCLI
  command perform its normal daemon auto-start.
- If the running daemon reports a disconnected extension, a required profile,
  or a disconnected selected profile, the wrapper returns
  `error.code: opencli_browser_unavailable` with `attempted: false`.
- If daemon auto-start later produces OpenCLI `BROWSER_CONNECT`, the wrapper
  returns the same error code with `attempted: false`.
- A draft may use `browser_agent` only when the returned
  `fallback_allowed` value is `true`. Public publishing requires a fresh
  confirmation for any different execution path.

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

## Public publishing gate

Do not call `opencli_execute` with `mode: "publish"` in the current runtime.
An A2UI `social_post_confirm` event is presently converted into model context;
it does not yet issue the server-side, scope- and payload-bound receipt required
by this executor. Arbitrary non-empty IDs are therefore rejected as
`opencli_confirmation_untrusted` before OpenCLI starts.

Keep the exact final account, title, content, media/text cards, topics,
visibility, and target audience available for the future confirmation binding.
Respect `social_post_cancel` by stopping. Do not substitute direct OpenCLI,
Bash, the bundled wrapper, or `browser_agent` to bypass this gate.
