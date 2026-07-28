---
opencli_contract:
  version: 2
  site: hackernews
  operation: discovery
  policy_sha256: c01b909ca1346a48bab7fdec539efd83fcbf716ed7d303362da917b10b43ac60
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
      - help: Search query
        name: query
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of results
        name: limit
        required: false
        type: int
      - choices:
        - relevance
        - date
        default: relevance
        help: Sort by relevance or date
        name: sort
        required: false
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Hackernews: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="hackernews", operation="discovery", command="search", arguments={"query":"<query>"})`<br>Search Hacker News stories | `query` (str, required, positional); `limit` (int, optional, default=20); `sort` (str, optional, default='relevance', choices=relevance,date) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
