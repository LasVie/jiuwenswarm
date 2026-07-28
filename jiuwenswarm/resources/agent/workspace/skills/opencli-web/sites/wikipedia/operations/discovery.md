---
opencli_contract:
  version: 2
  site: wikipedia
  operation: discovery
  policy_sha256: 230e0d7012b645670f11323ce167ae5cb4746e97d5dcc90cde4a2fd4a9d6e798
  commands:
    random:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: en
        help: Language code (e.g. en, zh, ja)
        name: lang
        required: false
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    search:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: Search keyword
        name: query
        positional: true
        required: true
        type: str
      - default: 10
        help: Max results
        name: limit
        required: false
        type: int
        constraints:
          minimum: 1
          maximum: 50
      - default: en
        help: Language code (e.g. en, zh, ja)
        name: lang
        required: false
        type: str
        constraints:
          pattern: ^[a-z]{2,3}(?:-[a-z0-9]+)?$
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    trending:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: 10
        help: Max results
        name: limit
        required: false
        type: int
        constraints:
          minimum: 1
          maximum: 50
      - default: en
        help: Language code (e.g. en, zh, ja)
        name: lang
        required: false
        type: str
        constraints:
          pattern: ^[a-z]{2,3}(?:-[a-z0-9]+)?$
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Wikipedia: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `random` | `enabled` | `public_read` / `low` | `opencli_execute(site="wikipedia", operation="discovery", command="random")`<br>Get a random Wikipedia article | `lang` (str, optional, default='en') |
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="wikipedia", operation="discovery", command="search", arguments={"query":"<query>"})`<br>Search Wikipedia articles | `query` (str, required, positional); `limit` (int, optional, default=10, minimum=1,maximum=50); `lang` (str, optional, default='en', pattern=^[a-z]{2,3}(?:-[a-z0-9]+)?$) |
| `trending` | `enabled` | `public_read` / `low` | `opencli_execute(site="wikipedia", operation="discovery", command="trending")`<br>Most-read Wikipedia articles (yesterday) | `limit` (int, optional, default=10, minimum=1,maximum=50); `lang` (str, optional, default='en', pattern=^[a-z]{2,3}(?:-[a-z0-9]+)?$) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
