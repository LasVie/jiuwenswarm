# Weread: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `book` | `public_read` / `low` | `opencli weread book "<book-id>" -f json`<br>View book details on WeRead | `book-id` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `book`: Source-audited against OpenCLI 1.8.6 weread/book.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
