# Archive: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `item` | `public_read` / `low` | `opencli archive item "<identifier>" -f json`<br>Fetch metadata for a single Internet Archive item by identifier. | `identifier` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `snapshots` | `public_read` / `low` | `opencli archive snapshots "<url>" [--from "<from>"] [--to "<to>"] [--limit <limit>] -f json`<br>List Wayback Machine snapshots over time for a URL via the CDX API. | `url` (str, required, positional); `from` (string, optional); `to` (string, optional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `wayback` | `public_read` / `low` | `opencli archive wayback "<url>" [--timestamp "<timestamp>"] -f json`<br>Look up the closest Wayback Machine snapshot for a URL. | `url` (str, required, positional); `timestamp` (string, optional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
