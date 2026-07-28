---
opencli_contract:
  version: 2
  site: xiaoyuzhou
  operation: private-content
  policy_sha256: 567210bd1cc385a31a214f648eb1031d2bebfc3dbb97188fd7b51f02ca930fc9
  commands:
    episode:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: local
      strategy: local
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: Episode ID (eid from podcast-episodes output)
        name: id
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
    podcast:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: local
      strategy: local
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: Podcast ID (from xiaoyuzhoufm.com URL)
        name: id
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
    podcast-episodes:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: local
      strategy: local
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: Podcast ID (from xiaoyuzhoufm.com URL)
        name: id
        positional: true
        required: true
        type: str
      - default: 20
        help: Max episodes to show
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

# Xiaoyuzhou: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `episode` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>View details of a Xiaoyuzhou podcast episode | `id` (str, required, positional) |
| `podcast` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>View a Xiaoyuzhou podcast profile | `id` (str, required, positional) |
| `podcast-episodes` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List episodes of a Xiaoyuzhou podcast | `id` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
