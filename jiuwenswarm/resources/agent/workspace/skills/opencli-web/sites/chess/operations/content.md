---
opencli_contract:
  version: 2
  site: chess
  operation: content
  policy_sha256: e8c3b37662ff4dd4a650f22484e05b9ecf10da13cf7767fea80c0fbe56ebb631
  commands:
    game:
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
      - help: Full game URL, e.g. https://www.chess.com/game/live/168842570216
        name: game-url
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
    games:
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
      - help: Chess.com username
        name: username
        positional: true
        required: true
        type: string
      - default: 10
        help: Number of recent games (1-100)
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

# Chess: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `game` | `enabled` | `public_read` / `low` | `opencli_execute(site="chess", operation="content", command="game", arguments={"game-url":"<game-url>"})`<br>Chess.com single-game detail (white, black, result, ECO, time control) by full game URL | `game-url` (string, required, positional) |
| `games` | `enabled` | `public_read` / `low` | `opencli_execute(site="chess", operation="content", command="games", arguments={"username":"<username>"})`<br>Chess.com recent games for a player, newest first | `username` (string, required, positional); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
