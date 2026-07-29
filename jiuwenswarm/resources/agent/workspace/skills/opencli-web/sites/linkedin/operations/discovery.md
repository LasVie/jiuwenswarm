---
opencli_contract:
  version: 2
  site: linkedin
  operation: discovery
  policy_sha256: 318b046f8d0394572c515dd0fcd92133ed118ddb2219732dc3c17115eac020f9
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
      - help: Job search keywords
        name: query
        positional: true
        required: true
        type: string
      - help: Location text such as San Francisco Bay Area
        name: location
        required: false
        type: string
      - default: 10
        help: Number of jobs to return (max 100)
        name: limit
        required: false
        type: int
      - default: 0
        help: Result offset for pagination
        name: start
        required: false
        type: int
      - default: false
        help: Include full job description and apply URL (slower)
        name: details
        required: false
        type: bool
      - help: Comma-separated company names or LinkedIn company IDs
        name: company
        required: false
        type: string
      - help: 'Comma-separated: internship, entry, associate, mid-senior, director, executive'
        name: experience-level
        required: false
        type: string
      - help: 'Comma-separated: full-time, part-time, contract, temporary, volunteer, internship, other'
        name: job-type
        required: false
        type: string
      - help: 'One of: any, month, week, 24h'
        name: date-posted
        required: false
        type: string
      - help: 'Comma-separated: on-site, hybrid, remote'
        name: remote
        required: false
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Linkedin: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Search LinkedIn jobs | `query` (string, required, positional); `location` (string, optional); `limit` (int, optional, default=10); `start` (int, optional, default=0); `details` (bool, optional, default=False); `company` (string, optional); `experience-level` (string, optional); `job-type` (string, optional); `date-posted` (string, optional); `remote` (string, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
