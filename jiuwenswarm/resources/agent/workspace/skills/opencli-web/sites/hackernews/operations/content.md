---
opencli_contract:
  version: 2
  site: hackernews
  operation: content
  policy_sha256: c01b909ca1346a48bab7fdec539efd83fcbf716ed7d303362da917b10b43ac60
  commands:
    best:
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
        help: Number of stories
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
    jobs:
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
        help: Number of job postings
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
      - help: HN item ID (e.g. 39847301)
        name: id
        positional: true
        required: true
        type: str
      - default: 25
        help: Max top-level comments
        name: limit
        required: false
        type: int
      - default: 2
        help: Max reply depth (1=no replies, 2=one level of replies, etc.)
        name: depth
        required: false
        type: int
      - default: 5
        help: Max replies shown per comment at each level
        name: replies
        required: false
        type: int
      - default: 2000
        help: Max characters per comment body (min 100)
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
    show:
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
        help: Number of stories
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
        help: Number of stories
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
      - help: HN username
        name: username
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

# Hackernews: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `best` | `enabled` | `public_read` / `low` | `opencli_execute(site="hackernews", operation="content", command="best")`<br>Hacker News best stories | `limit` (int, optional, default=20) |
| `jobs` | `enabled` | `public_read` / `low` | `opencli_execute(site="hackernews", operation="content", command="jobs")`<br>Hacker News job postings | `limit` (int, optional, default=20) |
| `read` | `enabled` | `public_read` / `low` | `opencli_execute(site="hackernews", operation="content", command="read", arguments={"id":"<id>"})`<br>Read a Hacker News story and its comment tree | `id` (str, required, positional); `limit` (int, optional, default=25); `depth` (int, optional, default=2); `replies` (int, optional, default=5); `max-length` (int, optional, default=2000) |
| `show` | `enabled` | `public_read` / `low` | `opencli_execute(site="hackernews", operation="content", command="show")`<br>Hacker News Show HN posts | `limit` (int, optional, default=20) |
| `top` | `enabled` | `public_read` / `low` | `opencli_execute(site="hackernews", operation="content", command="top")`<br>Hacker News top stories | `limit` (int, optional, default=20) |
| `user` | `enabled` | `public_read` / `low` | `opencli_execute(site="hackernews", operation="content", command="user", arguments={"username":"<username>"})`<br>Hacker News user profile | `username` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
