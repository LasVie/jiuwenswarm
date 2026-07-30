# Ones: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `my-tasks` | `private_content_read` / `medium` | `opencli ones my-tasks ["<team>"] [--limit <limit>] [--mode "<assign\|field004\|owner\|both>"] -f json`<br>ONES — my work items (filters/peek + strict must query). Default: assignee=me. Use --mode if your site uses field004 for assignee. | `team` (str, optional, positional); `limit` (int, optional, default=100); `mode` (str, optional, default='assign', choices=assign,field004,owner,both) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `task` | `private_content_read` / `medium` | `opencli ones task "<id>" [--team "<team>"] -f json`<br>ONES — work item detail (GET team/:team/task/:id/info); id is URL segment after …/task/ | `id` (str, required, positional); `team` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `tasks` | `private_content_read` / `medium` | `opencli ones tasks ["<team>"] [--project "<project>"] [--assign "<assign>"] [--limit <limit>] -f json`<br>ONES Project API — list work items (POST team/:team/filters/peek); use token-info -f json for team uuid | `team` (str, optional, positional); `project` (str, optional); `assign` (str, optional); `limit` (int, optional, default=30) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `my-tasks`: sensitive output: private content, account identifiers
- `task`: sensitive output: private content, account identifiers
- `tasks`: sensitive output: private content, account identifiers
