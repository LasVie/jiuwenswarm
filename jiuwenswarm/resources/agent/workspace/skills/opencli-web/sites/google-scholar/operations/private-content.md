---
opencli_contract:
  version: 2
  site: google-scholar
  operation: private-content
  policy_sha256: 0c3b32f56160b203c146f3a1e745b728787ba38836170eb583d9584a5d8e5d93
  commands:
    cite:
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
      - help: Paper title to search for
        name: query
        positional: true
        required: true
        type: str
      - choices:
        - bibtex
        - endnote
        - refman
        - refworks
        default: bibtex
        help: Citation format
        name: style
        required: false
        type: str
      - default: 1
        help: Which search result to cite (1-based)
        name: index
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
    search:
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
      - help: 搜索关键词
        name: query
        positional: true
        required: true
        type: str
      - default: 10
        help: 返回结果数量 (max 20)
        name: limit
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

# Google Scholar: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `cite` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get citation for a Google Scholar paper | `query` (str, required, positional); `style` (str, optional, default='bibtex', choices=bibtex,endnote,refman,refworks); `index` (int, optional, default=1) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Google Scholar 学术搜索 | `query` (str, required, positional); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
