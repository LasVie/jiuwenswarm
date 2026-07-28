---
opencli_contract:
  version: 2
  site: uiverse
  operation: arbitrary-execution
  policy_sha256: 64665d56f36ee18baec5d7869ae60c4c8216a089936edbca01b39b6e98a61c25
  commands:
    code:
      executor: none
      execution_state: quarantined
      semantic_effect: arbitrary_execution
      risk: critical
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
      - choices:
        - html
        - css
        - react
        - vue
        help: Code target to export
        name: target
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: none
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Uiverse: arbitrary-execution

Adapter entry points that can execute arbitrary input.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `code` | `quarantined` | `arbitrary_execution` / `critical` | Not executable; use the declared fallback if permitted<br>Export Uiverse component code (HTML, CSS, React, or Vue) | `input` (str, required, positional); `target` (str, required, choices=html,css,react,vue) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
