---
opencli_contract:
  version: 2
  site: notebooklm
  operation: publishing
  policy_sha256: b4afc9adf21e631af063d145e7d0a37363571ed629959fd0ea9de242d6e1a9ed
  commands:
    create:
      executor: none
      execution_state: disabled
      semantic_effect: public_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Notebook title (1-200 chars)
        name: title
        positional: true
        required: true
        type: str
      - help: Notebook emoji icon (default 📒)
        name: emoji
        required: false
        type: str
      - help: Actually create the remote NotebookLM notebook
        name: execute
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs:
      - workspace-relative input when declared by adapter
      file_outputs: []
      sensitive_output: []
---

# Notebooklm: publishing

Publish, create, edit, or upload remote content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `create` | `disabled` | `public_write` / `high` | Not executable; use the declared fallback if permitted<br>Create a new NotebookLM notebook with the given title | `title` (str, required, positional); `emoji` (str, optional); `execute` (boolean, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
