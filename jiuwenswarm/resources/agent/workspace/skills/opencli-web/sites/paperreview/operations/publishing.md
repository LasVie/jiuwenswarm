# Paperreview: publishing

Publish, create, edit, or upload remote content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `submit` | `public_write` / `high` | `opencli paperreview submit "<pdf>" --email "<email>" [--venue "<venue>"] [--dry-run <true\|false>] [--prepare-only <true\|false>] [--timeout <timeout>] -f json`<br>Submit a PDF to paperreview.ai for review | `pdf` (str, required, positional); `email` (str, required); `venue` (str, optional); `dry-run` (bool, optional, default=False); `prepare-only` (bool, optional, default=False); `timeout` (int, optional, default=120) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `submit`: file inputs: workspace-relative input when declared by adapter
