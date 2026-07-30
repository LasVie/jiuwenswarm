# Maimai: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search-talents` | `private_content_read` / `high` | `opencli maimai search-talents "<query>" [--page <page>] [--size <size>] [--positions "<positions>"] [--companies "<companies>"] [--schools "<schools>"] [--provinces "<provinces>"] [--cities "<cities>"] [--worktimes "<worktimes>"] [--degrees "<degrees>"] [--professions "<professions>"] [--is_211 <is_211>] [--is_985 <is_985>] [--sortby <sortby>] [--is_direct_chat <is_direct_chat>] -f json`<br>Search for candidates on Maimai with multi-dimensional filters | `query` (str, required, positional); `page` (int, optional, default=0); `size` (int, optional, default=20); `positions` (str, optional); `companies` (str, optional); `schools` (str, optional); `provinces` (str, optional); `cities` (str, optional); `worktimes` (str, optional); `degrees` (str, optional); `professions` (str, optional); `is_211` (int, optional); `is_985` (int, optional); `sortby` (int, optional, default=0); `is_direct_chat` (int, optional, default=0) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `search-talents`: Source-audited against OpenCLI 1.8.6 maimai/search-talents.js; reads authenticated enterprise talent-search results containing candidate personal data.; sensitive output: personal data, account identifiers
