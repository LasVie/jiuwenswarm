---
opencli_contract:
  version: 2
  site: twitter
  operation: discovery
  policy_sha256: ea1c61e10694164a7221301d4eb1fd14fec218da88d65957161ff72d1a564726
  commands:
    followers:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Twitter/X handle (with or without @). Omit to fetch followers of the currently logged-in account.
        name: user
        positional: true
        required: false
        type: string
      - default: 50
        help: Maximum number of follower rows to return (default 50). Must be a positive integer.
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
    following:
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
      - help: Twitter/X handle (with or without @). Omit to fetch the accounts the currently logged-in user follows.
        name: user
        positional: true
        required: false
        type: string
      - default: 50
        help: Maximum number of following rows to return (default 50). Must be a positive integer.
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
      - help: 'Search query. Raw X operators (e.g. "exact phrase", #tag, OR, lang:en, since:YYYY-MM-DD, from:, since:) are passed through unchanged.'
        name: query
        positional: true
        required: true
        type: string
      - choices:
        - top
        - live
        default: top
        help: Legacy alias for --product. Kept for backwards compatibility; if --product is set it wins.
        name: filter
        required: false
        type: string
      - choices:
        - top
        - live
        - photos
        - videos
        help: 'Which X search tab to read: top (default), live (Latest), photos, videos. Maps to the f= URL param.'
        name: product
        required: false
        type: string
      - help: Restrict to tweets authored by <user>. Leading @ is stripped. Equivalent to appending `from:<user>` to the query.
        name: from
        required: false
        type: string
      - choices:
        - media
        - images
        - videos
        - links
        - replies
        help: Restrict to tweets that have media|images|videos|links|replies. Maps to X's `filter:<has>` operator.
        name: has
        required: false
        type: string
      - choices:
        - replies
        - retweets
        - media
        - links
        help: 'Exclude tweets matching <type>: replies|retweets|media|links. Maps to X''s `-filter:<x>` operator (retweets → -filter:nativeretweets).'
        name: exclude
        required: false
        type: string
      - default: 15
        help: Maximum number of tweets to return (default 15). Result count after server-side filtering.
        name: limit
        required: false
        type: int
      - default: 0
        help: When set to N>0, re-rank the results by weighted engagement (likes×1 + retweets×3 + replies×2 + bookmarks×5 + log10(views+1)×0.5) and return the top N. Default 0 keeps X's native ordering.
        name: top-by-engagement
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    trending:
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
      - default: 20
        help: Number of trends to show
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

# Twitter: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `followers` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Get accounts following a Twitter/X user (defaults to the logged-in user when no user is given) | `user` (string, optional, positional); `limit` (int, optional, default=50) |
| `following` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Get accounts a Twitter/X user is following (defaults to the logged-in user when no user is given) | `user` (string, optional, positional); `limit` (int, optional, default=50) |
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Search Twitter/X for tweets, with optional --from / --has / --exclude / --product filters mapped to X's search operators | `query` (string, required, positional); `filter` (string, optional, default='top', choices=top,live); `product` (string, optional, choices=top,live,photos,videos); `from` (string, optional); `has` (string, optional, choices=media,images,videos,links,replies); `exclude` (string, optional, choices=replies,retweets,media,links); `limit` (int, optional, default=15); `top-by-engagement` (int, optional, default=0) |
| `trending` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Twitter/X trending topics | `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
