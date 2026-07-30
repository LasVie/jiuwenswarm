# Zhihu: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `comment` | `message_send` / `high` | `opencli zhihu comment "<target>" ["<text>"] [--file "<file>"] [--execute <true\|false>] -f json`<br>Create a top-level comment on a Zhihu answer or article | `target` (str, required, positional); `text` (str, optional, positional); `file` (str, optional); `execute` (boolean, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
