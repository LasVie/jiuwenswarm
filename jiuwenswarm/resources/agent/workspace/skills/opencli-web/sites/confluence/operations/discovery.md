---
opencli_contract:
  version: 2
  site: confluence
  operation: discovery
  policy_sha256: 9e165c669a07b0bc222b8320a76389adf0ede9f619479faf88104cd50a896a3e
  commands:
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
      - help: CQL query, e.g. "type = page and title ~ \"RCA\""
        name: cql
        positional: true
        required: true
        type: str
      - help: Limit search to a Confluence space key
        name: space
        required: false
        type: string
      - default: 20
        help: Max results to return (1-100)
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

# Confluence: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="confluence", operation="discovery", command="search", arguments={"cql":"<cql>"})`<br>Search Confluence content with CQL | `cql` (str, required, positional); `space` (string, optional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
