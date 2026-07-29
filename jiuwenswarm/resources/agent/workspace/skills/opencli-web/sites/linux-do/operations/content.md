---
opencli_contract:
  version: 2
  site: linux-do
  operation: content
  policy_sha256: cc2e02c6a9d1c322af5f087ca9458e5beda0949cc685cd56fa744162f7655b8a
  commands:
    topic:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Topic ID
        name: id
        positional: true
        required: true
        type: int
      - default: 20
        help: Number of posts
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    topic-content:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Topic ID
        name: id
        positional: true
        required: true
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Linux Do: content

Read one public item, record, page, or resource.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `topic` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>linux.do 帖子首页摘要和回复（首屏） | `id` (int, required, positional); `limit` (int, optional, default=20) |
| `topic-content` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Get the main topic body as Markdown | `id` (int, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
