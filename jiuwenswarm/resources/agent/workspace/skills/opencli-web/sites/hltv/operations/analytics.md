---
opencli_contract:
  version: 2
  site: hltv
  operation: analytics
  policy_sha256: 1276b6cc8052e138ba6068e902742a0cf0e015e0280365a553990195ff3394b2
  commands:
    event-matches:
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
      - help: Event id, /events/:id URL, or stats URL with event=
        name: event
        positional: true
        required: true
        type: string
      - default: 100
        help: Rows to return from the visible stats matches table (max 100)
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
    match-map:
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
      - help: Full HLTV /stats/matches/mapstatsid/:id/:slug URL from player-matches
        name: match
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
    match-series:
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
      - help: HLTV match, stats series, or mapstats URL
        name: match
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
    player-duel:
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
      - help: 'First player ref: 19230/m0nesy, player URL, or stats player URL'
        name: playerA
        positional: true
        required: true
        type: string
      - help: 'Second player ref: 3741/niko, player URL, or stats player URL'
        name: playerB
        positional: true
        required: true
        type: string
      - default: ''
        help: Optional HLTV match, stats series, or mapstats URL
        name: match
        required: false
        type: string
      - default: lastEncounter
        help: lastEncounter / intersection / history. Ignored when --match is provided
        name: mode
        required: false
        type: string
      - default: all
        help: all / lastMonth / last3Months / last6Months / last12Months / YYYY / YYYY-MM-DD:YYYY-MM-DD
        name: period
        required: false
        type: string
      - default: all
        help: all / majors / bigEvents / mvpEvents / lan / online
        name: eventType
        required: false
        type: string
      - default: all
        help: all / event id / /events/:id URL / stats URL with event=
        name: event
        required: false
        type: string
      - default: all
        help: all / top5 / top10 / top20 / top30 / top50
        name: ranking
        required: false
        type: string
      - default: all
        help: all / ancient / anubis / dust2 / inferno / mirage / nuke / overpass / cache / cobblestone / season / train / tuscan / vertigo
        name: map
        required: false
        type: string
      - default: both
        help: both / cs2 / csgo
        name: version
        required: false
        type: string
      - default: 0
        help: Pagination offset for broad mode; must be a multiple of 100
        name: offset
        required: false
        type: int
      - default: 100
        help: lastEncounter mode candidate maps from playerA to scan (max 500)
        name: recentMaps
        required: false
        type: int
      - default: 1
        help: Broad mode pages to scan, 100 rows each (max 5)
        name: scanPages
        required: false
        type: int
      - default: 20
        help: Maximum shared maps to compare (max 100)
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
    player-form:
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
      - default: 3741/niko
        help: 'Player ref: 3741/niko, player URL, or stats matches URL'
        name: player
        required: false
        type: string
      - default: all
        help: all / lastMonth / last3Months / last6Months / last12Months / YYYY / YYYY-MM-DD:YYYY-MM-DD
        name: period
        required: false
        type: string
      - default: all
        help: all / majors / bigEvents / mvpEvents / lan / online
        name: eventType
        required: false
        type: string
      - default: all
        help: all / top5 / top10 / top20 / top30 / top50
        name: ranking
        required: false
        type: string
      - default: all
        help: all / ancient / anubis / dust2 / inferno / mirage / nuke / overpass / cache / cobblestone / season / train / tuscan / vertigo
        name: map
        required: false
        type: string
      - default: both
        help: both / cs2 / csgo
        name: version
        required: false
        type: string
      - default: 0
        help: Pagination offset; must be a multiple of 100
        name: offset
        required: false
        type: int
      - default: 30
        help: Recent maps to aggregate from the current page (max 100)
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
    player-map-pool:
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
      - default: 3741/niko
        help: 'Player ref: 3741/niko, player URL, or stats player URL'
        name: player
        required: false
        type: string
      - default: all
        help: all / lastMonth / last3Months / last6Months / last12Months / YYYY / YYYY-MM-DD:YYYY-MM-DD
        name: period
        required: false
        type: string
      - default: all
        help: all / majors / bigEvents / mvpEvents / lan / online
        name: eventType
        required: false
        type: string
      - default: all
        help: all / event id / /events/:id URL / stats URL with event=
        name: event
        required: false
        type: string
      - default: all
        help: all / top5 / top10 / top20 / top30 / top50
        name: ranking
        required: false
        type: string
      - default: all
        help: all / ancient / anubis / dust2 / inferno / mirage / nuke / overpass / cache / cobblestone / season / train / tuscan / vertigo
        name: map
        required: false
        type: string
      - default: both
        help: both / cs2 / csgo
        name: version
        required: false
        type: string
      - default: 0
        help: Pagination offset; must be a multiple of 100
        name: offset
        required: false
        type: int
      - default: 100
        help: Recent maps to aggregate from the current page (max 100)
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
    player-matches:
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
      - default: 3741/niko
        help: 'Player ref: 3741/niko, player URL, or stats matches URL'
        name: player
        required: false
        type: string
      - default: all
        help: all / lastMonth / last3Months / last6Months / last12Months / YYYY / YYYY-MM-DD:YYYY-MM-DD
        name: period
        required: false
        type: string
      - default: all
        help: all / majors / bigEvents / mvpEvents / lan / online
        name: eventType
        required: false
        type: string
      - default: all
        help: all / top5 / top10 / top20 / top30 / top50
        name: ranking
        required: false
        type: string
      - default: all
        help: all / ancient / anubis / dust2 / inferno / mirage / nuke / overpass / cache / cobblestone / season / train / tuscan / vertigo
        name: map
        required: false
        type: string
      - default: both
        help: both / cs2 / csgo
        name: version
        required: false
        type: string
      - default: 0
        help: Pagination offset; must be a multiple of 100
        name: offset
        required: false
        type: int
      - default: 100
        help: Rows to return from the current page (max 100)
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
    player-summary:
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
      - default: 3741/niko
        help: 'Player ref: 3741/niko or https://www.hltv.org/player/3741/niko'
        name: player
        required: false
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    player-teammate-impact:
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
      - help: Primary player ref
        name: playerA
        positional: true
        required: true
        type: string
      - help: Teammate player ref
        name: playerB
        positional: true
        required: true
        type: string
      - default: all
        help: all / lastMonth / last3Months / last6Months / last12Months / YYYY / YYYY-MM-DD:YYYY-MM-DD
        name: period
        required: false
        type: string
      - default: all
        help: all / majors / bigEvents / mvpEvents / lan / online
        name: eventType
        required: false
        type: string
      - default: all
        help: all / event id / /events/:id URL / stats URL with event=
        name: event
        required: false
        type: string
      - default: all
        help: all / top5 / top10 / top20 / top30 / top50
        name: ranking
        required: false
        type: string
      - default: all
        help: all / ancient / anubis / dust2 / inferno / mirage / nuke / overpass / cache / cobblestone / season / train / tuscan / vertigo
        name: map
        required: false
        type: string
      - default: both
        help: both / cs2 / csgo
        name: version
        required: false
        type: string
      - default: 0
        help: Pagination offset; must be a multiple of 100
        name: offset
        required: false
        type: int
      - default: 100
        help: Rows to scan for each player from the current page (max 100)
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
    player-vs-team:
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
      - default: 3741/niko
        help: 'Player ref: 3741/niko, player URL, or stats player URL'
        name: player
        required: false
        type: string
      - help: 'Team ref: 7020/spirit, team URL, or stats team URL'
        name: team
        positional: true
        required: true
        type: string
      - default: all
        help: all / lastMonth / last3Months / last6Months / last12Months / YYYY / YYYY-MM-DD:YYYY-MM-DD
        name: period
        required: false
        type: string
      - default: all
        help: all / majors / bigEvents / mvpEvents / lan / online
        name: eventType
        required: false
        type: string
      - default: all
        help: all / event id / /events/:id URL / stats URL with event=
        name: event
        required: false
        type: string
      - default: all
        help: all / top5 / top10 / top20 / top30 / top50
        name: ranking
        required: false
        type: string
      - default: all
        help: all / ancient / anubis / dust2 / inferno / mirage / nuke / overpass / cache / cobblestone / season / train / tuscan / vertigo
        name: map
        required: false
        type: string
      - default: both
        help: both / cs2 / csgo
        name: version
        required: false
        type: string
      - default: 0
        help: Pagination offset; must be a multiple of 100
        name: offset
        required: false
        type: int
      - default: 100
        help: Rows to scan from the current page (max 100)
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
    team-map-pool:
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
      - help: 'Team ref: 11283/falcons, team URL, or stats team URL'
        name: team
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
    team-matches:
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
      - help: 'Team ref: 6667/falcons, team URL, or stats team URL'
        name: team
        positional: true
        required: true
        type: string
      - default: all
        help: all / lastMonth / last3Months / last6Months / last12Months / YYYY / YYYY-MM-DD:YYYY-MM-DD
        name: period
        required: false
        type: string
      - default: all
        help: all / majors / bigEvents / mvpEvents / lan / online
        name: eventType
        required: false
        type: string
      - default: all
        help: all / event id / /events/:id URL / stats URL with event=
        name: event
        required: false
        type: string
      - default: all
        help: all / top5 / top10 / top20 / top30 / top50
        name: ranking
        required: false
        type: string
      - default: all
        help: all / ancient / anubis / dust2 / inferno / mirage / nuke / overpass / cache / cobblestone / season / train / tuscan / vertigo
        name: map
        required: false
        type: string
      - default: both
        help: both / cs2 / csgo
        name: version
        required: false
        type: string
      - default: 0
        help: Pagination offset; must be a multiple of 100
        name: offset
        required: false
        type: int
      - default: 100
        help: Rows to return from the current page (max 100)
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

