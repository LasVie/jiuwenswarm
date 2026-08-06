# Midjourney: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `history` | `private_content_read` / `medium` | `opencli midjourney history [--limit <limit>] [--type "<type>"] [--status "<status>"] [--query "<query>"] -f json`<br>List recent Midjourney image, video, and derived jobs with real lifecycle status | `limit` (int, optional, default=10); `type` (str, optional, default='all'); `status` (str, optional, default='all'); `query` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `quota` | `private_content_read` / `medium` | `opencli midjourney quota -f json`<br>Show Midjourney quota, conservative batch estimates, and account-consumption trend | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `settings` | `private_content_read` / `medium` | `opencli midjourney settings -f json`<br>Read the currently selected Midjourney image and video settings from the visible Create UI | none | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `status` | `private_content_read` / `medium` | `opencli midjourney status "<job>" -f json`<br>Show the current state and metadata of one Midjourney job | `job` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `history`: sensitive output: private content, account identifiers
- `quota`: sensitive output: private content, account identifiers
- `settings`: sensitive output: private content, account identifiers
- `status`: sensitive output: private content, account identifiers
