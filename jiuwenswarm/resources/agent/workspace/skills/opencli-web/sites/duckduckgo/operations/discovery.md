---
opencli_contract:
  version: 2
  site: duckduckgo
  operation: discovery
  policy_sha256: 1333c2fd8f205145a3f0cabfeb7a5310fae4cf93a52b95efd9e46ef5ff39ccd5
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
        help: Number of results per page (1-10). For multi-page, use --offset
        name: limit
        required: false
        type: int
      - default: 0
        help: Result offset for pagination (0, 10, 20...). Uses XHR POST internally
        name: offset
        required: false
        type: int
      - help: 'Region code (e.g. jp-jp, us-en, cn-zh). Default: all regions'
        name: region
        required: false
        type: str
      - help: 'Time range: d (day), w (week), m (month), y (year)'
        name: time
        required: false
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
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
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="duckduckgo", operation="discovery", command="search", arguments={"keyword":"<keyword>"})`<br>Search DuckDuckGo | `keyword` (str, required, positional); `limit` (int, optional, default=10); `offset` (int, optional, default=0); `region` (str, optional); `time` (str, optional) |
| `suggest` | `enabled` | `public_read` / `low` | `opencli_execute(site="duckduckgo", operation="discovery", command="suggest", arguments={"keyword":"<keyword>"})`<br>DuckDuckGo search suggestions | `keyword` (str, required, positional); `limit` (int, optional, default=8) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
