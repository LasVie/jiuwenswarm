---
opencli_contract:
  version: 2
  site: weread
  operation: analytics
  policy_sha256: 2345432046fe5a6fb8663c41d6493c34c7ad68f543993ae9cfc313e120ab29f1
  commands:
    ranking:
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
      - default: all
        help: 'Category: all (default), rising, or numeric category ID'
        name: category
        positional: true
        required: false
        type: str
      - default: 20
        help: Max results
        name: limit
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Weread: analytics

Read aggregate metrics, trends, or rankings.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `ranking` | `enabled` | `public_read` / `low` | `opencli_execute(site="weread", operation="analytics", command="ranking")`<br>WeRead book rankings by category | `category` (str, optional, positional, default='all'); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
