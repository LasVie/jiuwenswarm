---
opencli_contract:
  version: 2
  site: slock
  operation: account-actions
  policy_sha256: e8c51aafc73ef81acbe9f554ecba65c0f2eca0cb9bc6baf4d412633ca655d97e
  commands:
    bookmark-add:
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
      - help: Full messageId UUID (short ids rejected)
        name: messageId
        positional: true
        required: true
        type: str
      - help: Override active server
        name: server
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    thread-follow:
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
      - help: Full parent messageId UUID (short ids rejected)
        name: parentMessageId
        positional: true
        required: true
        type: str
      - help: Override active server
        name: server
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Slock: account-actions

Change reversible account relationship or saved state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `bookmark-add` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Bookmark a message (POST /channels/saved). Requires full messageId UUID. | `messageId` (str, required, positional); `server` (str, optional) |
| `thread-follow` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Follow the thread on a parent message (POST /channels/threads/follow) | `parentMessageId` (str, required, positional); `server` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
