# Chaoxing: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `assignments` | `private_content_read` / `medium` | `opencli chaoxing assignments [--course "<course>"] [--status "<all\|pending\|submitted\|graded>"] [--limit <limit>] [--timeout <timeout>] -f json`<br>学习通作业列表 | `course` (string, optional); `status` (string, optional, default='all', choices=all,pending,submitted,graded); `limit` (int, optional, default=20); `timeout` (int, optional, default=90) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `exams` | `private_content_read` / `medium` | `opencli chaoxing exams [--course "<course>"] [--status "<all\|upcoming\|ongoing\|finished>"] [--limit <limit>] [--timeout <timeout>] -f json`<br>学习通考试列表 | `course` (string, optional); `status` (string, optional, default='all', choices=all,upcoming,ongoing,finished); `limit` (int, optional, default=20); `timeout` (int, optional, default=90) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `assignments`: sensitive output: private content, account identifiers
- `exams`: sensitive output: private content, account identifiers
