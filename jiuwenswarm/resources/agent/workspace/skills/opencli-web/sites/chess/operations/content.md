---
opencli_contract:
  version: 2
  site: chess
  operation: content
  policy_sha256: f63635437ea3ad1b58eb4ccde8ec5e1b310dbef5bd61eaeed49597a494678fde
  commands:
    analyze:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Full game URL, e.g. https://www.chess.com/game/live/168842570216
        name: game-url
        positional: true
        required: true
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
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
| `analyze` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Open a Chess.com game in the browser analysis board | `game-url` (string, required, positional) |
| `game` | `enabled` | `public_read` / `low` | `opencli_execute(site="chess", operation="content", command="game", arguments={"game-url":"<game-url>"})`<br>Chess.com single-game detail (white, black, result, ECO, time control) by full game URL | `game-url` (string, required, positional) |
| `games` | `enabled` | `public_read` / `low` | `opencli_execute(site="chess", operation="content", command="games", arguments={"username":"<username>"})`<br>Chess.com recent games for a player, newest first | `username` (string, required, positional); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
