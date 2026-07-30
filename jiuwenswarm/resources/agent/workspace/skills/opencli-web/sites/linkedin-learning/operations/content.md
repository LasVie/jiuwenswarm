# Linkedin Learning: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `course` | `public_read` / `low` | `opencli linkedin-learning course "<slug>" -f json`<br>Get LinkedIn Learning course detail by slug or course URL | `slug` (string, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `course`: Source-audited against OpenCLI 1.8.6 linkedin-learning/course.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
