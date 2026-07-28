# Xiaohongshu publish wrapper contract

## Input

Pass one UTF-8 JSON object through `--payload`.

| Field | Required | Shape | Notes |
|---|---|---|---|
| `title` | yes | string | Non-empty, at most 20 characters |
| `content` | yes | string | Non-empty |
| `images` | one media form | list of strings | 1-9 `.jpg`, `.jpeg`, `.png`, `.gif`, or `.webp` paths |
| `card_text` | one media form | string or list of strings | Mutually exclusive with `images`; list entries become `|||`-separated cards |
| `card_style` | no | string | Valid only with `card_text` |
| `topics` | no | list of strings | No `#` or commas |
| `mode` | no | `"draft"` or `"publish"` | Defaults to `"draft"` |
| `confirmation` | publish only | object | Requires action `social_post_confirm` and a stable unique `id` |

Unknown fields and ambiguous media combinations are rejected before OpenCLI
starts.

Example draft:

```json
{
  "title": "OpenCLI M1",
  "content": "A deterministic draft.",
  "images": ["C:\\media\\cover.png"],
  "topics": ["OpenCLI", "智能体"]
}
```

Example publish payload after final confirmation:

```json
{
  "title": "OpenCLI M1",
  "content": "A confirmed post.",
  "card_text": ["第一页", "第二页"],
  "mode": "publish",
  "confirmation": {
    "action": "social_post_confirm",
    "id": "session-and-action-specific-id"
  }
}
```

## Output

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

`attempted` means the OpenCLI process was started. `fallback_allowed` is true
only for a missing OpenCLI executable discovered before execution. Once a write
attempt starts, a failure or timeout remains non-fallback-safe.

For publish mode, the confirmation ID is represented by a one-time SHA-256
marker under `--confirmation-dir`, `JIUWENSWARM_OPENCLI_CONFIRMATION_DIR`, or
the default JiuwenSwarm workspace state directory. The original ID and post
content are not written to that marker.
