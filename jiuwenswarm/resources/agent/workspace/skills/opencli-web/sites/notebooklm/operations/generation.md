---
opencli_contract:
  version: 2
  site: notebooklm
  operation: generation
  policy_sha256: 73118f579f348316fdaf2092854ccfbd0ca1ac412e2b5f051b5b6fd4d32ef0c8
  commands:
    generate-audio:
      executor: none
      execution_state: disabled
      semantic_effect: quota_consumption
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Notebook id from `notebooklm list` or full notebook URL
        name: notebook
        positional: true
        required: true
        type: str
      - help: Actually trigger remote NotebookLM audio generation
        name: execute
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    generate-slides:
      executor: none
      execution_state: disabled
      semantic_effect: quota_consumption
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Notebook id from `notebooklm list` or full notebook URL
        name: notebook
        positional: true
        required: true
        type: str
      - help: 'Slide deck length: 1=Short, 3=Default (default 3)'
        name: length
        required: false
        type: str
      - help: Language code (default en)
        name: language
        required: false
        type: str
      - help: Actually trigger remote NotebookLM slide deck generation
        name: execute
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Notebooklm: generation

Generate remote content, start AI work, or consume quota.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `generate-audio` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Trigger an Audio Overview (Deep Dive podcast) generation for a NotebookLM notebook, using all of its sources | `notebook` (str, required, positional); `execute` (boolean, optional) |
| `generate-slides` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Trigger a Slide Deck (AI presentation) generation for a NotebookLM notebook, using all of its sources | `notebook` (str, required, positional); `length` (str, optional); `language` (str, optional); `execute` (boolean, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
