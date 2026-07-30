# Weread Official: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `list-apis` | `public_read` / `low` | `opencli weread-official list-apis -f json`<br>List every api_name supported by the WeRead agent gateway | none | auth=required; transport=public_http; fallback_before=browser_agent; fallback_after=none |
| `search` | `public_read` / `low` | `opencli weread-official search "<keyword>" [--scope "<all\|ebook\|webnovel\|audio\|author\|fulltext\|booklist\|mp\|article>"] [--count <count>] [--max-idx <max-idx>] -f json`<br>Search WeRead store via the official agent gateway | `keyword` (str, required, positional); `scope` (str, optional, default='ebook', choices=all,ebook,webnovel,audio,author,fulltext,booklist,mp,article); `count` (int, optional); `max-idx` (int, optional, default=0) | auth=required; transport=public_http; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `list-apis`: Requires WEREAD_API_KEY for the official WeRead gateway.
- `search`: Requires WEREAD_API_KEY although the returned store results are public.
