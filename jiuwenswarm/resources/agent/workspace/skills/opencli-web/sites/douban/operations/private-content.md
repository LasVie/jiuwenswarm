# Douban: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `marks` | `private_content_read` / `medium` | `opencli douban marks [--status "<collect\|wish\|do\|all>"] [--limit <limit>] [--uid "<uid>"] -f json`<br>导出个人观影标记 | `status` (str, optional, default='collect', choices=collect,wish,do,all); `limit` (int, optional, default=50); `uid` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `reviews` | `private_content_read` / `medium` | `opencli douban reviews [--limit <limit>] [--uid "<uid>"] [--full <true\|false>] -f json`<br>导出个人影评 | `limit` (int, optional, default=20); `uid` (str, optional); `full` (bool, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `marks`: sensitive output: private content, account identifiers
- `reviews`: sensitive output: private content, account identifiers
