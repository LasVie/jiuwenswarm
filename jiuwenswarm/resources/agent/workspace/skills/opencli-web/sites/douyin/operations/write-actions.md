---
opencli_contract:
  version: 2
  site: douyin
  operation: write-actions
  policy_sha256: bbec24521923ebb1327087b643f716d80cb93cb1c91f88100687c2f3854de22e
  commands:
    draft:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: 视频文件路径
        name: video
        positional: true
        required: true
        type: str
      - help: 视频标题（≤30字）
        name: title
        required: true
        type: str
      - default: ''
        help: '正文内容（≤1000字，支持 #话题）'
        name: caption
        required: false
        type: str
      - default: ''
        help: 封面图片路径
        name: cover
        required: false
        type: str
      - choices:
        - public
        - friends
        - private
        default: public
        help: ''
        name: visibility
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Douyin: write-actions

Change remote service state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `draft` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>上传视频并保存为草稿 | `video` (str, required, positional); `title` (str, required); `caption` (str, optional, default=''); `cover` (str, optional, default=''); `visibility` (str, optional, default='public', choices=public,friends,private) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
