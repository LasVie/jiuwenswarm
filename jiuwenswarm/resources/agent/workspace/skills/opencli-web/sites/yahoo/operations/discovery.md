---
opencli_contract:
  version: 2
  site: yahoo
  operation: discovery
  policy_sha256: 4414eace8982bdba7e36eccd11494af3847990249a9a964d225d9073e6c64eaa
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
      - default: 7
        help: Number of results per page (max 7)
        name: limit
        required: false
        type: int
      - default: 1
        help: Page number (1, 2, 3...). Yahoo returns ~7 results per page
        name: page
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

# Yahoo: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="yahoo", operation="discovery", command="search", arguments={"keyword":"<keyword>"})`<br>Search Yahoo (powered by Bing) | `keyword` (str, required, positional); `limit` (int, optional, default=7); `page` (int, optional, default=1) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
