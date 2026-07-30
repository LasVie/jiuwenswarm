# Weibo: destructive-actions

Delete, remove, revoke, or perform administrative changes.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `delete` | `destructive_or_admin` / `critical` | `opencli weibo delete "<id>" -f json`<br>Delete one of my Weibo posts by id | `id` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
