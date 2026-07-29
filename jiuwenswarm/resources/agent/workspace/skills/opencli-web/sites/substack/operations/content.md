---
opencli_contract:
  version: 2
  site: substack
  operation: content
  policy_sha256: df8ef4f8daaf608fb76501375020aa60d8556a54b751921df910bcbdd175773f
  commands:
    publication:
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
      - help: Newsletter URL（如 https://example.substack.com）
        name: url
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

# Substack: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `publication` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>获取特定 Substack Newsletter 的最新文章 | `url` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
