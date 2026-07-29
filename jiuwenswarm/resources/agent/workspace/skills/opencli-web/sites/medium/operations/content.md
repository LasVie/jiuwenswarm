---
opencli_contract:
  version: 2
  site: medium
  operation: content
  policy_sha256: ff72b54447fdc746fd7f4109325a2872a87cf9bfb1771abc1d0fd1e769ad7642
  commands:
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
      - help: Lowercase tag slug (e.g. "programming", "machine-learning")
        name: tag
        positional: true
        required: true
        type: str
      - default: 20
        help: Max articles (1-25 — single RSS page)
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
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Medium 用户名（如 @username 或 username）
        name: username
        positional: true
        required: true
        type: str
      - default: 20
        help: 返回的文章数量
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Medium: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `tag` | `enabled` | `public_read` / `low` | `opencli_execute(site="medium", operation="content", command="tag", arguments={"tag":"<tag>"})`<br>Latest Medium articles tagged with a given keyword (RSS feed) | `tag` (str, required, positional); `limit` (int, optional, default=20) |
| `user` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>获取 Medium 用户的文章列表 | `username` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
