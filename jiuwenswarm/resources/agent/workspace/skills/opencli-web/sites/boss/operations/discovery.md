---
opencli_contract:
  version: 2
  site: boss
  operation: discovery
  policy_sha256: 0512851bb10f8f329773a56b353cc02733b09e02ba73228f57eeb2307bd963c3
  commands:
    search:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
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
      sensitive_output: []
---

# Boss: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>BOSS直聘搜索职位（不带关键词时返回为你推荐职位） | `query` (str, optional, positional); `city` (str, optional, default='北京'); `experience` (str, optional, default=''); `degree` (str, optional, default=''); `salary` (str, optional, default=''); `industry` (str, optional, default=''); `jobType` (str, optional, default=''); `page` (int, optional, default=1); `limit` (int, optional, default=15) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
