# Hupu: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `detail` | `public_read` / `low` | `opencli hupu detail "<tid>" [--replies <true\|false>] -f json`<br>获取虎扑帖子详情 (使用Next.js JSON数据) | `tid` (str, required, positional); `replies` (boolean, optional, default=False) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `detail`: Source-audited against OpenCLI 1.8.6 hupu/detail.js; reads public browser-rendered content without authenticated account state.
