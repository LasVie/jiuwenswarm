---
opencli_contract:
  version: 2
  site: jira
  operation: content
  policy_sha256: 653e752fd0a366bfa17ccb2e5f875ea9bc0d6959e7cae877fcd365eff4fe36da
  commands:
    attachments:
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
      - help: Jira issue key, e.g. PROJ-123
        name: key
        positional: true
        required: true
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    comments:
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
      - help: Jira issue key, e.g. PROJ-123
        name: key
        positional: true
        required: true
        type: str
      - default: 50
        help: Max comments to return (1-100)
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
    issue:
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
      - help: Jira issue key, e.g. PROJ-123
        name: key
        positional: true
        required: true
        type: str
      - default: 100
        help: Max comments to include (1-100)
        name: comments-limit
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    links:
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
      - help: Jira issue key, e.g. PROJ-123
        name: key
        positional: true
        required: true
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Jira: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `attachments` | `enabled` | `public_read` / `low` | `opencli_execute(site="jira", operation="content", command="attachments", arguments={"key":"<key>"})`<br>Jira issue attachment metadata | `key` (str, required, positional) |
| `comments` | `enabled` | `public_read` / `low` | `opencli_execute(site="jira", operation="content", command="comments", arguments={"key":"<key>"})`<br>Jira issue comments as Markdown | `key` (str, required, positional); `limit` (int, optional, default=50) |
| `issue` | `enabled` | `public_read` / `low` | `opencli_execute(site="jira", operation="content", command="issue", arguments={"key":"<key>"})`<br>Jira issue detail normalized for agents (description, comments, attachments, links) | `key` (str, required, positional); `comments-limit` (int, optional, default=100) |
| `links` | `enabled` | `public_read` / `low` | `opencli_execute(site="jira", operation="content", command="links", arguments={"key":"<key>"})`<br>Jira issue links | `key` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
