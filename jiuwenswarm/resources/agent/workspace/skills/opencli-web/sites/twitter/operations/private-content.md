---
opencli_contract:
  version: 2
  site: twitter
  operation: private-content
  policy_sha256: d3dfdd9f50e334a4672153f072546b8d93fc2b4c68dc2786edab05aea347b96c
  commands:
    article:
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
      - help: Tweet ID or URL containing the article
        name: tweet-id
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
      - private content
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
      - private content
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
      - private content
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
      - private content
      - account identifiers
    followers:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
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
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    following:
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
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
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
      - private content
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
      - private content
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
      - private content
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
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    thread:
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
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
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
      - private content
      - account identifiers
    trending:
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
        help: Number of trends to show
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
    tweets:
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
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
---

# Twitter: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `article` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Fetch a Twitter Article (long-form content) and export as Markdown | `tweet-id` (string, required, positional) |
| `bookmark-folder` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read the tweets inside a single Twitter/X bookmark folder. Get the folder id from `opencli twitter bookmark-folders`. | `folder-id` (string, required, positional); `limit` (int, optional, default=20); `top-by-engagement` (int, optional, default=0) |
| `bookmark-folders` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List your Twitter/X bookmark folders (the user-created collections under Bookmarks). Returns folder id, name, item count, and created_at. | none |
| `bookmarks` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Fetch your Twitter/X bookmarks (the logged-in user's saved tweets, newest first) | `limit` (int, optional, default=20); `top-by-engagement` (int, optional, default=0) |
| `device-follow` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read the /i/timeline device-follow notification stream (tweets aggregated under a bell-icon "new posts from @userA and N others" notification) | `limit` (int, optional, default=20); `top-by-engagement` (int, optional, default=0) |
| `followers` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get accounts following a Twitter/X user (defaults to the logged-in user when no user is given) | `user` (string, optional, positional); `limit` (int, optional, default=50) |
| `following` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get accounts a Twitter/X user is following (defaults to the logged-in user when no user is given) | `user` (string, optional, positional); `limit` (int, optional, default=50) |
| `likes` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Fetch liked tweets of a Twitter user (defaults to the logged-in user when no username is given) | `username` (string, optional, positional); `limit` (int, optional, default=20); `top-by-engagement` (int, optional, default=0) |
| `list-tweets` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Fetch tweets from a Twitter/X list timeline | `listId` (string, required, positional); `limit` (int, optional, default=50); `top-by-engagement` (int, optional, default=0) |
| `lists` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get Twitter/X lists for the logged-in user (owned + subscribed) | `limit` (int, optional, default=50) |
| `notifications` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get your Twitter/X notifications (the logged-in user's likes/replies/follows feed, newest first) | `limit` (int, optional, default=20) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Search Twitter/X for tweets, with optional --from / --has / --exclude / --product filters mapped to X's search operators | `query` (string, required, positional); `filter` (string, optional, default='top', choices=top,live); `product` (string, optional, choices=top,live,photos,videos); `from` (string, optional); `has` (string, optional, choices=media,images,videos,links,replies); `exclude` (string, optional, choices=replies,retweets,media,links); `limit` (int, optional, default=15); `top-by-engagement` (int, optional, default=0) |
| `thread` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get a tweet thread (original + all replies) | `tweet-id` (string, required, positional); `limit` (int, optional, default=50); `top-by-engagement` (int, optional, default=0) |
| `timeline` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Fetch the logged-in user's home timeline (for-you algorithmic feed by default; pass --type following for the chronological feed of accounts you follow) | `type` (str, optional, default='for-you', choices=for-you,following); `limit` (int, optional, default=20); `top-by-engagement` (int, optional, default=0) |
| `trending` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Twitter/X trending topics | `limit` (int, optional, default=20) |
| `tweets` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Fetch a Twitter user's most recent tweets (chronological, excludes pinned; defaults to the logged-in user when no username is given) | `username` (string, optional, positional); `limit` (int, optional, default=20); `page-delay` (int, optional, default=2); `top-by-engagement` (int, optional, default=0) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
