# Ones: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `worklog` | `reversible_remote_write` / `high` | `opencli ones worklog "<task>" "<hours>" [--team "<team>"] [--date "<date>"] [--note "<note>"] [--owner "<owner>"] -f json`<br>ONES — log work hours on a task (defaults to today; use --date to backfill; endpoint falls back by deployment). | `task` (str, required, positional); `hours` (str, required, positional); `team` (str, optional); `date` (str, optional); `note` (str, optional); `owner` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
