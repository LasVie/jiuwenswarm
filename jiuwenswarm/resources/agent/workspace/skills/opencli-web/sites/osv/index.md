# Osv

- Site slug: `osv`
- Domains: `osv.dev`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `query`, `vulnerability` | `sites/osv/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `query` | `public_read` / `low` | `opencli osv query "<package>" --ecosystem "<ecosystem>" [--version "<version>"] [--limit <limit>] -f json`<br>OSV.dev vulnerabilities affecting a package (optionally pinned to a version) | `package` (string, required, positional); `ecosystem` (string, required); `version` (string, optional); `limit` (int, optional, default=30) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `vulnerability` | `public_read` / `low` | `opencli osv vulnerability "<id>" -f json`<br>Single OSV.dev vulnerability detail (severity, affected packages, CVE/GHSA aliases) | `id` (string, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
