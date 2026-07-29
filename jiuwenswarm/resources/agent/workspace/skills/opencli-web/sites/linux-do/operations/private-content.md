---
opencli_contract:
  version: 2
  site: linux-do
  operation: private-content
  policy_sha256: cc2e02c6a9d1c322af5f087ca9458e5beda0949cc685cd56fa744162f7655b8a
  commands:
    feed:
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
        - latest
        - hot
        - top
        default: latest
        help: View type
        name: view
        required: false
        type: str
      - help: Tag name, slug, or id
        name: tag
        required: false
        type: str
      - help: Category name, slug, id, or parent/name path
        name: category
        required: false
        type: str
      - default: 20
        help: Number of items (per_page)
        name: limit
        required: false
        type: int
      - choices:
        - default
        - created
        - activity
        - views
        - posts
        - category
        - likes
        - op_likes
        - posters
        default: default
        help: Sort order
        name: order
        required: false
        type: str
      - default: false
        help: 'Sort ascending (default: desc)'
        name: ascending
        required: false
        type: boolean
      - choices:
        - all
        - daily
        - weekly
        - monthly
        - quarterly
        - yearly
        help: Time period (only for --view top)
        name: period
        required: false
        type: str
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

# Linux Do: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `feed` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>linux.do 话题列表（需登录；支持全站、标签、分类） | `view` (str, optional, default='latest', choices=latest,hot,top); `tag` (str, optional); `category` (str, optional); `limit` (int, optional, default=20); `order` (str, optional, default='default', choices=default,created,activity,views,posts,category,likes,op_likes,posters); `ascending` (boolean, optional, default=False); `period` (str, optional, choices=all,daily,weekly,monthly,quarterly,yearly) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
