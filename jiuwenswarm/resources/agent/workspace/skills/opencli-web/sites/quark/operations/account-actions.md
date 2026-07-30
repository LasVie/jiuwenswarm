# Quark: account-actions

Change reversible account relationship or saved state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `save` | `reversible_remote_write` / `high` | `opencli quark save "<url>" [--to "<to>"] [--to-fid "<to-fid>"] [--fids "<fids>"] [--stoken "<stoken>"] [--passcode "<passcode>"] [--timeout <timeout>] -f json`<br>Save shared files to your Quark Drive | `url` (str, required, positional); `to` (str, optional, default=''); `to-fid` (str, optional, default=''); `fids` (str, optional, default=''); `stoken` (str, optional, default=''); `passcode` (str, optional, default=''); `timeout` (int, optional, default=120) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
