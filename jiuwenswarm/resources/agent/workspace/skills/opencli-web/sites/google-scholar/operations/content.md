# Google Scholar: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `cite` | `public_read` / `low` | `opencli google-scholar cite "<query>" [--style "<bibtex\|endnote\|refman\|refworks>"] [--index <index>] -f json`<br>Get citation for a Google Scholar paper | `query` (str, required, positional); `style` (str, optional, default='bibtex', choices=bibtex,endnote,refman,refworks); `index` (int, optional, default=1) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
| `profile` | `public_read` / `low` | `opencli google-scholar profile "<author>" [--limit <limit>] -f json`<br>View a Google Scholar author profile | `author` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
