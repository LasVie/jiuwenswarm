---
opencli_contract:
  version: 2
  site: wechat-channels
  operation: publishing
  policy_sha256: c4b4628502a825d7985b67a354f5b7a1631a037bffddb3e7e883e4b552e81a0c
  commands:
    publish:
      executor: none
      execution_state: disabled
      semantic_effect: public_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: 视频文件路径 (.mp4/.mov/.avi/.webm)
        name: video
        positional: true
        required: true
        type: str
      - help: 短标题（建议 6-16 字）
        name: title
        required: false
        type: str
      - help: '描述内容，支持直接写 #话题（如：日常生活 #搞笑 #生活）'
        name: caption
        required: false
        type: str
      - help: 定时发布时间（ISO8601 或 Unix 秒，如 "2026-05-20 10:00"）
        name: schedule
        required: false
        type: str
      - default: false
        help: 保存为草稿
        name: draft
        required: false
        type: bool
      - default: false
        help: 填完所有字段后不自动发布，由用户手动点击发表（务必同时传 --site-session persistent，否则表单页约 30 秒后会被重置为空白页）
        name: manual
        required: false
        type: bool
      - default: 600
        help: 命令整体超时秒数（含登录等待 + 上传转码，默认 600）
        name: timeout
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs:
      - workspace-relative input when declared by adapter
      file_outputs: []
      sensitive_output: []
---

# Wechat Channels: publishing

Publish, create, edit, or upload remote content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `publish` | `disabled` | `public_write` / `high` | Not executable; use the declared fallback if permitted<br>发布视频到视频号 | `video` (str, required, positional); `title` (str, optional); `caption` (str, optional); `schedule` (str, optional); `draft` (bool, optional, default=False); `manual` (bool, optional, default=False); `timeout` (int, optional, default=600) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
