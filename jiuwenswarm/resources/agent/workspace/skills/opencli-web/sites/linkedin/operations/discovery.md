# Linkedin: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli linkedin search "<query>" [--location "<location>"] [--limit <limit>] [--start <start>] [--details <true\|false>] [--company "<company>"] [--experience-level "<experience-level>"] [--job-type "<job-type>"] [--date-posted "<date-posted>"] [--remote "<remote>"] -f json`<br>Search LinkedIn jobs | `query` (string, required, positional); `location` (string, optional); `limit` (int, optional, default=10); `start` (int, optional, default=0); `details` (bool, optional, default=False); `company` (string, optional); `experience-level` (string, optional); `job-type` (string, optional); `date-posted` (string, optional); `remote` (string, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
