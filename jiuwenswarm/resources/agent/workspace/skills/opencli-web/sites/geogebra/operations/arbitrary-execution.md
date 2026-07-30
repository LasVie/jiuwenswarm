# Geogebra: arbitrary-execution

Adapter entry points that can execute arbitrary input.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `eval` | `arbitrary_execution` / `critical` | `opencli geogebra eval "<command>" -f json`<br>Execute one or more GeoGebra command strings (semicolon-separated) | `command` (str, required, positional) | auth=required; transport=browser_dom; fallback_before=none; fallback_after=none |
