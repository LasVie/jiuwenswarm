# Pypi

- Site slug: `pypi`
- Domains: `pypi.org`, `pypistats.org`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `downloads`, `package` | `sites/pypi/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `downloads` | `public_read` / `low` | `opencli pypi downloads "<name>" [--period "<period>"] -f json`<br>PyPI download stats for a package (recent totals or full daily history) | `name` (str, required, positional); `period` (str, optional, default='recent') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `package` | `public_read` / `low` | `opencli pypi package "<name>" -f json`<br>Single PyPI package metadata (latest version, license, homepage, classifiers) | `name` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
