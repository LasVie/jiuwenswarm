# Zhihu: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `answer` | `reversible_remote_write` / `high` | `opencli zhihu answer "<target>" ["<text>"] [--file "<file>"] [--execute <true\|false>] -f json`<br>Answer a Zhihu question | `target` (str, required, positional); `text` (str, optional, positional); `file` (str, optional); `execute` (boolean, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
