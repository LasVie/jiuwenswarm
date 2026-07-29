---
opencli_contract:
  version: 2
  site: reddit
  operation: content
  policy_sha256: b899e066532b76d45800f057c889f9dfb932b03bd7979cb0b6f4ad4af9b71596
  commands:
    read:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    subreddit-info:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    user:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    user-comments:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    user-posts:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Reddit: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `read` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Read a Reddit post and its comments | `post-id` (str, required, positional); `sort` (str, optional, default='best'); `limit` (int, optional, default=25); `depth` (int, optional, default=2); `replies` (int, optional, default=5); `max-length` (int, optional, default=2000); `expand-more` (bool, optional, default=False); `expand-rounds` (int, optional, default=2) |
| `subreddit-info` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Show metadata for a Reddit subreddit (subscribers, description, created date, NSFW) | `name` (string, required, positional) |
| `user` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>View a Reddit user profile | `username` (string, required, positional) |
| `user-comments` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>View a Reddit user's comment history | `username` (string, required, positional); `limit` (int, optional, default=15) |
| `user-posts` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>View a Reddit user's submitted posts | `username` (string, required, positional); `limit` (int, optional, default=15) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
