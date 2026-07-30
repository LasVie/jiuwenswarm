# Nvd

- Site slug: `nvd`
- Domains: `services.nvd.nist.gov`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `cve` | `sites/nvd/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `cve` | `public_read` / `low` | `opencli nvd cve "<id>" -f json`<br>NIST NVD CVE detail (description, CVSS, CWE, KEV flag) | `id` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
