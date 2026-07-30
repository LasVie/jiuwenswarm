# Paperreview: private-content

Read private review content addressed by a bearer capability token.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `review` | `private_content_read` / `high` | `opencli paperreview review "<token>" [--timeout <timeout>] -f json`<br>Fetch a paperreview.ai review by token | `token` (str, required, positional); `timeout` (int, optional, default=30) | auth=required; transport=public_http; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `review`: Requires a bearer capability token; public HTTP transport does not make the review data public.; sensitive output: review token, private review content
