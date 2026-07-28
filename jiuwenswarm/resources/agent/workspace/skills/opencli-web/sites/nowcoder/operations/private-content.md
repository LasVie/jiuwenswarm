---
opencli_contract:
  version: 2
  site: nowcoder
  operation: private-content
  policy_sha256: af747700ded643be1d096416626644585a5c21694b06876529968abad28c8085
  commands:
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
      - help: Post ID, UUID, or URL
        name: id
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
    experience:
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
      - default: 15
        help: Number of items
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
    notifications:
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
    papers:
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
      - default: '11002'
        help: Job ID (11002=Java, 11003=C++, 11200=Backend, 11203=QA, 11201=Frontend)
        name: job
        required: false
        type: str
      - default: ''
        help: Company ID (e.g. 139=Baidu, 138=Tencent, 239=Huawei)
        name: company
        required: false
        type: str
      - default: 10
        help: Number of items
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
    practice:
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
      - default: '11226'
        help: Career ID (11226=Software, 11227=Hardware, 11229=Product, 11230=Finance)
        name: job
        required: false
        type: str
      - default: 20
        help: Number of items
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
    referral:
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
      - default: 15
        help: Number of items
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
    salary:
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
      - default: 15
        help: Number of items
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
      - help: Search keyword
        name: query
        positional: true
        required: true
        type: str
      - default: all
        help: Search type (all/post/question/user/job)
        name: type
        required: false
        type: str
      - default: 10
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
    suggest:
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
      - help: Search keyword
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
      sensitive_output:
      - private content
      - account identifiers
---

# Nowcoder: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `detail` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Post detail view (supports ID / UUID / URL) | `id` (str, required, positional) |
| `experience` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Interview experience posts | `page` (int, optional, default=1); `limit` (int, optional, default=15) |
| `notifications` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Unread message summary | none |
| `papers` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Interview question bank by company and job | `job` (str, optional, default='11002'); `company` (str, optional, default=''); `limit` (int, optional, default=10) |
| `practice` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Categorized practice questions with progress | `job` (str, optional, default='11226'); `limit` (int, optional, default=20) |
| `referral` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Internal referral posts | `page` (int, optional, default=1); `limit` (int, optional, default=15) |
| `salary` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Salary disclosure posts | `page` (int, optional, default=1); `limit` (int, optional, default=15) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Full-text search | `query` (str, required, positional); `type` (str, optional, default='all'); `limit` (int, optional, default=10) |
| `suggest` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Search suggestions | `query` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
