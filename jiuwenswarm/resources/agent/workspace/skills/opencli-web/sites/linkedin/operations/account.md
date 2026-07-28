---
opencli_contract:
  version: 2
  site: linkedin
  operation: account
  policy_sha256: d0c16e9f75ca1a20826b14b84ed1623a5a25b38ba0d1785c847e19d8620f8018
  commands:
    profile-analytics:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: LinkedIn /in/<handle>/ profile URL. Defaults to /in/me/.
        name: profile-url
        required: false
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - account identifiers
    profile-experience:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: LinkedIn /in/<handle>/ profile URL. Defaults to /in/me/.
        name: profile-url
        required: false
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - account identifiers
    profile-projects:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: LinkedIn /in/<handle>/ profile URL. Defaults to /in/me/.
        name: profile-url
        required: false
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - account identifiers
    profile-read:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: LinkedIn /in/<handle>/ profile URL. Defaults to /in/me/.
        name: profile-url
        required: false
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - account identifiers
    whoami:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - account identifiers
---

# Linkedin: account

Read account identity or account-scoped metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `profile-analytics` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read visible LinkedIn profile dashboard metrics such as profile views, post impressions, and search appearances | `profile-url` (string, optional) |
| `profile-experience` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read visible LinkedIn profile experience entries with titles, dates, locations, skills, media, and URLs | `profile-url` (string, optional) |
| `profile-projects` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read visible LinkedIn profile projects with descriptions, dates, skills, media, and URLs | `profile-url` (string, optional) |
| `profile-read` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read visible LinkedIn profile sections: headline, About, experience, education, services, and featured sections | `profile-url` (string, optional) |
| `whoami` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>Show the current logged-in linkedin account | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
