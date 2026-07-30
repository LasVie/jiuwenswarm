# Chatgpt: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `send` | `message_send` / `high` | `opencli chatgpt send "<prompt>" [--new <true\|false>] [--conversation "<conversation>"] [--project "<project>"] -f json`<br>Send a prompt to ChatGPT web without waiting for the response | `prompt` (str, required, positional); `new` (boolean, optional, default=False); `conversation` (str, optional); `project` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
