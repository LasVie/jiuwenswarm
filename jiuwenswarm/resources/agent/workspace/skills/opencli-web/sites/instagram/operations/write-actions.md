# Instagram: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `note` | `reversible_remote_write` / `high` | `opencli instagram note "<content>" [--timeout <timeout>] -f json`<br>Publish a text Instagram note | `content` (str, required, positional); `timeout` (int, optional, default=120) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `reel` | `reversible_remote_write` / `high` | `opencli instagram reel [--video "<video>"] ["<content>"] [--timeout <timeout>] -f json`<br>Post an Instagram reel video | `video` (str, optional); `content` (str, optional, positional); `timeout` (int, optional, default=600) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `story` | `reversible_remote_write` / `high` | `opencli instagram story [--media "<media>"] [--timeout <timeout>] -f json`<br>Post a single Instagram story image or video | `media` (str, optional); `timeout` (int, optional, default=300) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `unlike` | `reversible_remote_write` / `high` | `opencli instagram unlike "<username>" [--index <index>] -f json`<br>Unlike an Instagram post | `username` (str, required, positional); `index` (int, optional, default=1) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `unsave` | `reversible_remote_write` / `high` | `opencli instagram unsave "<username>" [--index <index>] -f json`<br>Unsave (remove bookmark) an Instagram post | `username` (str, required, positional); `index` (int, optional, default=1) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
