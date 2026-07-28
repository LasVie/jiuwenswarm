---
opencli_contract:
  version: 2
  site: spotify
  operation: authentication
  policy_sha256: 62c64b7e6dc3d752f97becf1a28ab253285c3de4d29a00f68a36cc9e4ed9fbc5
  commands:
    auth:
      executor: none
      execution_state: disabled
      semantic_effect: auth_session_change
      risk: high
      auth: interactive
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: write
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Spotify: authentication

Open, change, or clear an authenticated browser session.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `auth` | `disabled` | `auth_session_change` / `high` | Not executable; use the declared fallback if permitted<br>Authenticate with Spotify (OAuth — run once) | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
