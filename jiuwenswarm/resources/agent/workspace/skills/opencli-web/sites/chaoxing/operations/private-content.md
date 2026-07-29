---
opencli_contract:
  version: 2
  site: chaoxing
  operation: private-content
  policy_sha256: 3ca8510877d5a6238f9adf9c1032c3fac301b6d4b67d4da983d75efe61baca6c
  commands:
    assignments:
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
      - help: 按课程名过滤（模糊匹配）
        name: course
        required: false
        type: string
      - choices:
        - all
        - pending
        - submitted
        - graded
        default: all
        help: 按状态过滤
        name: status
        required: false
        type: string
      - default: 20
        help: 最大返回数量
        name: limit
        required: false
        type: int
      - default: 90
        help: 'Max seconds for the overall command (default: 90)'
        name: timeout
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
    exams:
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
      - help: 按课程名过滤（模糊匹配）
        name: course
        required: false
        type: string
      - choices:
        - all
        - upcoming
        - ongoing
        - finished
        default: all
        help: 按状态过滤
        name: status
        required: false
        type: string
      - default: 20
        help: 最大返回数量
        name: limit
        required: false
        type: int
      - default: 90
        help: 'Max seconds for the overall command (default: 90)'
        name: timeout
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

# Chaoxing: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `assignments` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>学习通作业列表 | `course` (string, optional); `status` (string, optional, default='all', choices=all,pending,submitted,graded); `limit` (int, optional, default=20); `timeout` (int, optional, default=90) |
| `exams` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>学习通考试列表 | `course` (string, optional); `status` (string, optional, default='all', choices=all,upcoming,ongoing,finished); `limit` (int, optional, default=20); `timeout` (int, optional, default=90) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
