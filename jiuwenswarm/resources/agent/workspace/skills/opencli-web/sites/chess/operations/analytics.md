---
opencli_contract:
  version: 2
  site: chess
  operation: analytics
  policy_sha256: f63635437ea3ad1b58eb4ccde8ec5e1b310dbef5bd61eaeed49597a494678fde
  commands:
    stats:
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
      - help: Chess.com username (case-insensitive)
        name: username
        positional: true
        required: true
        type: string
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Chess: analytics

Read aggregate metrics, trends, or rankings.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `stats` | `enabled` | `public_read` / `low` | `opencli_execute(site="chess", operation="analytics", command="stats", arguments={"username":"<username>"})`<br>Chess.com player ratings + win/loss record across game kinds | `username` (string, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
