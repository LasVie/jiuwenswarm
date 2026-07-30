# Geogebra: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `info` | `private_content_read` / `medium` | `opencli geogebra info --name "<name>" -f json`<br>Get detailed properties of a GeoGebra object | `name` (str, required) | auth=optional; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `list` | `private_content_read` / `medium` | `opencli geogebra list [--type "<type>"] -f json`<br>List all geometric objects on the GeoGebra canvas | `type` (str, optional) | auth=optional; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `info`: sensitive output: private content, account identifiers
- `list`: sensitive output: private content, account identifiers
