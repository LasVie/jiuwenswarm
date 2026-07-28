---
opencli_contract:
  version: 2
  site: duckduckgo
  operation: discovery
  policy_sha256: e092074b61e3024749ae3133a3ef3784467d0eb1d8a2a2369e5592aa83597645
  commands:
    suggest:
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
      - help: Search query prefix
        name: keyword
        positional: true
        required: true
        type: str
      - default: 8
        help: Max number of suggestions
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
---

# Duckduckgo: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `suggest` | `enabled` | `public_read` / `low` | `opencli_execute(site="duckduckgo", operation="discovery", command="suggest", arguments={"keyword":"<keyword>"})`<br>DuckDuckGo search suggestions | `keyword` (str, required, positional); `limit` (int, optional, default=8) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
