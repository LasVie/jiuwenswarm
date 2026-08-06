# Pinterest: destructive-actions

Delete, remove, revoke, or perform administrative changes.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `board-delete` | `destructive_or_admin` / `critical` | `opencli pinterest board-delete "<board>" [--confirm <true\|false>] -f json`<br>Delete one of your own boards | `board` (string, required, positional); `confirm` (bool, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `board-section-delete` | `destructive_or_admin` / `critical` | `opencli pinterest board-section-delete "<board>" --section "<section>" [--confirm <true\|false>] -f json`<br>Delete a section from one of your boards | `board` (string, required, positional); `section` (string, required); `confirm` (bool, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `pin-delete` | `destructive_or_admin` / `critical` | `opencli pinterest pin-delete "<pin>" [--confirm <true\|false>] -f json`<br>Delete one of your own pins | `pin` (string, required, positional); `confirm` (bool, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
