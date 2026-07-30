# Maven

- Site slug: `maven`
- Domains: `search.maven.org`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `artifact`, `search` | `sites/maven/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `artifact` | `public_read` / `low` | `opencli maven artifact "<coordinate>" [--limit <limit>] -f json`<br>Fetch a Maven Central artifact's version history (groupId:artifactId[:version]) | `coordinate` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli maven search "<query>" [--limit <limit>] -f json`<br>Search Maven Central by keyword (artifact name, groupId, tag) | `query` (str, required, positional); `limit` (int, optional, default=30) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
