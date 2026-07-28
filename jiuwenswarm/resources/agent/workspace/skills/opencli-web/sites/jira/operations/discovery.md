---
opencli_contract:
  version: 2
  site: jira
  operation: discovery
  policy_sha256: 691c2064bdb38815255e941dfddf957d1c0d04cf322401252a6f17285f78d7f1
  commands:
    search:
      executor: none
      execution_state: quarantined
      semantic_effect: private_content_read
      risk: high
      auth: required
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: JQL query, e.g. "project = PROJ order by updated desc"
        name: jql
        positional: true
        required: true
        type: str
      - default: 20
        help: Max issues to return (1-100)
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: none
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private issue content
      - account identifiers
---

# Jira: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `quarantined` | `private_content_read` / `high` | Not executable; use the declared fallback if permitted<br>Search Jira issues with JQL | `jql` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
