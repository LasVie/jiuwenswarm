# Youtube: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `channel` | `public_read` / `low` | `opencli youtube channel "<id>" [--limit <limit>] -f json`<br>Get YouTube channel info and recent videos | `id` (str, required, positional); `limit` (int, optional, default=10) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `comments` | `public_read` / `low` | `opencli youtube comments "<url>" [--limit <limit>] -f json`<br>Get YouTube video comments | `url` (str, required, positional); `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `transcript` | `public_read` / `low` | `opencli youtube transcript "<url>" [--lang "<lang>"] [--mode "<mode>"] -f json`<br>Get YouTube video transcript/subtitles | `url` (str, required, positional); `lang` (str, optional); `mode` (str, optional, default='grouped') | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `video` | `public_read` / `low` | `opencli youtube video "<url>" -f json`<br>Get YouTube video metadata (title, views, description, etc.) | `url` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `channel`: Source-audited against OpenCLI 1.8.6 youtube/channel.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `comments`: Source-audited against OpenCLI 1.8.6 youtube/comments.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `transcript`: Source-audited against OpenCLI 1.8.6 youtube/transcript.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.; file outputs: workspace-relative output
- `video`: Source-audited against OpenCLI 1.8.6 youtube/video.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
