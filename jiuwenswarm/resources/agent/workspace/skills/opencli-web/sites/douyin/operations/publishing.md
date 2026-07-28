---
opencli_contract:
  version: 2
  site: douyin
  operation: publishing
  policy_sha256: bbec24521923ebb1327087b643f716d80cb93cb1c91f88100687c2f3854de22e
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
      - help: 视频文件路径
        name: video
        positional: true
        required: true
        type: str
      - help: 视频标题（≤30字）
        name: title
        required: true
        type: str
      - help: 定时发布时间（ISO8601 或 Unix 秒，2h ~ 14天后）
        name: schedule
        required: true
        type: str
      - default: ''
        help: '正文内容（≤1000字，支持 #话题）'
        name: caption
        required: false
        type: str
      - default: ''
        help: 封面图片路径（不提供时使用视频截帧）
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
      - default: false
        help: 允许下载
        name: allow_download
        required: false
        type: bool
      - default: ''
        help: 合集 ID
        name: collection
        required: false
        type: str
      - default: ''
        help: 活动 ID
        name: activity
        required: false
        type: str
      - default: ''
        help: 地理位置 ID
        name: poi_id
        required: false
        type: str
      - default: ''
        help: 地理位置名称
        name: poi_name
        required: false
        type: str
      - default: ''
        help: 关联热点词
        name: hotspot
        required: false
        type: str
      - default: false
        help: 跳过内容安全检测
        name: no_safety_check
        required: false
        type: bool
      - default: false
        help: 同步发布到头条
        name: sync_toutiao
        required: false
        type: bool
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs:
      - workspace-relative input when declared by adapter
      file_outputs: []
      sensitive_output: []
    update:
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
      - help: 抖音作品 ID（aweme_id，可从作品 URL 末尾获取）
        name: aweme_id
        positional: true
        required: true
        type: str
      - default: ''
        help: 新的发布时间（ISO8601 或 Unix 秒）
        name: reschedule
        required: false
        type: str
      - default: ''
        help: 新的正文内容
        name: caption
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs:
      - workspace-relative input when declared by adapter
      file_outputs: []
      sensitive_output: []
---

# Douyin: publishing

Publish, create, edit, or upload remote content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `publish` | `disabled` | `public_write` / `high` | Not executable; use the declared fallback if permitted<br>定时发布视频到抖音（必须设置 2h ~ 14天后的发布时间） | `video` (str, required, positional); `title` (str, required); `schedule` (str, required); `caption` (str, optional, default=''); `cover` (str, optional, default=''); `visibility` (str, optional, default='public', choices=public,friends,private); `allow_download` (bool, optional, default=False); `collection` (str, optional, default=''); `activity` (str, optional, default=''); `poi_id` (str, optional, default=''); `poi_name` (str, optional, default=''); `hotspot` (str, optional, default=''); `no_safety_check` (bool, optional, default=False); `sync_toutiao` (bool, optional, default=False) |
| `update` | `disabled` | `public_write` / `high` | Not executable; use the declared fallback if permitted<br>更新视频信息 | `aweme_id` (str, required, positional); `reschedule` (str, optional, default=''); `caption` (str, optional, default='') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
