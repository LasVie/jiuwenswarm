# 12306: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `orders` | `private_content_read` / `medium` | `opencli 12306 orders [--include-sensitive <true\|false>] -f json`<br>List in-progress 12306 orders (not yet ridden, refunded, or completed) for the logged-in user | `include-sensitive` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `passengers` | `private_content_read` / `medium` | `opencli 12306 passengers [--limit <limit>] [--include-sensitive <true\|false>] -f json`<br>List the logged-in user's saved 12306 passengers. Sensitive fields are masked by default; pass --include-sensitive to opt in. | `limit` (int, optional, default=20); `include-sensitive` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `orders`: sensitive output: private content, account identifiers
- `passengers`: sensitive output: private content, account identifiers
