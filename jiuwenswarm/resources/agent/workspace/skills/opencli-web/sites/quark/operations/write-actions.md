# Quark: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `mkdir` | `reversible_remote_write` / `high` | `opencli quark mkdir "<name>" [--parent "<parent>"] [--parent-fid "<parent-fid>"] -f json`<br>Create a folder in your Quark Drive | `name` (str, required, positional); `parent` (str, optional); `parent-fid` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `mv` | `reversible_remote_write` / `high` | `opencli quark mv "<fids>" [--to "<to>"] [--to-fid "<to-fid>"] [--timeout <timeout>] -f json`<br>Move files to a folder in your Quark Drive | `fids` (str, required, positional); `to` (str, optional, default=''); `to-fid` (str, optional, default=''); `timeout` (int, optional, default=120) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `rename` | `reversible_remote_write` / `high` | `opencli quark rename "<fid>" --name "<name>" -f json`<br>Rename a file in your Quark Drive | `fid` (str, required, positional); `name` (str, required) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `rm` | `reversible_remote_write` / `high` | `opencli quark rm "<fids>" -f json`<br>Delete files from your Quark Drive | `fids` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
