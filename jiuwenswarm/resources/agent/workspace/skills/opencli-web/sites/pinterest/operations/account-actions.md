# Pinterest: account-actions

Change reversible account relationship or saved state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `save` | `reversible_remote_write` / `high` | `opencli pinterest save "<pin>" [--board "<board>"] [--section "<section>"] -f json`<br>Save a pin to your profile or a board | `pin` (string, required, positional); `board` (string, optional); `section` (string, optional, default='') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
