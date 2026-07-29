---
opencli_contract:
  version: 2
  site: twitter
  operation: private-content
  policy_sha256: ea1c61e10694164a7221301d4eb1fd14fec218da88d65957161ff72d1a564726
  commands:
    bookmark-folder:
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
      - help: Folder id from `opencli twitter bookmark-folders`.
        name: folder-id
        positional: true
        required: true
        type: string
      - default: 20
        help: Maximum number of bookmarks to return (default 20).
        name: limit
        required: false
        type: int
      - default: 0
        help: When set to N>0, re-rank the folder by weighted engagement (likes×1 + retweets×3 + replies×2 + bookmarks×5 + log10(views+1)×0.5) and return the top N. Default 0 keeps the API's native (saved-time) ordering.
        name: top-by-engagement
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private social content
      - account identifiers
    bookmark-folders:
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
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private social content
      - account identifiers
    bookmarks:
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
        help: Maximum number of bookmarks to return (default 20).
        name: limit
        required: false
        type: int
      - default: 0
        help: When set to N>0, re-rank the bookmarks by weighted engagement (likes×1 + retweets×3 + replies×2 + bookmarks×5 + log10(views+1)×0.5) and return the top N. Default 0 keeps the API's native (saved-time) ordering.
        name: top-by-engagement
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private social content
      - account identifiers
    device-follow:
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
        help: Maximum number of tweets to return (1-200, default 20)
        name: limit
        required: false
        type: int
      - default: 0
        help: When set to N>0, re-rank by weighted engagement and return the top N. Default 0 keeps upstream ordering.
        name: top-by-engagement
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private social content
      - account identifiers
    likes:
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
      - help: Twitter screen name (with or without @). Defaults to the logged-in user when omitted.
        name: username
        positional: true
        required: false
        type: string
      - default: 20
        help: Maximum number of liked tweets to return (default 20).
        name: limit
        required: false
        type: int
      - default: 0
        help: When set to N>0, re-rank the liked tweets by weighted engagement (likes×1 + retweets×3 + replies×2 + bookmarks×5 + log10(views+1)×0.5) and return the top N. Default 0 keeps the API's native (recency) ordering.
        name: top-by-engagement
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private social content
      - account identifiers
    list-tweets:
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
      - help: Numeric ID of a Twitter/X list (e.g. from `opencli twitter lists`)
        name: listId
        positional: true
        required: true
        type: string
      - default: 50
        help: ''
        name: limit
        required: false
        type: int
      - default: 0
        help: When set to N>0, re-rank the list timeline by weighted engagement (likes×1 + retweets×3 + replies×2 + bookmarks×5 + log10(views+1)×0.5) and return the top N. Default 0 keeps the list's native (recency) ordering.
        name: top-by-engagement
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private social content
      - account identifiers
    lists:
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
      - default: 50
        help: Maximum number of lists to return (default 50).
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
      - private social content
      - account identifiers
    notifications:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_intercept
      strategy: intercept
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: Maximum number of notifications to return (default 20).
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
      - private social content
      - account identifiers
    timeline:
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
      - choices:
        - for-you
        - following
        default: for-you
        help: Which home-timeline feed to read. Default for-you (algorithmic). Use following for the chronological feed of accounts you follow.
        name: type
        required: false
        type: str
      - default: 20
        help: Maximum number of tweets to return (default 20).
        name: limit
        required: false
        type: int
      - default: 0
        help: When set to N>0, re-rank the timeline by weighted engagement (likes×1 + retweets×3 + replies×2 + bookmarks×5 + log10(views+1)×0.5) and return the top N. Default 0 keeps X's native ordering.
        name: top-by-engagement
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private social content
      - account identifiers
---

# Twitter: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `bookmark-folder` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read the tweets inside a single Twitter/X bookmark folder. Get the folder id from `opencli twitter bookmark-folders`. | `folder-id` (string, required, positional); `limit` (int, optional, default=20); `top-by-engagement` (int, optional, default=0) |
| `bookmark-folders` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List your Twitter/X bookmark folders (the user-created collections under Bookmarks). Returns folder id, name, item count, and created_at. | none |
| `bookmarks` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Fetch your Twitter/X bookmarks (the logged-in user's saved tweets, newest first) | `limit` (int, optional, default=20); `top-by-engagement` (int, optional, default=0) |
| `device-follow` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read the /i/timeline device-follow notification stream (tweets aggregated under a bell-icon "new posts from @userA and N others" notification) | `limit` (int, optional, default=20); `top-by-engagement` (int, optional, default=0) |
| `likes` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Fetch liked tweets of a Twitter user (defaults to the logged-in user when no username is given) | `username` (string, optional, positional); `limit` (int, optional, default=20); `top-by-engagement` (int, optional, default=0) |
| `list-tweets` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Fetch tweets from a Twitter/X list timeline | `listId` (string, required, positional); `limit` (int, optional, default=50); `top-by-engagement` (int, optional, default=0) |
| `lists` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get Twitter/X lists for the logged-in user (owned + subscribed) | `limit` (int, optional, default=50) |
| `notifications` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get your Twitter/X notifications (the logged-in user's likes/replies/follows feed, newest first) | `limit` (int, optional, default=20) |
| `timeline` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Fetch the logged-in user's home timeline (for-you algorithmic feed by default; pass --type following for the chronological feed of accounts you follow) | `type` (str, optional, default='for-you', choices=for-you,following); `limit` (int, optional, default=20); `top-by-engagement` (int, optional, default=0) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
