---
opencli_contract:
  version: 2
  site: tieba
  operation: discovery
  policy_sha256: 239c0f008bb350c840d9f8f253b634481a32f077945d1bd31e7d601e734cc952
  commands:
    hot:
      executor: browser_manifest_public_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: Number of items to return
        name: limit
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    posts:
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
      - help: Forum name in Chinese
        name: forum
        positional: true
        required: true
        type: string
      - default: 1
        help: Page number
        name: page
        required: false
        type: int
      - default: 20
        help: Number of items to return
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
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
        name: keyword
        positional: true
        required: true
        type: string
      - choices:
        - '1'
        default: 1
        help: Page number (currently only 1 is supported)
        name: page
        required: false
        type: int
      - default: 20
        help: Number of items to return
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Tieba: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `hot` | `enabled` | `public_read` / `low` | `opencli_execute(site="tieba", operation="discovery", command="hot")`<br>Tieba hot topics | `limit` (int, optional, default=20) |
| `posts` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Browse posts in a tieba forum | `forum` (string, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=20) |
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Search posts across tieba | `keyword` (string, required, positional); `page` (int, optional, default=1, choices=1); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
