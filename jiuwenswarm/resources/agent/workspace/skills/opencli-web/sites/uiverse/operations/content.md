---
opencli_contract:
  version: 2
  site: uiverse
  operation: content
  policy_sha256: faf9cfac5523734f27c4929dd8d62d163f59b218a1fd87ae8830b3d31a1109a1
  commands:
    code:
      executor: browser_manifest_public_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
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
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Uiverse: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `code` | `enabled` | `public_read` / `low` | `opencli_execute(site="uiverse", operation="content", command="code", arguments={"input":"<input>","target":"<target>"})`<br>Export Uiverse component code (HTML, CSS, React, or Vue) | `input` (str, required, positional); `target` (str, required, choices=html,css,react,vue) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
