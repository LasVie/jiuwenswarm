# Rednote: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `comments` | `public_read` / `low` | `opencli rednote comments "<note-id>" [--limit <limit>] [--with-replies <true\|false>] -f json`<br>Read comments from a rednote note (supports nested replies) | `note-id` (str, required, positional); `limit` (int, optional, default=20); `with-replies` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `note` | `public_read` / `low` | `opencli rednote note "<note-id>" -f json`<br>Read note body and engagement counts from a rednote note | `note-id` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `user` | `public_read` / `low` | `opencli rednote user "<id>" [--limit <limit>] -f json`<br>Get public notes from a rednote user profile | `id` (str, required, positional); `limit` (int, optional, default=15) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
