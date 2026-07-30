# 36Kr: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `article` | `public_read` / `low` | `opencli 36kr article "<id>" -f json`<br>获取36氪文章正文内容 | `id` (str, required, positional) | auth=none; transport=browser_intercept; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `article`: Source-audited against OpenCLI 1.8.6 36kr/article.js; reads public browser-rendered content without authenticated account state.
