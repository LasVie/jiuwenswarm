---
opencli_contract:
  version: 2
  site: jike
  operation: content
  policy_sha256: fe96a20e3b2bc4c2630c74b573ded5477bf007ae268dc0640c96e881b1776651
  commands:
    post:
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
      - help: Post ID (from post URL)
        name: id
        positional: true
        required: true
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
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
      - help: Topic ID (from topic URL, e.g. 553870e8e4b0cafb0a1bef68)
        name: id
        positional: true
        required: true
        type: string
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
    user:
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
      - help: Username from profile URL (e.g. wenhao1996)
        name: username
        positional: true
        required: true
        type: string
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
---

# Jike: content

Read one public item, record, page, or resource.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `post` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>即刻帖子详情及评论 | `id` (string, required, positional) |
| `topic` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>即刻话题/圈子帖子 | `id` (string, required, positional); `limit` (int, optional, default=20) |
| `user` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>即刻用户动态 | `username` (string, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
