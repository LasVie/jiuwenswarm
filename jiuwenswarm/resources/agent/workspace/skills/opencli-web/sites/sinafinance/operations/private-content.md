---
opencli_contract:
  version: 2
  site: sinafinance
  operation: private-content
  policy_sha256: 0e2bcbc6a43027fe339f4a99f9f4730abe1b3e354a76c6d4f729599e0ab2a1c3
  commands:
    rolling-news:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    stock-rank:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - choices:
        - cn
        - hk
        - us
        - wh
        - ft
        default: cn
        help: 'Market: cn (A股), hk (港股), us (美股), wh (外汇), ft (期货)'
        name: market
        required: false
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
---

# Sinafinance: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `rolling-news` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>新浪财经滚动新闻 | none |
| `stock-rank` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>新浪财经热搜榜 | `market` (string, optional, default='cn', choices=cn,hk,us,wh,ft) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
