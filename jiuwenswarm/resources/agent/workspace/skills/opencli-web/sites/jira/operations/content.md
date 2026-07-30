# Jira: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `attachments` | `private_content_read` / `high` | `opencli jira attachments "<key>" -f json`<br>Jira issue attachment metadata | `key` (str, required, positional) | auth=required; transport=public_http; fallback_before=none; fallback_after=none |
| `comments` | `private_content_read` / `high` | `opencli jira comments "<key>" [--limit <limit>] -f json`<br>Jira issue comments as Markdown | `key` (str, required, positional); `limit` (int, optional, default=50) | auth=required; transport=public_http; fallback_before=none; fallback_after=none |
| `issue` | `private_content_read` / `high` | `opencli jira issue "<key>" [--comments-limit <comments-limit>] -f json`<br>Jira issue detail normalized for agents (description, comments, attachments, links) | `key` (str, required, positional); `comments-limit` (int, optional, default=100) | auth=required; transport=public_http; fallback_before=none; fallback_after=none |
| `links` | `private_content_read` / `high` | `opencli jira links "<key>" -f json`<br>Jira issue links | `key` (str, required, positional) | auth=required; transport=public_http; fallback_before=none; fallback_after=none |

## Operation-specific constraints

- `attachments`: Requires a configured Jira base URL and secret-bound authentication.; sensitive output: private issue content, attachment URLs, account identifiers
- `comments`: Requires a configured Jira base URL and secret-bound authentication.; sensitive output: private issue comments, account identifiers
- `issue`: Requires a configured Jira base URL and secret-bound authentication.; sensitive output: private issue content, account identifiers
- `links`: Requires a configured Jira base URL and secret-bound authentication.; sensitive output: private issue links, account identifiers
