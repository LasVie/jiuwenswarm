---
opencli_contract:
  version: 2
  site: boss
  operation: private-content
  policy_sha256: 7bf0146c4d09d643b06c584dccd0f48d8b22e84aa66a69872e0757c0841e48a5
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
    detail:
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
      - help: Security ID from search results (securityId field)
        name: security-id
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
    search:
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
      - help: Search keyword (optional, empty = recommended jobs)
        name: query
        positional: true
        required: false
        type: str
      - default: 北京
        help: City name or code (e.g. 杭州, 上海, 101010100)
        name: city
        required: false
        type: str
      - default: ''
        help: 'Experience: 在校生(实习)/应届生(校招)/经验不限/1年以内/1-3年/3-5年/5-10年/10年以上'
        name: experience
        required: false
        type: str
      - default: ''
        help: 'Degree: 大专/本科/硕士/博士'
        name: degree
        required: false
        type: str
      - default: ''
        help: 'Salary: 3K以下/3-5K/5-10K/10-15K/15-20K/20-30K/30-50K/50K以上'
        name: salary
        required: false
        type: str
      - default: ''
        help: Industry code or name (e.g. 100020, 互联网)
        name: industry
        required: false
        type: str
      - default: ''
        help: 'Job type: 全职/兼职/实习（不传=不限，混合校招与实习）'
        name: jobType
        required: false
        type: str
      - default: 1
        help: Page number
        name: page
        required: false
        type: int
      - default: 15
        help: Number of results
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
| `detail` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>BOSS直聘查看职位详情 | `security-id` (str, required, positional) |
| `joblist` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>BOSS直聘查看我发布的职位列表 | none |
| `recommend` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>BOSS直聘查看推荐候选人（新招呼列表） | `limit` (int, optional, default=20) |
| `resume` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>BOSS直聘查看候选人简历（招聘端） | `uid` (str, required, positional) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>BOSS直聘搜索职位（不带关键词时返回为你推荐职位） | `query` (str, optional, positional); `city` (str, optional, default='北京'); `experience` (str, optional, default=''); `degree` (str, optional, default=''); `salary` (str, optional, default=''); `industry` (str, optional, default=''); `jobType` (str, optional, default=''); `page` (int, optional, default=1); `limit` (int, optional, default=15) |
| `stats` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>BOSS直聘职位数据统计 | `job-id` (str, optional, default='') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
