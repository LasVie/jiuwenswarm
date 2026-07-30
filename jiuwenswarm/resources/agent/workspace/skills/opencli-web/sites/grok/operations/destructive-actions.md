# Grok: destructive-actions

Delete, remove, revoke, or perform administrative changes.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `delete` | `destructive_or_admin` / `critical` | `opencli grok delete "<id>" [--yes <true\|false>] -f json`<br>Delete a Grok conversation by ID. Grok takes effect immediately with no confirmation dialog — require --yes to actually delete. | `id` (string, required, positional); `yes` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
