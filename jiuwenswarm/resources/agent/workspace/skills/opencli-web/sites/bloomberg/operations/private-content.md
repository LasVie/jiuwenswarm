# Bloomberg: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `news` | `private_content_read` / `medium` | `opencli bloomberg news "<link>" -f json`<br>Read a Bloomberg story/article page and return title, full content, and media links | `link` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `news`: Source-audited against OpenCLI 1.8.6 bloomberg/news.js; reads the article visible in the current browser session and does not bypass subscription or paywall controls.; sensitive output: subscription-gated content
