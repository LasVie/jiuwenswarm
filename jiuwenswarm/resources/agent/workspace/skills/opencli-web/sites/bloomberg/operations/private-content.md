---
opencli_contract:
  version: 2
  site: bloomberg
  operation: private-content
  policy_sha256: fc11a4e4f3dba4820f8bc9aa003f0fa2e715721959938e3cfb3f97b8b6cab036
  commands:
    news:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: optional
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Bloomberg story/article URL or relative Bloomberg path
        name: link
        positional: true
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - subscription-gated content
---

# Bloomberg: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `news` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read a Bloomberg story/article page and return title, full content, and media links | `link` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
