---
opencli_contract:
  version: 2
  site: notebooklm
  operation: write-actions
  policy_sha256: b4afc9adf21e631af063d145e7d0a37363571ed629959fd0ea9de242d6e1a9ed
  commands:
    add-source:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
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
      - help: Source URL to add (http/https). Pass exactly one of --url, --content, --file.
        name: url
        required: false
        type: str
      - help: Raw text content to add as a Text source (max 10 MB).
        name: content
        required: false
        type: str
      - help: Local file path to upload as a source (max 52428800 bytes; pdf / txt / md / html / docx / etc.). Uses Google Drive's 3-step resumable upload protocol.
        name: file
        required: false
        type: str
      - help: Title for the text source (default "Text Source"). Ignored for --url and --file.
        name: title
        required: false
        type: str
      - help: Override the auto-detected MIME type when --file is given.
        name: mime-type
        required: false
        type: str
      - help: Actually add the remote source to the NotebookLM notebook
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
    write-note:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
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
      - help: Note title (1-200 chars)
        name: title
        required: true
        type: str
      - help: Note body as Markdown
        name: content
        required: true
        type: str
      - help: Actually create the remote NotebookLM note
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

# Notebooklm: write-actions

Change remote service state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `add-source` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Add a URL, text, or local file source to an existing NotebookLM notebook | `notebook` (str, required, positional); `url` (str, optional); `content` (str, optional); `file` (str, optional); `title` (str, optional); `mime-type` (str, optional); `execute` (boolean, optional) |
| `write-note` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Create a Studio note in an existing NotebookLM notebook with the given title and Markdown content | `notebook` (str, required, positional); `title` (str, required); `content` (str, required); `execute` (boolean, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
