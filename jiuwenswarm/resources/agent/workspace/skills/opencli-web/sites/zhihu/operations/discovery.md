# Zhihu: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `followers` | `public_read` / `low` | `opencli zhihu followers "<user>" [--limit <limit>] -f json`<br>知乎某用户的粉丝列表 | `user` (string, required, positional); `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `following` | `public_read` / `low` | `opencli zhihu following "<user>" [--limit <limit>] -f json`<br>知乎某用户关注的人列表 | `user` (string, required, positional); `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `hot` | `public_read` / `low` | `opencli zhihu hot [--limit <limit>] -f json`<br>知乎热榜 | `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `pins` | `public_read` / `low` | `opencli zhihu pins "<user>" [--limit <limit>] -f json`<br>知乎某用户的想法（短内容）列表 | `user` (string, required, positional); `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli zhihu search "<query>" [--limit <limit>] [--type "<all\|answer\|article\|question>"] -f json`<br>知乎搜索 | `query` (str, required, positional); `limit` (int, optional, default=10); `type` (str, optional, default='all', choices=all,answer,article,question) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `user-answers` | `public_read` / `low` | `opencli zhihu user-answers "<user>" [--limit <limit>] -f json`<br>知乎某用户的回答列表 | `user` (string, required, positional); `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `user-articles` | `public_read` / `low` | `opencli zhihu user-articles "<user>" [--limit <limit>] -f json`<br>知乎某用户的文章/专栏列表 | `user` (string, required, positional); `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `followers`: Source-audited against OpenCLI 1.8.6 zhihu/followers.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `following`: Source-audited against OpenCLI 1.8.6 zhihu/following.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `hot`: Source-audited against OpenCLI 1.8.6 zhihu/hot.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `pins`: Source-audited against OpenCLI 1.8.6 zhihu/pins.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `search`: Source-audited against OpenCLI 1.8.6 zhihu/search.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `user-answers`: Source-audited against OpenCLI 1.8.6 zhihu/user-answers.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `user-articles`: Source-audited against OpenCLI 1.8.6 zhihu/user-articles.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
