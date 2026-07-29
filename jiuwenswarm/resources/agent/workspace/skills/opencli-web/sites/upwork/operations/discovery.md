---
opencli_contract:
  version: 2
  site: upwork
  operation: discovery
  policy_sha256: 1d10bc6218b6d560645d06ab55894f4993fe0c04ae042f221c635f1db2599946
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Upwork: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Upwork keyword job search (logged-in browser session, US site) | `query` (str, required, positional); `location` (string, optional, default=''); `category` (string, optional, default=''); `sort` (string, optional, default='recency'); `page` (int, optional, default=1); `per_page` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
