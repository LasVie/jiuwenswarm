---
opencli_contract:
  version: 2
  site: pixiv
  operation: content
  policy_sha256: 91fe6dcb96f651c08d5de587daada322a6f09d8257010b42751cd5ba7768c4bb
  commands:
    detail:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Illustration ID
        name: id
        positional: true
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    user:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Pixiv user ID
        name: uid
        positional: true
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Pixiv: content

Read one public item, record, page, or resource.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `detail` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>View illustration details (tags, stats, URLs) | `id` (str, required, positional) |
| `user` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>View Pixiv artist profile | `uid` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
