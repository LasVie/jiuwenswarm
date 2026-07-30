# Paperreview: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `feedback` | `reversible_remote_write` / `high` | `opencli paperreview feedback "<token>" --helpfulness <helpfulness> --critical-error "<yes\|no>" --actionable-suggestions "<yes\|no>" [--additional-comments "<additional-comments>"] [--timeout <timeout>] -f json`<br>Submit feedback for a paperreview.ai review token | `token` (str, required, positional); `helpfulness` (int, required); `critical-error` (str, required, choices=yes,no); `actionable-suggestions` (str, required, choices=yes,no); `additional-comments` (str, optional); `timeout` (int, optional, default=30) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=none |
