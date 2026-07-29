---
opencli_contract:
  version: 2
  site: producthunt
  operation: discovery
  policy_sha256: c1f2952ebd536707c900ca251a688f82f094c3d514fff6f0a8b9b5bfa28bc222
  commands:
    browse:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: browser_intercept
      strategy: intercept
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Category slug, e.g. vibe-coding, ai-agents, developer-tools
        name: category
        positional: true
        required: true
        type: string
      - default: 20
        help: Number of results (max 50)
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
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: browser_intercept
      strategy: intercept
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: Number of results (max 50)
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

# Producthunt: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `browse` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Best products in a Product Hunt category | `category` (string, required, positional); `limit` (int, optional, default=20) |
| `hot` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Today's top Product Hunt launches with vote counts | `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
