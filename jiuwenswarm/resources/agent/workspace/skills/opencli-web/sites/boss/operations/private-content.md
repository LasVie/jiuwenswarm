---
opencli_contract:
  version: 2
  site: boss
  operation: private-content
  policy_sha256: 0512851bb10f8f329773a56b353cc02733b09e02ba73228f57eeb2307bd963c3
  commands:
    chatlist:
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
      - default: 1
        help: Page number
        name: page
        required: false
        type: int
      - default: 20
        help: Number of results
        name: limit
        required: false
        type: int
      - default: '0'
        help: Filter by job ID (0=all, boss side only)
        name: job-id
        required: false
        type: str
      - choices:
        - auto
        - boss
        - geek
        default: auto
        help: 'Identity side: auto (default), boss (recruiter), or geek (job-seeker)'
        name: side
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
    chatmsg:
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
      - help: Encrypted UID (from chatlist)
        name: uid
        positional: true
        required: true
        type: str
      - default: 1
        help: Page number
        name: page
        required: false
        type: int
      - choices:
        - auto
        - boss
        - geek
        default: auto
        help: 'Identity side: auto (default), boss (recruiter), or geek (job-seeker)'
        name: side
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
    joblist:
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
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    recommend:
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
      - default: 20
        help: Number of results to return
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
    resume:
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
      - help: Encrypted UID of the candidate (from chatlist)
        name: uid
        positional: true
        required: true
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
    stats:
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
      - default: ''
        help: Encrypted job ID (show all if empty)
        name: job-id
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
---

# Boss: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `chatlist` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>BOSS直聘查看聊天列表（招聘端/求职端） | `page` (int, optional, default=1); `limit` (int, optional, default=20); `job-id` (str, optional, default='0'); `side` (str, optional, default='auto', choices=auto,boss,geek) |
| `chatmsg` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>BOSS直聘查看聊天消息历史（招聘端/求职端） | `uid` (str, required, positional); `page` (int, optional, default=1); `side` (str, optional, default='auto', choices=auto,boss,geek) |
| `joblist` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>BOSS直聘查看我发布的职位列表 | none |
| `recommend` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>BOSS直聘查看推荐候选人（新招呼列表） | `limit` (int, optional, default=20) |
| `resume` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>BOSS直聘查看候选人简历（招聘端） | `uid` (str, required, positional) |
| `stats` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>BOSS直聘职位数据统计 | `job-id` (str, optional, default='') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
