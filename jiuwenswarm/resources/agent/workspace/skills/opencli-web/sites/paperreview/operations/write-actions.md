---
opencli_contract:
  version: 2
  site: paperreview
  operation: write-actions
  policy_sha256: 7c57f79b95a57b61fee3048b014fbe427f6b1438c98418b545beeb8d2073d190
  commands:
    feedback:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: write
      args:
      - help: Review token returned by paperreview.ai
        name: token
        positional: true
        required: true
        type: str
      - help: Helpfulness score from 1 to 5
        name: helpfulness
        required: true
        type: int
      - choices:
        - 'yes'
        - 'no'
        help: Whether the review contains a critical error
        name: critical-error
        required: true
        type: str
      - choices:
        - 'yes'
        - 'no'
        help: Whether the review contains actionable suggestions
        name: actionable-suggestions
        required: true
        type: str
      - help: Optional free-text feedback
        name: additional-comments
        required: false
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
      sensitive_output: []
---

# Paperreview: write-actions

Change remote service state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `feedback` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Submit feedback for a paperreview.ai review token | `token` (str, required, positional); `helpfulness` (int, required); `critical-error` (str, required, choices=yes,no); `actionable-suggestions` (str, required, choices=yes,no); `additional-comments` (str, optional); `timeout` (int, optional, default=30) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
