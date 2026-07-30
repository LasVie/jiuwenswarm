# Nuget

- Site slug: `nuget`
- Domains: `api.nuget.org`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `package`, `search` | `sites/nuget/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `package` | `public_read` / `low` | `opencli nuget package "<id>" -f json`<br>Full NuGet package version history (catalogEntry per release) | `id` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli nuget search "<query>" [--limit <limit>] [--prerelease <true\|false>] -f json`<br>Search NuGet packages by keyword | `query` (str, required, positional); `limit` (int, optional, default=20); `prerelease` (boolean, optional, default=False) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
