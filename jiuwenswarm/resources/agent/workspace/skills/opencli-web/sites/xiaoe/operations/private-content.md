# Xiaoe: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `catalog` | `private_content_read` / `medium` | `opencli xiaoe catalog "<url>" -f json`<br>小鹅通课程目录（支持普通课程、专栏、大专栏） | `url` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `content` | `private_content_read` / `medium` | `opencli xiaoe content "<url>" -f json`<br>提取小鹅通图文页面内容为文本 | `url` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `courses` | `private_content_read` / `medium` | `opencli xiaoe courses -f json`<br>列出已购小鹅通课程（含 URL 和店铺名） | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `play-url` | `private_content_read` / `medium` | `opencli xiaoe play-url "<url>" -f json`<br>小鹅通视频/音频/直播回放 M3U8 播放地址 | `url` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `catalog`: Source-audited against OpenCLI 1.8.6 xiaoe/catalog.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private course content, account identifiers
- `content`: Source-audited against OpenCLI 1.8.6 xiaoe/content.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private course content, account identifiers
- `courses`: Source-audited against OpenCLI 1.8.6 xiaoe/courses.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: purchase history, account identifiers
- `play-url`: Source-audited against OpenCLI 1.8.6 xiaoe/play-url.js; reads account-authorized media playback URLs that can be signed or access-scoped and must not be persisted or shared.; sensitive output: private course media URL, account identifiers
