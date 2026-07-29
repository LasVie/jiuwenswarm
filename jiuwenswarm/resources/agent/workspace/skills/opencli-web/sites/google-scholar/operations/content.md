---
opencli_contract:
  version: 2
  site: google-scholar
  operation: content
  policy_sha256: e8a375447fb508103975cdf63b6461e573ec004e31f53863c0d904d434d51cd3
  commands:
    cite:
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
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    profile:
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
      - help: Author name or Scholar user ID (e.g. JicYPdAAAAAJ)
        name: author
        positional: true
        required: true
        type: str
      - default: 10
        help: Max papers to show (max 20)
        name: limit
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

# Google Scholar: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `cite` | `enabled` | `public_read` / `low` | `opencli_execute(site="google-scholar", operation="content", command="cite", arguments={"query":"<query>"})`<br>Get citation for a Google Scholar paper | `query` (str, required, positional); `style` (str, optional, default='bibtex', choices=bibtex,endnote,refman,refworks); `index` (int, optional, default=1) |
| `profile` | `enabled` | `public_read` / `low` | `opencli_execute(site="google-scholar", operation="content", command="profile", arguments={"author":"<author>"})`<br>View a Google Scholar author profile | `author` (str, required, positional); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
