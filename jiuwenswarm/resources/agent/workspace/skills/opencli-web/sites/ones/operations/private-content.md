---
opencli_contract:
  version: 2
  site: ones
  operation: private-content
  policy_sha256: 64d44ee783edfb380e515b610ab3f68cdc26d3c6e52d68eae4e61b20a8f378e0
  commands:
    my-tasks:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Team UUID from URL …/team/<uuid>/…, or set ONES_TEAM_UUID
        name: team
        positional: true
        required: false
        type: str
      - default: 100
        help: Max rows (default 100, max 500)
        name: limit
        required: false
        type: int
      - choices:
        - assign
        - field004
        - owner
        - both
        default: assign
        help: assign=负责人(顶层 assign)；field004=负责人(筛选器示例里的 field004)；owner=创建者；both=负责人∪创建者(两次 peek 去重)
        name: mode
        required: false
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
    task:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Work item UUID (often 16 chars) from …/task/<id>
        name: id
        positional: true
        required: true
        type: str
      - help: Team UUID (8 chars from …/team/<team>/…), or set ONES_TEAM_UUID
        name: team
        required: false
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
    tasks:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Team UUID (8 chars), or set ONES_TEAM_UUID
        name: team
        positional: true
        required: false
        type: str
      - help: Filter by project UUID (field006 / 所属项目)
        name: project
        required: false
        type: str
      - help: Filter by assignee user UUID (负责人 assign)
        name: assign
        required: false
        type: str
      - default: 30
        help: Max rows after flattening groups (default 30)
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

# Ones: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `my-tasks` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>ONES — my work items (filters/peek + strict must query). Default: assignee=me. Use --mode if your site uses field004 for assignee. | `team` (str, optional, positional); `limit` (int, optional, default=100); `mode` (str, optional, default='assign', choices=assign,field004,owner,both) |
| `task` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>ONES — work item detail (GET team/:team/task/:id/info); id is URL segment after …/task/ | `id` (str, required, positional); `team` (str, optional) |
| `tasks` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>ONES Project API — list work items (POST team/:team/filters/peek); use token-info -f json for team uuid | `team` (str, optional, positional); `project` (str, optional); `assign` (str, optional); `limit` (int, optional, default=30) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
