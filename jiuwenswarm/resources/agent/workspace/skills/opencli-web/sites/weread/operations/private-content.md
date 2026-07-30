# Weread: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `ai-outline` | `private_content_read` / `medium` | `opencli weread ai-outline "<book-id>" [--limit <limit>] [--depth <depth>] [--raw <true\|false>] -f json`<br>Get AI-generated outline for a book | `book-id` (str, required, positional); `limit` (int, optional, default=200); `depth` (int, optional, default=4); `raw` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `highlights` | `private_content_read` / `medium` | `opencli weread highlights "<book-id>" [--limit <limit>] -f json`<br>List your highlights (underlines) in a book | `book-id` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `notebooks` | `private_content_read` / `medium` | `opencli weread notebooks -f json`<br>List books that have highlights or notes | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `notes` | `private_content_read` / `medium` | `opencli weread notes "<book-id>" [--limit <limit>] -f json`<br>List your notes (thoughts) on a book | `book-id` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `shelf` | `private_content_read` / `medium` | `opencli weread shelf [--limit <limit>] -f json`<br>List books on your WeRead bookshelf | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `ai-outline`: Source-audited against OpenCLI 1.8.6 weread/ai-outline.js; retrieves an existing account-accessible outline and does not request new AI generation or consume generation quota.; sensitive output: licensed book-derived content, account identifiers
- `highlights`: Source-audited against OpenCLI 1.8.6 weread/highlights.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private reading data, account identifiers
- `notebooks`: Source-audited against OpenCLI 1.8.6 weread/notebooks.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private reading data, account identifiers
- `notes`: Source-audited against OpenCLI 1.8.6 weread/notes.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private reading data, account identifiers
- `shelf`: Source-audited against OpenCLI 1.8.6 weread/shelf.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private reading data, account identifiers
