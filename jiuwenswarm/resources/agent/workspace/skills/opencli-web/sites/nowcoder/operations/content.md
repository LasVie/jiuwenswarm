---
opencli_contract:
  version: 2
  site: nowcoder
  operation: content
  policy_sha256: 8a5afbc7161bd46d50a4cd170c19607059ebeebdaa8692237ad97edcdb31e061
  commands:
    companies:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: '11002'
        help: Job ID (11002=Java, 11003=C++, 11200=Backend, 11203=QA, 11201=Frontend)
        name: job
        required: false
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    creators:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: 10
        help: Number of items
        name: limit
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    detail:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    experience:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    hot:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: 10
        help: Number of items
        name: limit
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    jobs:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args: []
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    papers:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    recommend:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
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
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    referral:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    salary:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    topics:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: 10
        help: Number of items
        name: limit
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Nowcoder: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `companies` | `enabled` | `public_read` / `low` | `opencli_execute(site="nowcoder", operation="content", command="companies")`<br>Hot companies for interview prep | `job` (str, optional, default='11002') |
| `creators` | `enabled` | `public_read` / `low` | `opencli_execute(site="nowcoder", operation="content", command="creators")`<br>Top content creators leaderboard | `limit` (int, optional, default=10) |
| `detail` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Post detail view (supports ID / UUID / URL) | `id` (str, required, positional) |
| `experience` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Interview experience posts | `page` (int, optional, default=1); `limit` (int, optional, default=15) |
| `hot` | `enabled` | `public_read` / `low` | `opencli_execute(site="nowcoder", operation="content", command="hot")`<br>Hot search ranking | `limit` (int, optional, default=10) |
| `jobs` | `enabled` | `public_read` / `low` | `opencli_execute(site="nowcoder", operation="content", command="jobs")`<br>Career category listing | none |
| `papers` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Interview question bank by company and job | `job` (str, optional, default='11002'); `company` (str, optional, default=''); `limit` (int, optional, default=10) |
| `recommend` | `enabled` | `public_read` / `low` | `opencli_execute(site="nowcoder", operation="content", command="recommend")`<br>Recommended feed | `page` (int, optional, default=1); `limit` (int, optional, default=15) |
| `referral` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Internal referral posts | `page` (int, optional, default=1); `limit` (int, optional, default=15) |
| `salary` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Salary disclosure posts | `page` (int, optional, default=1); `limit` (int, optional, default=15) |
| `topics` | `enabled` | `public_read` / `low` | `opencli_execute(site="nowcoder", operation="content", command="topics")`<br>Hot discussion topics | `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
