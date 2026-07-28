---
opencli_contract:
  version: 2
  site: notebooklm
  operation: private-content
  policy_sha256: b4afc9adf21e631af063d145e7d0a37363571ed629959fd0ea9de242d6e1a9ed
  commands:
    current:
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
    get:
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
    history:
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
    list:
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
    note-list:
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
    notes-get:
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
      - help: Note title or id from the current notebook
        name: note
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
      - private content
      - account identifiers
    open:
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
      - help: Notebook id from list output, or a full NotebookLM notebook URL
        name: notebook
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
      - private content
      - account identifiers
    source-fulltext:
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
      - help: Source id or title from the current notebook
        name: source
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
      - private content
      - account identifiers
    source-get:
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
      - help: Source id or title from the current notebook
        name: source
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
      - private content
      - account identifiers
    source-guide:
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
      - help: Source id or title from the current notebook
        name: source
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
      - private content
      - account identifiers
    source-list:
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
    status:
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
    summary:
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
---

# Notebooklm: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `current` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Show metadata for the currently opened NotebookLM notebook tab | none |
| `get` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get rich metadata for the currently opened NotebookLM notebook | none |
| `history` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List NotebookLM conversation history threads in the current notebook | none |
| `list` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List NotebookLM notebooks via in-page batchexecute RPC in the current logged-in session | none |
| `note-list` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List saved notes from the Studio panel of the current NotebookLM notebook | none |
| `notes-get` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get one note from the current NotebookLM notebook by title from the visible note editor | `note` (str, required, positional) |
| `open` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Open one NotebookLM notebook in the adapter session by id or URL | `notebook` (str, required, positional) |
| `source-fulltext` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get the extracted fulltext for one source in the currently opened NotebookLM notebook | `source` (str, required, positional) |
| `source-get` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get one source from the currently opened NotebookLM notebook by id or title | `source` (str, required, positional) |
| `source-guide` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get the guide summary and keywords for one source in the currently opened NotebookLM notebook | `source` (str, required, positional) |
| `source-list` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List sources for the currently opened NotebookLM notebook | none |
| `status` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Check NotebookLM page availability and login state in the current Chrome session | none |
| `summary` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get the summary block from the currently opened NotebookLM notebook | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
