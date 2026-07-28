---
opencli_contract:
  version: 2
  site: spotify
  operation: write-actions
  policy_sha256: a79d0b04af7de90a372da7a714ea9f00e6d21d6dac4df21fe39708f531fe47ac
  commands:
    next:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: none
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
    pause:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: none
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
    play:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: write
      args:
      - default: ''
        help: Track or artist to play (optional)
        name: query
        positional: true
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    prev:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: none
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
    queue:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: write
      args:
      - help: Track to add to queue
        name: query
        positional: true
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    repeat:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: write
      args:
      - choices:
        - 'off'
        - track
        - context
        default: context
        help: off / track / context
        name: mode
        positional: true
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    shuffle:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: write
      args:
      - choices:
        - 'on'
        - 'off'
        default: 'on'
        help: on or off
        name: state
        positional: true
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    volume:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: write
      args:
      - default: 50
        help: Volume 0–100
        name: level
        positional: true
        required: true
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Spotify: write-actions

Change remote service state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `next` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Skip to next track | none |
| `pause` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Pause playback | none |
| `play` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Resume playback or search and play a track/artist | `query` (str, optional, positional, default='') |
| `prev` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Skip to previous track | none |
| `queue` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Add a track to the playback queue | `query` (str, required, positional) |
| `repeat` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Set repeat mode (off / track / context) | `mode` (str, optional, positional, default='context', choices=off,track,context) |
| `shuffle` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Toggle shuffle on/off | `state` (str, optional, positional, default='on', choices=on,off) |
| `volume` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Set playback volume (0-100) | `level` (int, required, positional, default=50) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
