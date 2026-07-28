# Xiaohongshu Discovery Operations

This operation contract is selected by the Xiaohongshu site router. It
authorizes only the commands listed below. Keep all parent routing, shell,
confirmation, and fallback rules in force.

| Command | Access | Exact usage | Purpose and important options |
|---|---|---|---|
| `ask` | write | `opencli xiaohongshu ask <query> [--timeout <seconds>] [--source-limit <count>] -f json` | Ask 小红书点点 and return an answer with sources. Defaults: timeout 90, source limit 10. |
| `feed` | read | `opencli xiaohongshu feed [--limit <count>] -f json` | Read the home recommendation feed. Limit defaults to 20. |
| `search` | read | `opencli xiaohongshu search <query> [--limit <count>] -f json` | Search notes. Limit defaults to 20. |

## Run discovery

1. Preserve the user's query as one argument; do not add shell quoting inside
   the value.
2. Use `search` for explicit keywords and `feed` only for the current account's
   recommendation stream.
3. Treat `ask` as a write-class browser interaction. Once it starts, do not
   repeat the request through `browser_agent`.
4. A failed read-only `search` or `feed` may fall back to `browser_agent` when
   no side effect occurred and the parent router otherwise permits fallback.
