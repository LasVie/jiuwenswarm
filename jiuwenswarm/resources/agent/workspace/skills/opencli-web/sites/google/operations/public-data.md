---
opencli_contract:
  version: 2
  site: google
  operation: public-data
  policy_sha256: 8f8e9b5f1df0ce31cba6ad236f14011d957450747655c76b7cc1583a8e22d329
  commands:
    news:
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
      - help: Search query (omit for top stories)
        name: keyword
        positional: true
        required: false
        type: str
      - default: 10
        help: Number of results
        name: limit
        required: false
        type: int
        constraints:
          minimum: 1
          maximum: 100
      - default: en
        help: Language short code (e.g. en, zh)
        name: lang
        required: false
        type: str
        constraints:
          pattern: ^[A-Za-z]{2,3}(?:-[A-Za-z0-9]+)?$
      - default: US
        help: Region code (e.g. US, CN)
        name: region
        required: false
        type: str
        constraints:
          pattern: ^[A-Z]{2}$
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    suggest:
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
      - help: Search query
        name: keyword
        positional: true
        required: true
        type: str
      - default: zh-CN
        help: Language code
        name: lang
        required: false
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    trends:
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
      - default: US
        help: Region code (e.g. US, CN, JP)
        name: region
        required: false
        type: str
        constraints:
          pattern: ^[A-Z]{2}$
      - default: 20
        help: Number of results
        name: limit
        required: false
        type: int
        constraints:
          minimum: 1
          maximum: 100
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Google: public-data

Read low-risk public data without browser state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `news` | `enabled` | `public_read` / `low` | `opencli_execute(site="google", operation="public-data", command="news")`<br>Get Google News headlines | `keyword` (str, optional, positional); `limit` (int, optional, default=10, minimum=1,maximum=100); `lang` (str, optional, default='en', pattern=^[A-Za-z]{2,3}(?:-[A-Za-z0-9]+)?$); `region` (str, optional, default='US', pattern=^[A-Z]{2}$) |
| `suggest` | `enabled` | `public_read` / `low` | `opencli_execute(site="google", operation="public-data", command="suggest", arguments={"keyword":"<keyword>"})`<br>Get Google search suggestions | `keyword` (str, required, positional); `lang` (str, optional, default='zh-CN') |
| `trends` | `enabled` | `public_read` / `low` | `opencli_execute(site="google", operation="public-data", command="trends")`<br>Get Google Trends daily trending searches | `region` (str, optional, default='US', pattern=^[A-Z]{2}$); `limit` (int, optional, default=20, minimum=1,maximum=100) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
