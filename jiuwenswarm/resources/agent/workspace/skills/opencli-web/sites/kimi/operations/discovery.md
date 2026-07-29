---
opencli_contract:
  version: 2
  site: kimi
  operation: discovery
  policy_sha256: 06589d724fcc28aebeb0e534d47ba40ca82b10436b9126fb01a38ef3b18467a7
  commands:
    templates:
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
      - help: 'Navigate to mode first: ppt|docs|deep-research|agent|websites|sheets|agent-swarm|code'
        name: mode
        required: false
        type: str
      - default: 30
        help: ''
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
---

# Kimi: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `templates` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>List template cards visible on a Kimi mode page (PPT/docs/deep-research/agent). Each mode shows curated example projects organized by category. Pass --mode to navigate first. | `mode` (str, optional); `limit` (int, optional, default=30) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
