# Xiaohongshu Social Action Operations

This operation contract is selected by the Xiaohongshu site router. It
authorizes only the commands listed below. Keep all parent routing, shell,
confirmation, and fallback rules in force.

| Command | Access | Exact usage | Purpose and important options |
|---|---|---|---|
| `delete-note` | write | `opencli xiaohongshu delete-note <note-id> [--execute true] -f json` | Verify a published note target by default. After final confirmation, `--execute true` deletes it. |
| `follow` | write | `opencli xiaohongshu follow <user-id-or-profile-url> -f json` | Follow a user immediately. |
| `unfollow` | write | `opencli xiaohongshu unfollow <user-id-or-profile-url> -f json` | Unfollow a user immediately. |

## Follow or unfollow

1. Resolve and show the exact user ID or profile URL.
2. Obtain final Web-channel confirmation for that account and action.
3. Invoke `follow` or `unfollow` exactly once.
4. Do not retry through `browser_agent` after the command starts.

## Delete a published note

1. Run `delete-note <note-id>` without `--execute true` to verify the target.
2. Show the exact note and obtain final Web-channel confirmation.
3. Repeat once with `--execute true`.
4. Verify with a loaded read-operation contract when possible; otherwise report
   uncertainty without retrying the deletion.
