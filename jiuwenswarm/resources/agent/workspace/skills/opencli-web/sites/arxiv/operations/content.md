# Arxiv: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `author` | `public_read` / `low` | `opencli arxiv author "<author>" [--limit <limit>] -f json`<br>List arXiv papers by a given author (newest first) | `author` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `paper` | `public_read` / `low` | `opencli arxiv paper "<id>" -f json`<br>Get arXiv paper details by ID | `id` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `recent` | `public_read` / `low` | `opencli arxiv recent "<category>" [--limit <limit>] -f json`<br>List recent arXiv submissions in a category | `category` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
