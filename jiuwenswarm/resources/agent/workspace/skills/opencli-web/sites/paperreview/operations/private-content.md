---
opencli_contract:
  version: 2
  site: paperreview
  operation: private-content
  policy_sha256: e2340c7ea5cda0685bb79c2758686d307f57d91bfba9107e5d7932617265f589
  commands:
    review:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: high
      auth: required
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: Review token returned by paperreview.ai
        name: token
        positional: true
        required: true
        type: str
      - default: 30
        help: 'Max seconds for the overall command (default: 30)'
        name: timeout
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - review token
      - private review content
---

# Paperreview: private-content

Read private review content addressed by a bearer capability token.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `review` | `disabled` | `private_content_read` / `high` | Not executable; use the declared fallback if permitted<br>Fetch a paperreview.ai review by token | `token` (str, required, positional); `timeout` (int, optional, default=30) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
