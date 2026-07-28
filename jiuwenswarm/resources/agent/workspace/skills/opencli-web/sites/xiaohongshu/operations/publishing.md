# Xiaohongshu Publishing Operation

This operation contract is selected by the Xiaohongshu site router. It
authorizes only the command listed below. Keep all parent routing, shell,
confirmation, and fallback rules in force.

| Command | Access | Exact usage | Purpose and important options |
|---|---|---|---|
| `publish` | write | `python -E "<opencli-web-directory>/sites/xiaohongshu/scripts/publish.py" --payload "<payload.json>"` | Create an image/text draft or publish after `social_post_confirm`. Always use the guarded wrapper and the contract below. |

Never invoke `opencli xiaohongshu publish` directly. The guarded wrapper
validates the payload, defaults to draft mode, preserves argument boundaries,
checks the shared OpenCLI runtime, classifies fallback safety, and invokes
OpenCLI without a shell. Do not invoke `scripts/opencli_runtime.py` separately;
the wrapper calls it internally before adapter dispatch.

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

## Create a draft

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
failure or timeout remains non-fallback-safe. For publish mode, the confirmation
ID is represented by a one-time SHA-256 marker; the original ID and post content
are not written to that marker.

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

## Publish publicly

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
not switch to `browser_agent`. Verify with a loaded read-operation contract
when possible; otherwise report that the outcome is unknown and require a new,
explicit confirmation before any later attempt.
