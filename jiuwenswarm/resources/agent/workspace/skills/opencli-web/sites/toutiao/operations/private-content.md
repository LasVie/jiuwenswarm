# Toutiao: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `articles` | `private_content_read` / `medium` | `opencli toutiao articles [--page <page>] -f json`<br>获取头条号创作者后台文章列表及数据 | `page` (int, optional, default=1) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `articles`: sensitive output: private content, account identifiers
