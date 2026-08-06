# Trip: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `package` | `public_read` / `low` | `opencli trip package "<from>" "<to>" --depart "<depart>" --return "<return>" [--adults <adults>] [--limit <limit>] -f json`<br>Search Trip.com flight+hotel packages by route + dates; lists the package flight options priced at the bundle rate | `from` (str, required, positional); `to` (str, required, positional); `depart` (str, required); `return` (str, required); `adults` (int, optional, default=2); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
