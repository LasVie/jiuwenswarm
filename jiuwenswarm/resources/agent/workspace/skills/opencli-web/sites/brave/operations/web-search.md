---
opencli_contract:
  version: 2
  site: brave
  operation: web-search
  policy_sha256: dc8da22970a9969060ff750bd07b24cdef2949510bd52027cf8cb8f29adf69f3
  commands:
    search:
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
      - help: Search query
        name: keyword
        positional: true
        required: true
        type: str
      - default: 10
        help: Number of results per page (max 18)
        name: limit
        required: false
        type: int
      - default: 0
        help: Page offset (0, 1, 2...). Brave returns ~18 results per page
        name: offset
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

# Brave: web-search

Read browser-rendered web search results.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="brave", operation="web-search", command="search", arguments={"keyword":"<keyword>"})`<br>Search Brave Search | `keyword` (str, required, positional); `limit` (int, optional, default=10); `offset` (int, optional, default=0) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
