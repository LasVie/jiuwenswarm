---
opencli_contract:
  version: 2
  site: v2ex
  operation: content
  policy_sha256: 9a23459a44630f9fce56ffd4d0038ea59b8848415e78acbc97c07f8114c6c816
  commands:
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
      - default: 20
        help: Number of topics
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
        help: Number of topics
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
    member:
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
      - help: Username
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
    node:
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
      - help: Node name (e.g. python, javascript, apple)
        name: name
        positional: true
        required: true
        type: str
      - default: 10
        help: Number of topics (API returns max 20)
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
    nodes:
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
      - default: 30
        help: Number of nodes
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
    replies:
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
      - help: Topic ID
        name: id
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of replies
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
    topic:
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
      - help: Topic ID
        name: id
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
      - help: Username
        name: username
        positional: true
        required: true
        type: str
      - default: 10
        help: Number of topics (API returns max 20)
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

# V2Ex: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `hot` | `enabled` | `public_read` / `low` | `opencli_execute(site="v2ex", operation="content", command="hot")`<br>V2EX 热门话题 | `limit` (int, optional, default=20) |
| `latest` | `enabled` | `public_read` / `low` | `opencli_execute(site="v2ex", operation="content", command="latest")`<br>V2EX 最新话题 | `limit` (int, optional, default=20) |
| `member` | `enabled` | `public_read` / `low` | `opencli_execute(site="v2ex", operation="content", command="member", arguments={"username":"<username>"})`<br>V2EX 用户资料 | `username` (str, required, positional) |
| `node` | `enabled` | `public_read` / `low` | `opencli_execute(site="v2ex", operation="content", command="node", arguments={"name":"<name>"})`<br>V2EX 节点话题列表 | `name` (str, required, positional); `limit` (int, optional, default=10) |
| `nodes` | `enabled` | `public_read` / `low` | `opencli_execute(site="v2ex", operation="content", command="nodes")`<br>V2EX 所有节点列表 | `limit` (int, optional, default=30) |
| `replies` | `enabled` | `public_read` / `low` | `opencli_execute(site="v2ex", operation="content", command="replies", arguments={"id":"<id>"})`<br>V2EX 主题回复列表 | `id` (str, required, positional); `limit` (int, optional, default=20) |
| `topic` | `enabled` | `public_read` / `low` | `opencli_execute(site="v2ex", operation="content", command="topic", arguments={"id":"<id>"})`<br>V2EX 主题详情和回复 | `id` (str, required, positional) |
| `user` | `enabled` | `public_read` / `low` | `opencli_execute(site="v2ex", operation="content", command="user", arguments={"username":"<username>"})`<br>V2EX 用户发帖列表 | `username` (str, required, positional); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
