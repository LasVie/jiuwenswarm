# Xiaohongshu: notes

Read Xiaohongshu note and notification data.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `comments` | `private_content_read` / `medium` | `opencli xiaohongshu comments "<full-note-url-with-xsec-token>" [--limit <limit>] [--with-replies <true\|false>] -f json`<br>获取小红书笔记评论（支持楼中楼子回复） | `note-id` (str, required, positional); `limit` (int, optional, default=20); `with-replies` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `download` | `local_write` / `high` | `opencli xiaohongshu download "<full-note-url-with-xsec-token-or-xhslink>" [--output "<output>"] -f json`<br>下载小红书笔记中的图片和视频 | `note-id` (str, required, positional); `output` (str, optional, default='./xiaohongshu-downloads') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `liked` | `private_content_read` / `medium` | `opencli xiaohongshu liked [--id "<id>"] [--limit <limit>] -f json`<br>小红书赞过笔记列表 | `id` (string, optional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `note` | `private_content_read` / `medium` | `opencli xiaohongshu note "<full-note-url-with-xsec-token>" -f json`<br>获取小红书笔记正文和互动数据 | `note-id` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `notifications` | `private_content_read` / `medium` | `opencli xiaohongshu notifications [--type "<type>"] [--limit <limit>] -f json`<br>小红书通知 (mentions/likes/connections) | `type` (str, optional, default='mentions'); `limit` (int, optional, default=20) | auth=required; transport=browser_intercept; fallback_before=browser_agent; fallback_after=none |
| `saved` | `private_content_read` / `medium` | `opencli xiaohongshu saved [--id "<id>"] [--limit <limit>] -f json`<br>小红书收藏笔记列表 | `id` (string, optional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `user` | `private_content_read` / `medium` | `opencli xiaohongshu user "<id>" [--limit <limit>] -f json`<br>Get public notes from a Xiaohongshu user profile | `id` (string, required, positional); `limit` (int, optional, default=15) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `comments`: Always pass the original full Xiaohongshu note URL containing xsec_token. Copy the complete URL unchanged, including its query string; never extract or substitute a bare note ID; sensitive output: private content, account identifiers
- `download`: Always pass the original full Xiaohongshu note URL containing xsec_token, or an xhslink short URL. Copy a signed URL unchanged, including its query string; never extract or substitute a bare note ID; file outputs: workspace-relative output
- `liked`: sensitive output: private content, account identifiers
- `note`: Always pass the original full Xiaohongshu note URL containing xsec_token. Copy the complete URL unchanged, including its query string; never extract or substitute a bare note ID; sensitive output: private content, account identifiers
- `notifications`: sensitive output: private content, account identifiers
- `saved`: sensitive output: private content, account identifiers
- `user`: sensitive output: private content, account identifiers
