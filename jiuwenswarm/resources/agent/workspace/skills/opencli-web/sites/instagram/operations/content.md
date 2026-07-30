# Instagram: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `profile` | `public_read` / `low` | `opencli instagram profile "<username>" -f json`<br>Get Instagram user profile info | `username` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `profile`: Source-audited against OpenCLI 1.8.6 instagram/profile.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
