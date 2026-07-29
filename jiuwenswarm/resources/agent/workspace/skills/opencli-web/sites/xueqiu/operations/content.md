---
opencli_contract:
  version: 2
  site: xueqiu
  operation: content
  policy_sha256: 7a5406525e083d7bfa2e25b732b8df0543bc33834f5e0471e504ceebe08e0303
  commands:
    comments:
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
      - help: Stock symbol, e.g. SH600519, AAPL, or 00700
        name: symbol
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of discussion posts to return
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

# Xueqiu: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `comments` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>获取单只股票的讨论动态 | `symbol` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
