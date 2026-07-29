---
opencli_contract:
  version: 2
  site: coupang
  operation: discovery
  policy_sha256: 15c9c239b0ba09eff87a1bba06361a2c5302d3e26fe8bbdf0afc9cea0984cb15
  commands:
    search:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Search keyword
        name: query
        positional: true
        required: true
        type: str
      - default: 1
        help: Search result page number
        name: page
        required: false
        type: int
      - default: 20
        help: Max results (max 50)
        name: limit
        required: false
        type: int
      - help: 'Optional search filter (currently supports: rocket)'
        name: filter
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Coupang: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Search Coupang products with logged-in browser session | `query` (str, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=20); `filter` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
