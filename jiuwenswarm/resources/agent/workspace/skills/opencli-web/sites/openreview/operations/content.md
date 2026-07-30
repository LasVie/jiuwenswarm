# Openreview: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `author` | `public_read` / `low` | `opencli openreview author "<profile>" [--limit <limit>] -f json`<br>List OpenReview submissions by an author profile id (newest first) | `profile` (str, required, positional); `limit` (int, optional, default=50) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `paper` | `public_read` / `low` | `opencli openreview paper "<id>" -f json`<br>Show full metadata for a single OpenReview paper | `id` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `reviews` | `public_read` / `low` | `opencli openreview reviews "<forum>" [--max-length <max-length>] -f json`<br>Show full review thread (paper + reviews + decisions) for an OpenReview forum | `forum` (str, required, positional); `max-length` (int, optional, default=4000) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `venue` | `public_read` / `low` | `opencli openreview venue "<venue>" [--limit <limit>] [--offset <offset>] -f json`<br>List papers at an OpenReview venue (e.g. "ICLR 2024 oral" or full invitation id) | `venue` (str, required, positional); `limit` (int, optional, default=25); `offset` (int, optional, default=0) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
