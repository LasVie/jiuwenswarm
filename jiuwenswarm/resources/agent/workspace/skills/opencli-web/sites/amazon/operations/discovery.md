---
opencli_contract:
  version: 2
  site: amazon
  operation: discovery
  policy_sha256: d829909e04280195a5861590061a9e1f4c71232378a0219b70dc6d18da50fe38
  commands:
    bestsellers:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Ranking URL or supported Amazon path. Omit to use the list root.
        name: input
        positional: true
        required: false
        type: str
      - default: 100
        help: Maximum number of ranked items to return (default 100)
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    movers-shakers:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Ranking URL or supported Amazon path. Omit to use the list root.
        name: input
        positional: true
        required: false
        type: str
      - default: 100
        help: Maximum number of ranked items to return (default 100)
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    new-releases:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Ranking URL or supported Amazon path. Omit to use the list root.
        name: input
        positional: true
        required: false
        type: str
      - default: 100
        help: Maximum number of ranked items to return (default 100)
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    search:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Search query, for example "desk shelf organizer"
        name: query
        positional: true
        required: true
        type: str
      - default: 20
        help: Maximum number of results to return (default 20)
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Amazon: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `bestsellers` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Amazon Best Sellers pages for category candidate discovery | `input` (str, optional, positional); `limit` (int, optional, default=100) |
| `movers-shakers` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Amazon Movers & Shakers pages for short-term growth signals | `input` (str, optional, positional); `limit` (int, optional, default=100) |
| `new-releases` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Amazon New Releases pages for early momentum discovery | `input` (str, optional, positional); `limit` (int, optional, default=100) |
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Amazon search results for product discovery and coarse filtering | `query` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
