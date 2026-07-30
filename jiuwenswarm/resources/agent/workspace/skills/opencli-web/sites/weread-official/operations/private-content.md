# Weread Official: private-content

Read credential-gated personal WeRead content and account activity.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `book` | `private_content_read` / `medium` | `opencli weread-official book "<bookId>" [--no-chapters <true\|false>] [--no-progress <true\|false>] -f json`<br>Show WeRead book metadata, chapters, and reading progress | `bookId` (str, required, positional); `no-chapters` (boolean, optional, default=False); `no-progress` (boolean, optional, default=False) | auth=required; transport=public_http; fallback_before=browser_agent; fallback_after=none |
| `discover` | `private_content_read` / `medium` | `opencli weread-official discover ["<bookId>"] [--count <count>] [--max-idx <max-idx>] [--session-id "<session-id>"] -f json`<br>Personalized or similar-book recommendations from WeRead | `bookId` (str, optional, positional); `count` (int, optional, default=12); `max-idx` (int, optional, default=0); `session-id` (str, optional) | auth=required; transport=public_http; fallback_before=browser_agent; fallback_after=none |
| `notes` | `private_content_read` / `medium` | `opencli weread-official notes ["<bookId>"] [--count <count>] [--last-sort <last-sort>] -f json`<br>List notebooks overview or merged highlights+thoughts for a book | `bookId` (str, optional, positional); `count` (int, optional, default=20); `last-sort` (int, optional) | auth=required; transport=public_http; fallback_before=browser_agent; fallback_after=none |
| `readdata` | `private_content_read` / `medium` | `opencli weread-official readdata [--mode "<weekly\|monthly\|annually\|overall>"] [--base-time <base-time>] -f json`<br>Reading statistics: time, streak, preferences, top books | `mode` (str, optional, default='monthly', choices=weekly,monthly,annually,overall); `base-time` (int, optional) | auth=required; transport=public_http; fallback_before=browser_agent; fallback_after=none |
| `shelf` | `private_content_read` / `medium` | `opencli weread-official shelf -f json`<br>Sync your WeRead shelf (books + albums + article bookmark entry) via the official gateway | none | auth=required; transport=public_http; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `book`: Requires WEREAD_API_KEY for the official WeRead gateway.; sensitive output: private content, account identifiers
- `discover`: Requires WEREAD_API_KEY for personalized recommendations.; sensitive output: private content, account identifiers
- `notes`: Requires WEREAD_API_KEY; results can contain personal highlights and thoughts.; sensitive output: private content, account identifiers
- `readdata`: Requires WEREAD_API_KEY; results contain account-scoped reading activity.; sensitive output: private content, account identifiers
- `shelf`: Requires WEREAD_API_KEY; results contain the account's shelf and bookmarks.; sensitive output: private content, account identifiers
