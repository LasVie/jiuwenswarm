# Twitter: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `hide-reply` | `message_send` / `high` | `opencli twitter hide-reply "<url>" -f json`<br>Hide a reply on your tweet (useful for hiding bot/spam replies) | `url` (string, required, positional) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `reply` | `message_send` / `high` | `opencli twitter reply "<url>" "<text>" [--image "<image>"] [--image-url "<image-url>"] -f json`<br>Reply to a specific tweet, optionally with a local or remote image | `url` (string, required, positional); `text` (string, required, positional); `image` (str, optional); `image-url` (str, optional) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `reply-dm` | `message_send` / `high` | `opencli twitter reply-dm "<text>" [--max <max>] [--skip-replied <true\|false>] [--timeout <timeout>] -f json`<br>Send a message to recent DM conversations | `text` (string, required, positional); `max` (int, optional, default=20); `skip-replied` (boolean, optional, default=True); `timeout` (int, optional, default=600) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
