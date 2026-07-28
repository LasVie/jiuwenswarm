---
opencli_contract:
  version: 2
  site: dockerhub
  operation: discovery
  policy_sha256: 5419955245424527c58a623654566ed71841248fcc1472478bbd7a01c1370e48
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
      - help: Search keyword (e.g. "nginx", "bitnami redis")
        name: query
        positional: true
        required: true
        type: str
      - default: 25
        help: Max repositories (1-100, single Docker Hub page)
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

# Dockerhub: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="dockerhub", operation="discovery", command="search", arguments={"query":"<query>"})`<br>Search Docker Hub repositories by keyword | `query` (str, required, positional); `limit` (int, optional, default=25) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
