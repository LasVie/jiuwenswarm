---
opencli_contract:
  version: 2
  site: paperreview
  operation: content
  policy_sha256: 7c57f79b95a57b61fee3048b014fbe427f6b1438c98418b545beeb8d2073d190
  commands:
    review:
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
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Paperreview: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `review` | `enabled` | `public_read` / `low` | `opencli_execute(site="paperreview", operation="content", command="review", arguments={"token":"<token>"})`<br>Fetch a paperreview.ai review by token | `token` (str, required, positional); `timeout` (int, optional, default=30) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
