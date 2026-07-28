---
opencli_contract:
  version: 2
  site: reddit
  operation: account-actions
  policy_sha256: 0487426fd966b3a96ccef136af5816f03b5ade5e203ef9e262e722a48273f258
  commands:
    save:
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
      - help: Post ID (e.g. 1abc123) or fullname (t3_xxx)
        name: post-id
        positional: true
        required: true
        type: string
      - default: false
        help: Unsave instead of save
        name: undo
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    subscribe:
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
      - help: Subreddit name (e.g. python)
        name: subreddit
        positional: true
        required: true
        type: string
      - default: false
        help: Unsubscribe instead of subscribe
        name: undo
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Reddit: account-actions

Change reversible account relationship or saved state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `save` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Save or unsave a Reddit post | `post-id` (string, required, positional); `undo` (boolean, optional, default=False) |
| `subscribe` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Subscribe or unsubscribe to a subreddit | `subreddit` (string, required, positional); `undo` (boolean, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
