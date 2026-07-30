# Gitee: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `user` | `public_read` / `low` | `opencli gitee user "<username>" -f json`<br>Show a Gitee user profile panel | `username` (str, required, positional) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `user`: Source-audited against OpenCLI 1.8.6 gitee/user.js; reads public browser-rendered content without authenticated account state.
