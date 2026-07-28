---
opencli_contract:
  version: 2
  site: indeed
  operation: private-content
  policy_sha256: 8fe15b8b2b5b75cfc7faf1eeba8d6678c117d8440c5e4cd3ab2dcb9529c403c1
  commands:
    job:
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
      - help: Job key (16-char hex from `indeed search`, e.g. "dccc07ac5a6a3683")
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
      - help: Job keyword (title / skill / company)
        name: query
        positional: true
        required: true
        type: str
      - default: ''
        help: Location filter (e.g. "remote", "New York, NY", "San Francisco")
        name: location
        required: false
        type: string
      - default: ''
        help: 'Recency filter, days back: 1 / 3 / 7 / 14'
        name: fromage
        required: false
        type: string
      - default: relevance
        help: 'Sort order: relevance | date'
        name: sort
        required: false
        type: string
      - default: 0
        help: Pagination offset (multiple of 10, 0-based)
        name: start
        required: false
        type: int
      - default: 15
        help: Max rows to return (1-25, capped at one page)
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

# Indeed: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `job` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read the full Indeed job posting by jk (job key) | `id` (str, required, positional) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Indeed keyword job search (rendered DOM via browser session, US site) | `query` (str, required, positional); `location` (string, optional, default=''); `fromage` (string, optional, default=''); `sort` (string, optional, default='relevance'); `start` (int, optional, default=0); `limit` (int, optional, default=15) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
