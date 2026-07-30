# 51Job: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `company` | `public_read` / `low` | `opencli 51job company "<encCoId>" [--limit <limit>] -f json`<br>51job 公司简介 + 在招职位（按 encCoId） | `encCoId` (string, required, positional); `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `detail` | `public_read` / `low` | `opencli 51job detail "<jobId>" -f json`<br>51job 职位详情（按 jobId） | `jobId` (string, required, positional) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `company`: Source-audited against OpenCLI 1.8.6 51job/company.js; reads public browser-rendered content without authenticated account state.
- `detail`: Source-audited against OpenCLI 1.8.6 51job/detail.js; reads public browser-rendered content without authenticated account state.
