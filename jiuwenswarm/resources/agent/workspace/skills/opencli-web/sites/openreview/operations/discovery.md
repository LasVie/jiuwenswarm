---
opencli_contract:
  version: 2
  site: openreview
  operation: discovery
  policy_sha256: 096b115ccc93e419a9ef5dc5776b3179c3bbaceb07a04d5e78ab0bb9aee19b59
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
      - help: Search keyword (e.g. "diffusion model")
        name: query
        positional: true
        required: true
        type: str
      - default: 25
        help: Max results (max 50)
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

# Openreview: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="openreview", operation="discovery", command="search", arguments={"query":"<query>"})`<br>Search OpenReview papers by free-text query | `query` (str, required, positional); `limit` (int, optional, default=25) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
