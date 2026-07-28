---
opencli_contract:
  version: 2
  site: lesswrong
  operation: generation
  policy_sha256: 09260253b3cc2232c5b1d13f95df38bddde26310c970ef660f5811e93bc1816b
  commands:
    new:
      executor: none
      execution_state: disabled
      semantic_effect: quota_consumption
      risk: high
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: 10
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

# Lesswrong: generation

Generate remote content, start AI work, or consume quota.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `new` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Latest posts | `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
