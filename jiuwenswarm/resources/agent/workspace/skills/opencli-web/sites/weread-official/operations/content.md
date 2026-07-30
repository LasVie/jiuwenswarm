# Weread Official: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `review` | `public_read` / `low` | `opencli weread-official review "<bookId>" [--type "<all\|recommend\|thumbs-down\|newest\|neutral>"] [--count <count>] [--max-idx <max-idx>] [--synckey <synckey>] -f json`<br>Browse public reviews of a WeRead book | `bookId` (str, required, positional); `type` (str, optional, default='all', choices=all,recommend,thumbs-down,newest,neutral); `count` (int, optional, default=20); `max-idx` (int, optional, default=0); `synckey` (int, optional) | auth=required; transport=public_http; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `review`: Requires WEREAD_API_KEY although the returned reviews are public.
