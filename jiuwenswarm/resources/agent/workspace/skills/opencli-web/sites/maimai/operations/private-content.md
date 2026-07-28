---
opencli_contract:
  version: 2
  site: maimai
  operation: private-content
  policy_sha256: c3a7768b30c706b0535c75e785fc1f483166cfdf8f9201442b2b88580a2fa9d9
  commands:
    search-talents:
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
      - help: Search keyword (e.g., "Java", "产品经理")
        name: query
        positional: true
        required: true
        type: str
      - default: 0
        help: Page number (0-based)
        name: page
        required: false
        type: int
      - default: 20
        help: Results per page
        name: size
        required: false
        type: int
      - help: Positions (e.g., "运营", "Java 开发工程师")
        name: positions
        required: false
        type: str
      - help: Companies, comma-separated (e.g., "百度", "字节跳动，阿里巴巴")
        name: companies
        required: false
        type: str
      - help: Schools, comma-separated (e.g., "北京大学", "清华大学，复旦大学")
        name: schools
        required: false
        type: str
      - help: Provinces (e.g., "北京", "上海")
        name: provinces
        required: false
        type: str
      - help: Cities (e.g., "北京市", "上海市")
        name: cities
        required: false
        type: str
      - help: 'Work years: 1=1-3y, 2=3-5y, 3=5-10y, 4=10+y'
        name: worktimes
        required: false
        type: str
      - help: 'Education: 1=大专，2=本科，3=硕士，4=博士，5=MBA'
        name: degrees
        required: false
        type: str
      - help: 'Industries: 01=互联网，02=金融，03=电子，04=通信'
        name: professions
        required: false
        type: str
      - help: '211 university: 0=any, 1=211'
        name: is_211
        required: false
        type: int
      - help: '985 university: 0=any, 1=985'
        name: is_985
        required: false
        type: int
      - default: 0
        help: 'Sort: 0=relevance, 1=activity, 2=work_years, 3=education'
        name: sortby
        required: false
        type: int
      - default: 0
        help: 'Direct chat: 0=any, 1=available'
        name: is_direct_chat
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

# Maimai: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search-talents` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Search for candidates on Maimai with multi-dimensional filters | `query` (str, required, positional); `page` (int, optional, default=0); `size` (int, optional, default=20); `positions` (str, optional); `companies` (str, optional); `schools` (str, optional); `provinces` (str, optional); `cities` (str, optional); `worktimes` (str, optional); `degrees` (str, optional); `professions` (str, optional); `is_211` (int, optional); `is_985` (int, optional); `sortby` (int, optional, default=0); `is_direct_chat` (int, optional, default=0) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
