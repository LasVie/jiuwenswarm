# Zhihu: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `answer-comments` | `public_read` / `low` | `opencli zhihu answer-comments "<id>" [--limit <limit>] [--replies-limit <replies-limit>] -f json`<br>知乎回答评论列表 | `id` (str, required, positional); `limit` (int, optional, default=20); `replies-limit` (int, optional, default=3) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `answer-detail` | `public_read` / `low` | `opencli zhihu answer-detail "<id>" [--max-content <max-content>] -f json`<br>知乎单个回答完整内容（按 answer ID 获取） | `id` (str, required, positional); `max-content` (int, optional, default=0) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `question` | `public_read` / `low` | `opencli zhihu question "<id>" [--limit <limit>] [--sort "<default\|created>"] -f json`<br>知乎问题详情和回答 | `id` (str, required, positional); `limit` (int, optional, default=5); `sort` (str, optional, default='default', choices=default,created) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `user` | `public_read` / `low` | `opencli zhihu user "<user>" -f json`<br>知乎用户主页资料（粉丝/关注/回答/文章/获赞数） | `user` (string, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `answer-comments`: Source-audited against OpenCLI 1.8.6 zhihu/answer-comments.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `answer-detail`: Source-audited against OpenCLI 1.8.6 zhihu/answer-detail.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `question`: Source-audited against OpenCLI 1.8.6 zhihu/question.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `user`: Source-audited against OpenCLI 1.8.6 zhihu/user.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
