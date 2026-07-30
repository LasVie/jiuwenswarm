# Semanticscholar: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `citations` | `public_read` / `low` | `opencli semanticscholar citations "<id>" [--limit <limit>] [--offset <offset>] -f json`<br>List papers that cite a Semantic Scholar paper (paginated) | `id` (str, required, positional); `limit` (int, optional, default=20); `offset` (int, optional, default=0) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `paper` | `public_read` / `low` | `opencli semanticscholar paper "<id>" -f json`<br>Semantic Scholar paper detail (citation graph + AI tldr) by paperId, DOI, or arXiv id | `id` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `recommendations` | `public_read` / `low` | `opencli semanticscholar recommendations "<id>" [--limit <limit>] -f json`<br>Semantic Scholar AI-curated related papers for a paperId, DOI, or arXiv id | `id` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
