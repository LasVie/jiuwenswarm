---
opencli_contract:
  version: 2
  site: upwork
  operation: private-content
  policy_sha256: b72915895eb81bb776af49116cb56ea9889cc673b7cd846e6b21d897ad96ff7b
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
      - help: Job ciphertext id (~01… / ~02…) or full /jobs/~02… URL
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
    feed:
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
      - default: best-matches
        help: 'Feed tab: best-matches | most-recent'
        name: tab
        positional: true
        required: false
        type: str
      - default: 20
        help: Max rows to return (1-50, capped at one page)
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
      - help: Job keyword (skill / title / company)
        name: query
        positional: true
        required: true
        type: str
      - default: ''
        help: Country/city filter (e.g. "United States", "Remote")
        name: location
        required: false
        type: string
      - default: ''
        help: Category uid filter (advanced; from job detail `category` slug)
        name: category
        required: false
        type: string
      - default: recency
        help: 'Sort: recency | relevance | client_total_charge | client_total_reviews'
        name: sort
        required: false
        type: string
      - default: 1
        help: Page number (1-based)
        name: page
        required: false
        type: int
      - default: 10
        help: Rows per page (10-50, capped at one page)
        name: per_page
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

# Upwork: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `detail` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read the full Upwork job posting by ciphertext id (e.g. ~022054964136512093518) | `id` (str, required, positional) |
| `feed` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Upwork personalized jobs feed (best-matches \| most-recent) — requires login | `tab` (str, optional, positional, default='best-matches'); `limit` (int, optional, default=20) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Upwork keyword job search (logged-in browser session, US site) | `query` (str, required, positional); `location` (string, optional, default=''); `category` (string, optional, default=''); `sort` (string, optional, default='recency'); `page` (int, optional, default=1); `per_page` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
