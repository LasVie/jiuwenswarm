# Jianyu: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `detail` | `public_read` / `low` | `opencli jianyu detail "<url>" [--query "<query>"] -f json`<br>读取剑鱼标讯详情页并抽取证据字段 | `url` (str, required, positional); `query` (str, optional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `detail`: Source-audited against OpenCLI 1.8.6 jianyu/detail.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
