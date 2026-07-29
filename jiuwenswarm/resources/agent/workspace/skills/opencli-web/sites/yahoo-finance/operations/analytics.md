---
opencli_contract:
  version: 2
  site: yahoo-finance
  operation: analytics
  policy_sha256: 4d01cc82090cb1a349ecb4ac33d5b70f7de1458a0bb5ecbdcc7fde25c75a822c
  commands:
    quote:
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
      - help: Stock ticker (e.g. AAPL, MSFT, TSLA)
        name: symbol
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
---

# Yahoo Finance: analytics

Read aggregate metrics, trends, or rankings.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `quote` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Yahoo Finance 股票行情 | `symbol` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
