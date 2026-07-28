---
opencli_contract:
  version: 2
  site: spotify
  operation: account
  policy_sha256: a79d0b04af7de90a372da7a714ea9f00e6d21d6dac4df21fe39708f531fe47ac
  commands:
    status:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
      risk: medium
      auth: required
      transport: mixed
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs:
      - ~/.opencli/spotify.env
      - ~/.opencli/spotify-tokens.json
      file_outputs:
      - ~/.opencli/spotify-tokens.json
      sensitive_output:
      - private playback state
      - account identifiers
      - OAuth access and refresh tokens
---

# Spotify: account

Read account-scoped playback state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `status` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>Show current playback status | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
