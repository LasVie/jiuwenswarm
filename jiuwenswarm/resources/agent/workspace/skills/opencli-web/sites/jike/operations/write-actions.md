# Jike: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `repost` | `reversible_remote_write` / `high` | `opencli jike repost "<id>" ["<text>"] -f json`<br>转发即刻帖子 | `id` (string, required, positional); `text` (string, optional, positional) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
