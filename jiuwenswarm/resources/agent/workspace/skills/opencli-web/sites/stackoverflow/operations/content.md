---
opencli_contract:
  version: 2
  site: stackoverflow
  operation: content
  policy_sha256: 62868097b184f6f856cb90832f1e2a6d341558af5eb77a281e752d2dfa3696a6
  commands:
    bounties:
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
      - default: 10
        help: Max number of results
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
    hot:
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
      - default: 10
        help: Max number of results
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
      - help: Stack Overflow question id (numeric, e.g. 79935770)
        name: id
        positional: true
        required: true
        type: str
      - default: 10
        help: Max answers to include (1-100; accepted answer always included first)
        name: answers-limit
        required: false
        type: int
      - default: 5
        help: Max comments per question/answer (1-100)
        name: comments-limit
        required: false
        type: int
      - default: 4000
        help: Max characters per body / answer / comment (min 100)
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
    related:
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
      - help: Stack Overflow question id (numeric, e.g. 79935770).
        name: id
        positional: true
        required: true
        type: string
      - default: rank
        help: 'Sort key: rank, activity, votes, creation (rank = SO relevance default).'
        name: sort
        required: false
        type: string
      - default: 20
        help: Max related questions (1-100).
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
      - help: Tag slug (e.g. python, rust, typescript).
        name: tag
        positional: true
        required: true
        type: string
      - default: activity
        help: 'Sort key: activity, votes, creation, hot, week, month'
        name: sort
        required: false
        type: string
      - default: 20
        help: Max questions to return (max 100).
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
    unanswered:
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
      - default: 10
        help: Max number of results
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
      - help: Display name (or substring) to search.
        name: name
        positional: true
        required: true
        type: string
      - default: 10
        help: Max users to return (max 100).
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

# Stackoverflow: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `bounties` | `enabled` | `public_read` / `low` | `opencli_execute(site="stackoverflow", operation="content", command="bounties")`<br>Active bounties on Stack Overflow | `limit` (int, optional, default=10) |
| `hot` | `enabled` | `public_read` / `low` | `opencli_execute(site="stackoverflow", operation="content", command="hot")`<br>Hot Stack Overflow questions | `limit` (int, optional, default=10) |
| `read` | `enabled` | `public_read` / `low` | `opencli_execute(site="stackoverflow", operation="content", command="read", arguments={"id":"<id>"})`<br>Read a Stack Overflow question with answers and comments | `id` (str, required, positional); `answers-limit` (int, optional, default=10); `comments-limit` (int, optional, default=5); `max-length` (int, optional, default=4000) |
| `related` | `enabled` | `public_read` / `low` | `opencli_execute(site="stackoverflow", operation="content", command="related", arguments={"id":"<id>"})`<br>List Stack Overflow questions related to a given question id. | `id` (string, required, positional); `sort` (string, optional, default='rank'); `limit` (int, optional, default=20) |
| `tag` | `enabled` | `public_read` / `low` | `opencli_execute(site="stackoverflow", operation="content", command="tag", arguments={"tag":"<tag>"})`<br>List Stack Overflow questions tagged with a given tag (most active first). | `tag` (string, required, positional); `sort` (string, optional, default='activity'); `limit` (int, optional, default=20) |
| `unanswered` | `enabled` | `public_read` / `low` | `opencli_execute(site="stackoverflow", operation="content", command="unanswered")`<br>Top voted unanswered questions on Stack Overflow | `limit` (int, optional, default=10) |
| `user` | `enabled` | `public_read` / `low` | `opencli_execute(site="stackoverflow", operation="content", command="user", arguments={"name":"<name>"})`<br>Find Stack Overflow users by display name (highest reputation first). | `name` (string, required, positional); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
