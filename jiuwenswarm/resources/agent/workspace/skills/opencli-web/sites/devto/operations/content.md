---
opencli_contract:
  version: 2
  site: devto
  operation: content
  policy_sha256: ed727f40f9cfdf35572dcd0e1d918072a1c4d040ffd8c59c2edc23928ae0c580
  commands:
    latest:
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
      - default: 20
        help: Articles per page (1-100)
        name: limit
        required: false
        type: int
      - default: 1
        help: Page number (1-based)
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
    read:
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
      - help: DEV.to article id (numeric, e.g. 3605688)
        name: id
        positional: true
        required: true
        type: str
      - default: 20000
        help: Max characters of body to return (min 100)
        name: max-length
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    tag:
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
      - help: Tag name (e.g. javascript, python, webdev)
        name: tag
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of articles
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
    top:
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
      - default: 20
        help: Number of articles
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
    user:
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
      - help: DEV.to username (e.g. ben, thepracticaldev)
        name: username
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of articles
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

# Devto: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `latest` | `enabled` | `public_read` / `low` | `opencli_execute(site="devto", operation="content", command="latest")`<br>Newest dev.to articles (firehose, all tags) | `limit` (int, optional, default=20); `page` (int, optional, default=1) |
| `read` | `enabled` | `public_read` / `low` | `opencli_execute(site="devto", operation="content", command="read", arguments={"id":"<id>"})`<br>Read a DEV.to article body by id | `id` (str, required, positional); `max-length` (int, optional, default=20000) |
| `tag` | `enabled` | `public_read` / `low` | `opencli_execute(site="devto", operation="content", command="tag", arguments={"tag":"<tag>"})`<br>Latest DEV.to articles for a specific tag | `tag` (str, required, positional); `limit` (int, optional, default=20) |
| `top` | `enabled` | `public_read` / `low` | `opencli_execute(site="devto", operation="content", command="top")`<br>Top DEV.to articles of the day | `limit` (int, optional, default=20) |
| `user` | `enabled` | `public_read` / `low` | `opencli_execute(site="devto", operation="content", command="user", arguments={"username":"<username>"})`<br>Recent DEV.to articles from a specific user | `username` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
