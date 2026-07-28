---
opencli_contract:
  version: 2
  site: kimi
  operation: write-actions
  policy_sha256: 056583a5f1c52cef59531c9069f8800486317741e706b3dc0a99070b53dabbaa
  commands:
    dismiss-banner:
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
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    history-rename:
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
      - help: Chat id (UUID-like)
        name: chat-id
        positional: true
        required: true
        type: str
      - help: New title
        name: new-title
        positional: true
        required: true
        type: str
      - default: false
        help: 'Actually rename (default: dry-run)'
        name: 'yes'
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    mode:
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
      - help: Mode name (omit to list all)
        name: name
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
    model:
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
      - default: false
        help: Open model dropdown + list options
        name: list
        required: false
        type: boolean
      - help: Substring (case-insensitive) of model to switch to
        name: set
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    react:
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
      - help: like or dislike
        name: kind
        positional: true
        required: true
        type: str
      - help: Chat id or URL
        name: conv
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    regenerate:
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
      - help: Chat id or URL
        name: conv
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    settings:
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
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    share:
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
      - help: Chat id or URL
        name: conv
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    sidebar-toggle:
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
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    sign-out:
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
      - default: false
        help: 'Actually sign out (default: dry-run)'
        name: 'yes'
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    upgrade:
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
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    view-all-history:
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
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Kimi: write-actions

Change remote service state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `dismiss-banner` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Close any visible sidebar banner (e.g., "Make a Review & Earn Credit", "获取应用程序") by clicking its Close svg. | none |
| `history-rename` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Rename a chat from the /chat/history page (clicks the inline Edit svg next to a chat row, types the new title, and saves). Requires --yes. | `chat-id` (str, required, positional); `new-title` (str, required, positional); `yes` (boolean, optional, default=False) |
| `mode` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Switch to a Kimi work mode: ppt \| docs \| deep-research \| websites \| sheets \| agent-swarm \| code. With no argument, lists modes. | `name` (str, optional, positional) |
| `model` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Read the current Kimi model (e.g. "K2.6 思考") or switch by clicking the model dropdown. With no argument, returns current; with --list, opens dropdown + lists; with --set <name>, switches. | `list` (boolean, optional, default=False); `set` (str, optional) |
| `react` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Like or dislike the last assistant message. Pass --conv <id> to target a specific chat. | `kind` (str, required, positional); `conv` (str, optional) |
| `regenerate` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Click Refresh (Kimi's regenerate button) on the last assistant message. Pass --conv <id> to target a specific chat. | `conv` (str, optional) |
| `settings` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Open the Kimi settings page (/settings). | none |
| `share` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Click Share on the last assistant message (opens Kimi's share dialog). Pass --conv <id> to target a specific chat. | `conv` (str, optional) |
| `sidebar-toggle` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Click the LeftBar svg to toggle the Kimi sidebar. | none |
| `sign-out` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Click SignOut on the Kimi /settings page. Navigates to /settings first if not already there. Requires --yes. | `yes` (boolean, optional, default=False) |
| `upgrade` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Click the "Upgrade" button (or 升级会员) in the Kimi sidebar — opens the membership/upgrade page or dialog. | none |
| `view-all-history` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Navigate to /chat/history (full conversation list page). | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
