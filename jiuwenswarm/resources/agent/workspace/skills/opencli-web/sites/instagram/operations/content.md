---
opencli_contract:
  version: 2
  site: instagram
  operation: content
  policy_sha256: 2f23b0dffc95b6eb1f0ec9f5697f887ee9af073f197122b3280c07425989434d
  commands:
    profile:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Instagram username
        name: username
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

# Instagram: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `profile` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Get Instagram user profile info | `username` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
