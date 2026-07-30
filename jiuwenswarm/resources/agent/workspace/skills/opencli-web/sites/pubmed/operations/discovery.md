# Pubmed: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli pubmed search "<query>" [--limit <limit>] [--author "<author>"] [--journal "<journal>"] [--year-from <year-from>] [--year-to <year-to>] [--article-type "<article-type>"] [--has-abstract <true\|false>] [--free-full-text <true\|false>] [--humans-only <true\|false>] [--english-only <true\|false>] [--sort "<relevance\|date\|author\|journal>"] -f json`<br>Search PubMed articles with advanced filters | `query` (str, required, positional); `limit` (int, optional, default=20); `author` (str, optional); `journal` (str, optional); `year-from` (int, optional); `year-to` (int, optional); `article-type` (str, optional); `has-abstract` (boolean, optional, default=False); `free-full-text` (boolean, optional, default=False); `humans-only` (boolean, optional, default=False); `english-only` (boolean, optional, default=False); `sort` (str, optional, default='relevance', choices=relevance,date,author,journal) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
