---
opencli_contract:
  version: 2
  site: twitter
  operation: content
  policy_sha256: ea1c61e10694164a7221301d4eb1fd14fec218da88d65957161ff72d1a564726
  commands:
    article:
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
      - help: Tweet ID or URL containing the article
        name: tweet-id
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
    profile:
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
      - help: Twitter screen name (with or without @). Defaults to the logged-in user when omitted.
        name: username
        positional: true
        required: false
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    thread:
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
      - help: Tweet numeric ID (e.g. 1234567890) or full status URL
        name: tweet-id
        positional: true
        required: true
        type: string
      - default: 50
        help: ''
        name: limit
        required: false
        type: int
      - default: 0
        help: When set to N>0, re-rank the thread by weighted engagement (likes×1 + retweets×3 + replies×2 + bookmarks×5 + log10(views+1)×0.5) and return the top N. Default 0 keeps the conversation's structural ordering.
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
    tweets:
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
      - help: Twitter screen name (with or without @). Defaults to the logged-in user when omitted.
        name: username
        positional: true
        required: false
        type: string
      - default: 20
        help: Max tweets to return (1-10000; fetched across cursor pages)
        name: limit
        required: false
        type: int
      - default: 2
        help: Seconds to wait between paginated timeline requests to reduce rate-limit risk. Use 0 to disable.
        name: page-delay
        required: false
        type: int
      - default: 0
        help: When set to N>0, re-rank the tweets by weighted engagement (likes×1 + retweets×3 + replies×2 + bookmarks×5 + log10(views+1)×0.5) and return the top N. Default 0 keeps the chronological ordering.
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
---

# Twitter: content

Read one public item, record, page, or resource.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `article` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Fetch a Twitter Article (long-form content) and export as Markdown | `tweet-id` (string, required, positional) |
| `profile` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Fetch a Twitter user profile — bio, stats, etc. (defaults to the logged-in user when no username is given) | `username` (string, optional, positional) |
| `thread` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Get a tweet thread (original + all replies) | `tweet-id` (string, required, positional); `limit` (int, optional, default=50); `top-by-engagement` (int, optional, default=0) |
| `tweets` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Fetch a Twitter user's most recent tweets (chronological, excludes pinned; defaults to the logged-in user when no username is given) | `username` (string, optional, positional); `limit` (int, optional, default=20); `page-delay` (int, optional, default=2); `top-by-engagement` (int, optional, default=0) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
