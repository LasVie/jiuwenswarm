# Linkedin: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `company` | `private_content_read` / `medium` | `opencli linkedin company "<company>" -f json`<br>Read a LinkedIn company page: industry, size, HQ, founded, website, followers, about | `company` (string, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `connections` | `private_content_read` / `medium` | `opencli linkedin connections [--limit <limit>] -f json`<br>List your LinkedIn first-degree connections (name, headline, profile URL) | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `inbox` | `private_content_read` / `medium` | `opencli linkedin inbox [--limit <limit>] [--unread-only <true\|false>] -f json`<br>List LinkedIn messaging inbox conversations and unread messages | `limit` (int, optional, default=40); `unread-only` (bool, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `jobs-preferences` | `private_content_read` / `medium` | `opencli linkedin jobs-preferences -f json`<br>Read visible LinkedIn Jobs preferences and alert settings without changing them | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `people-search` | `private_content_read` / `medium` | `opencli linkedin people-search "<keywords>" [--limit <limit>] -f json`<br>Search standard LinkedIn (not Sales Navigator) for people by keyword. Each invocation consumes against LinkedIn's monthly Commercial Use Limit on people search; throttle accordingly. | `keywords` (string, required, positional); `limit` (int, optional, default=5) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `post-analytics` | `private_content_read` / `medium` | `opencli linkedin post-analytics [--profile-url "<profile-url>"] [--limit <limit>] -f json`<br>Summarize raw visible LinkedIn post counters without custom scoring or classification | `profile-url` (string, optional); `limit` (int, optional, default=30) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `posts` | `private_content_read` / `medium` | `opencli linkedin posts [--profile-url "<profile-url>"] [--limit <limit>] -f json`<br>Export visible posts from a LinkedIn profile activity page with engagement metrics | `profile-url` (string, optional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `salesnav-inbox` | `private_content_read` / `medium` | `opencli linkedin salesnav-inbox [--limit <limit>] [--max-pages <max-pages>] [--unread-only <true\|false>] -f json`<br>List LinkedIn Sales Navigator message conversations with API pagination | `limit` (number, optional, default=40); `max-pages` (number, optional, default=30); `unread-only` (bool, optional, default=False) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `salesnav-search` | `private_content_read` / `medium` | `opencli linkedin salesnav-search "<keywords>" [--limit <limit>] -f json`<br>Search LinkedIn Sales Navigator for people leads by keyword | `keywords` (string, required, positional); `limit` (number, optional, default=25) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `salesnav-thread` | `private_content_read` / `medium` | `opencli linkedin salesnav-thread "<thread-or-recipient>" [--limit <limit>] [--max-pages <max-pages>] -f json`<br>Return full Sales Navigator message history for a thread id, Sales Navigator inbox URL, lead URL, recipient urn, or exact recipient name | `thread-or-recipient` (string, required, positional); `limit` (number, optional, default=200); `max-pages` (number, optional, default=30) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `sent-invitations` | `private_content_read` / `medium` | `opencli linkedin sent-invitations -f json`<br>List pending LinkedIn sent invitations for CRM reconciliation | none | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `services-read` | `private_content_read` / `medium` | `opencli linkedin services-read [--profile-url "<profile-url>"] [--services-url "<services-url>"] -f json`<br>Read LinkedIn Services page details including services, overview, availability, pricing, and media titles/descriptions | `profile-url` (string, optional); `services-url` (string, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `thread-snapshot` | `private_content_read` / `medium` | `opencli linkedin thread-snapshot --thread-url "<thread-url>" [--max-scrolls <max-scrolls>] [--json <true\|false>] -f json`<br>Load a LinkedIn messaging thread, scroll for available history, and return a full context snapshot | `thread-url` (str, required); `max-scrolls` (number, optional, default=30); `json` (bool, optional, default=False) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `timeline` | `private_content_read` / `medium` | `opencli linkedin timeline [--limit <limit>] -f json`<br>Read LinkedIn home timeline posts | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `company`: sensitive output: private content, account identifiers
- `connections`: sensitive output: private content, account identifiers
- `inbox`: sensitive output: private content, account identifiers
- `jobs-preferences`: sensitive output: private content, account identifiers
- `people-search`: sensitive output: private content, account identifiers
- `post-analytics`: sensitive output: private content, account identifiers
- `posts`: sensitive output: private content, account identifiers
- `salesnav-inbox`: sensitive output: private content, account identifiers
- `salesnav-search`: sensitive output: private content, account identifiers
- `salesnav-thread`: sensitive output: private content, account identifiers
- `sent-invitations`: sensitive output: private content, account identifiers
- `services-read`: sensitive output: private content, account identifiers
- `thread-snapshot`: sensitive output: private content, account identifiers
- `timeline`: sensitive output: private content, account identifiers
