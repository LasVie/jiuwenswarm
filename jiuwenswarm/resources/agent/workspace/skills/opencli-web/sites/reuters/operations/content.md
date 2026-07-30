# Reuters: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `article-detail` | `public_read` / `low` | `opencli reuters article-detail "<url>" -f json`<br>Reuters 路透社文章详情：标题/作者/正文文本 | `url` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `article-detail`: Source-audited against OpenCLI 1.8.6 reuters/article-detail.js; reads Reuters content visible in the current browser session and does not bypass login, subscription, paywall, or human-verification controls.