# Hltv: analytics

Read aggregate metrics, trends, or rankings.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `event-matches` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Read visible HLTV stats match rows for a specific event | `event` (string, required, positional); `limit` (int, optional, default=100) |
| `match-map` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Read a single HLTV mapstats page and return all player rows for that map | `match` (string, required, positional) |
| `match-series` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Expand an HLTV match or stats series into summary, map, and player rows | `match` (string, required, positional) |
| `player-duel` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Compare two HLTV players on shared maps, including direct kill matrix when available | `playerA` (string, required, positional); `playerB` (string, required, positional); `match` (string, optional, default=''); `mode` (string, optional, default='lastEncounter'); `period` (string, optional, default='all'); `eventType` (string, optional, default='all'); `event` (string, optional, default='all'); `ranking` (string, optional, default='all'); `map` (string, optional, default='all'); `version` (string, optional, default='both'); `offset` (int, optional, default=0); `recentMaps` (int, optional, default=100); `scanPages` (int, optional, default=1); `limit` (int, optional, default=20) |
| `player-form` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Aggregate recent HLTV player maps into form summaries grouped by summary, map, and opponent | `player` (string, optional, default='3741/niko'); `period` (string, optional, default='all'); `eventType` (string, optional, default='all'); `ranking` (string, optional, default='all'); `map` (string, optional, default='all'); `version` (string, optional, default='both'); `offset` (int, optional, default=0); `limit` (int, optional, default=30) |
| `player-map-pool` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Aggregate a player matches page into per-map performance buckets | `player` (string, optional, default='3741/niko'); `period` (string, optional, default='all'); `eventType` (string, optional, default='all'); `event` (string, optional, default='all'); `ranking` (string, optional, default='all'); `map` (string, optional, default='all'); `version` (string, optional, default='both'); `offset` (int, optional, default=0); `limit` (int, optional, default=100) |
| `player-matches` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Read HLTV player match history from the stats Matches tab | `player` (string, optional, default='3741/niko'); `period` (string, optional, default='all'); `eventType` (string, optional, default='all'); `ranking` (string, optional, default='all'); `map` (string, optional, default='all'); `version` (string, optional, default='both'); `offset` (int, optional, default=0); `limit` (int, optional, default=100) |
| `player-summary` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Read an HLTV player summary page | `player` (string, optional, default='3741/niko') |
| `player-teammate-impact` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Compare playerA maps with and without playerB present in the scanned sample | `playerA` (string, required, positional); `playerB` (string, required, positional); `period` (string, optional, default='all'); `eventType` (string, optional, default='all'); `event` (string, optional, default='all'); `ranking` (string, optional, default='all'); `map` (string, optional, default='all'); `version` (string, optional, default='both'); `offset` (int, optional, default=0); `limit` (int, optional, default=100) |
| `player-vs-team` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Filter a player matches page to maps played against a specific HLTV team | `player` (string, optional, default='3741/niko'); `team` (string, required, positional); `period` (string, optional, default='all'); `eventType` (string, optional, default='all'); `event` (string, optional, default='all'); `ranking` (string, optional, default='all'); `map` (string, optional, default='all'); `version` (string, optional, default='both'); `offset` (int, optional, default=0); `limit` (int, optional, default=100) |
| `team-map-pool` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Read the visible HLTV team map-pool page with win rate, pick rate, and ban rate | `team` (string, required, positional) |
| `team-matches` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Read recent HLTV team map results from the stats team matches page | `team` (string, required, positional); `period` (string, optional, default='all'); `eventType` (string, optional, default='all'); `event` (string, optional, default='all'); `ranking` (string, optional, default='all'); `map` (string, optional, default='all'); `version` (string, optional, default='both'); `offset` (int, optional, default=0); `limit` (int, optional, default=100) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
