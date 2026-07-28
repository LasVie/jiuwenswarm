---
opencli_contract:
  version: 2
  site: uiverse
  operation: private-content
  policy_sha256: 64665d56f36ee18baec5d7869ae60c4c8216a089936edbca01b39b6e98a61c25
  commands:
    preview:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Uiverse URL or author/slug identifier
        name: input
        positional: true
        required: true
        type: str
      - help: Output image path (defaults to a temp file)
        name: output
        required: false
        type: str
      - default: 8
        help: Extra padding around the captured preview in pixels
        name: padding
        required: false
        type: int
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

# Uiverse: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `preview` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Capture a screenshot of the Uiverse preview element | `input` (str, required, positional); `output` (str, optional); `padding` (int, optional, default=8) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
