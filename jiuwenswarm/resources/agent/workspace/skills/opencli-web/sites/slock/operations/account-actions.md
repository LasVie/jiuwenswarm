# Slock: account-actions

Change reversible account relationship or saved state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `bookmark-add` | `reversible_remote_write` / `high` | `opencli slock bookmark-add "<messageId>" [--server "<server>"] -f json`<br>Bookmark a message (POST /channels/saved). Requires full messageId UUID. | `messageId` (str, required, positional); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `thread-follow` | `reversible_remote_write` / `high` | `opencli slock thread-follow "<parentMessageId>" [--server "<server>"] -f json`<br>Follow the thread on a parent message (POST /channels/threads/follow) | `parentMessageId` (str, required, positional); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
