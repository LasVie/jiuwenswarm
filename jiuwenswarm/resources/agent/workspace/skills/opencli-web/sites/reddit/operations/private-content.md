---
opencli_contract:
  version: 2
  site: reddit
  operation: private-content
  policy_sha256: 0487426fd966b3a96ccef136af5816f03b5ade5e203ef9e262e722a48273f258
  commands:
    frontpage:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 15
        help: ''
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    home:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 25
        help: Number of posts (1–100)
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    hot:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: ''
        help: Subreddit name (e.g. programming). Empty for frontpage
        name: subreddit
        required: false
        type: str
      - default: 20
        help: Number of posts
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    popular:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: ''
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    read:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Post ID (e.g. 1abc123) or full URL
        name: post-id
        positional: true
        required: true
        type: str
      - default: best
        help: 'Comment sort: best, top, new, controversial, old, qa'
        name: sort
        required: false
        type: str
      - default: 25
        help: Number of top-level comments
        name: limit
        required: false
        type: int
      - default: 2
        help: Max reply depth (1=no replies, 2=one level of replies, etc.)
        name: depth
        required: false
        type: int
      - default: 5
        help: Max replies shown per comment at each level (sorted by score)
        name: replies
        required: false
        type: int
      - default: 2000
        help: Max characters per comment body (min 100)
        name: max-length
        required: false
        type: int
      - default: false
        help: Follow Reddit "more comments" stubs by calling /api/morechildren.json
        name: expand-more
        required: false
        type: bool
      - default: 2
        help: Max expansion passes when --expand-more is on (1–5; each round can fan out new "more" stubs)
        name: expand-rounds
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    saved:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 15
        help: ''
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    search:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Reddit search query
        name: query
        positional: true
        required: true
        type: string
      - default: ''
        help: Search within a specific subreddit
        name: subreddit
        required: false
        type: string
      - default: relevance
        help: 'Sort order: relevance, hot, top, new, comments'
        name: sort
        required: false
        type: string
      - default: all
        help: 'Time filter: hour, day, week, month, year, all'
        name: time
        required: false
        type: string
      - default: 15
        help: ''
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    subreddit:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Subreddit name (no `r/` prefix; e.g. `python`)
        name: name
        positional: true
        required: true
        type: string
      - default: hot
        help: 'Sorting method: hot, new, top, rising, controversial'
        name: sort
        required: false
        type: string
      - default: all
        help: 'Time filter for top/controversial: hour, day, week, month, year, all'
        name: time
        required: false
        type: string
      - default: 15
        help: ''
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    subreddit-info:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Subreddit name (no `r/` prefix needed)
        name: name
        positional: true
        required: true
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    subscribed:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 100
        help: Max subreddits to return (1-1000, auto-paginates)
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    upvoted:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 15
        help: ''
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    user:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Reddit username (no `u/` prefix needed)
        name: username
        positional: true
        required: true
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    user-comments:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Reddit username (no `u/` prefix needed)
        name: username
        positional: true
        required: true
        type: string
      - default: 15
        help: ''
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    user-posts:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Reddit username (no `u/` prefix needed)
        name: username
        positional: true
        required: true
        type: string
      - default: 15
        help: ''
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
---

# Reddit: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `frontpage` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Reddit Frontpage / r/all | `limit` (int, optional, default=15) |
| `home` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Reddit personalized home feed (Best, requires login) | `limit` (int, optional, default=25) |
| `hot` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Reddit 热门帖子 | `subreddit` (str, optional, default=''); `limit` (int, optional, default=20) |
| `popular` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Reddit Popular posts (/r/popular) | `limit` (int, optional, default=20) |
| `read` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read a Reddit post and its comments | `post-id` (str, required, positional); `sort` (str, optional, default='best'); `limit` (int, optional, default=25); `depth` (int, optional, default=2); `replies` (int, optional, default=5); `max-length` (int, optional, default=2000); `expand-more` (bool, optional, default=False); `expand-rounds` (int, optional, default=2) |
| `saved` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Browse your saved Reddit posts | `limit` (int, optional, default=15) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Search Reddit Posts | `query` (string, required, positional); `subreddit` (string, optional, default=''); `sort` (string, optional, default='relevance'); `time` (string, optional, default='all'); `limit` (int, optional, default=15) |
| `subreddit` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get posts from a specific Subreddit | `name` (string, required, positional); `sort` (string, optional, default='hot'); `time` (string, optional, default='all'); `limit` (int, optional, default=15) |
| `subreddit-info` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Show metadata for a Reddit subreddit (subscribers, description, created date, NSFW) | `name` (string, required, positional) |
| `subscribed` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List subreddits you are subscribed to | `limit` (int, optional, default=100) |
| `upvoted` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Browse your upvoted Reddit posts | `limit` (int, optional, default=15) |
| `user` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>View a Reddit user profile | `username` (string, required, positional) |
| `user-comments` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>View a Reddit user's comment history | `username` (string, required, positional); `limit` (int, optional, default=15) |
| `user-posts` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>View a Reddit user's submitted posts | `username` (string, required, positional); `limit` (int, optional, default=15) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
