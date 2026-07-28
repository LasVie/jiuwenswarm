---
opencli_contract:
  version: 2
  site: confluence
  operation: publishing
  policy_sha256: 9e165c669a07b0bc222b8320a76389adf0ede9f619479faf88104cd50a896a3e
  commands:
    create:
      executor: none
      execution_state: disabled
      semantic_effect: public_write
      risk: high
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: write
      args:
      - help: Cloud space id, or Data Center space key
        name: space
        required: true
        type: string
      - help: Page title
        name: title
        required: true
        type: string
      - help: Markdown file path
        name: file
        required: true
        type: string
      - help: Optional parent page id
        name: parent
        required: false
        type: string
      - choices:
        - markdown
        - storage
        default: markdown
        help: Input file format
        name: representation
        required: false
        type: string
      - help: Actually create the remote page
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
    update:
      executor: none
      execution_state: disabled
      semantic_effect: public_write
      risk: high
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: write
      args:
      - help: Confluence page id
        name: id
        positional: true
        required: true
        type: str
      - help: Markdown file path
        name: file
        required: true
        type: string
      - help: Optional replacement title; defaults to current title
        name: title
        required: false
        type: string
      - help: Confluence version message
        name: version-message
        required: false
        type: string
      - choices:
        - markdown
        - storage
        default: markdown
        help: Input file format
        name: representation
        required: false
        type: string
      - help: Actually update the remote page
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

# Confluence: publishing

Publish, create, edit, or upload remote content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `create` | `disabled` | `public_write` / `high` | Not executable; use the declared fallback if permitted<br>Create a Confluence page from Markdown or storage XHTML | `space` (string, required); `title` (string, required); `file` (string, required); `parent` (string, optional); `representation` (string, optional, default='markdown', choices=markdown,storage); `execute` (boolean, optional) |
| `update` | `disabled` | `public_write` / `high` | Not executable; use the declared fallback if permitted<br>Update a Confluence page body from Markdown or storage XHTML | `id` (str, required, positional); `file` (string, required); `title` (string, optional); `version-message` (string, optional); `representation` (string, optional, default='markdown', choices=markdown,storage); `execute` (boolean, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
