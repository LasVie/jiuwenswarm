# Xiaohongshu Draft Operations

This operation contract is selected by the Xiaohongshu site router. It
authorizes only the commands listed below. Keep all parent routing, shell,
confirmation, and fallback rules in force.

| Command | Access | Exact usage | Purpose and important options |
|---|---|---|---|
| `draft-clear` | write | `opencli xiaohongshu draft-clear [--type image\|video\|article\|audio\|all] [--execute true] -f json` | Count matching local drafts by default. After final confirmation, `--execute true` clears them. |
| `draft-delete` | write | `opencli xiaohongshu draft-delete <draft-id> [--type image\|video\|article\|audio] [--execute true] -f json` | Verify one local draft by default. After final confirmation, `--execute true` deletes it. |
| `draft-open` | read | `opencli xiaohongshu draft-open <draft-id> [--type image\|video\|article\|audio] -f json` | Read one local draft's title, content, images, and update time. |
| `drafts` | read | `opencli xiaohongshu drafts [--type image\|video\|article\|audio] -f json` | List local drafts of the selected type. |

## Inspect drafts

1. Use `drafts` to identify candidate IDs and types.
2. Use `draft-open` to verify the exact draft before any destructive action.
3. Preserve the exact draft ID and type between inspection and confirmation.

## Delete drafts safely

1. Run `draft-delete` or `draft-clear` without `--execute true` first.
2. Show the exact target or matching count and obtain final Web-channel
   confirmation.
3. Repeat the same command once with `--execute true`.
4. Do not retry through `browser_agent` after the execute call starts. Verify
   with `drafts` or `draft-open`, or report uncertainty.
