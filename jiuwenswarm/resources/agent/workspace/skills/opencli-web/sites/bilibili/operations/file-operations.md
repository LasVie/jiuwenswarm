---
opencli_contract:
  version: 2
  site: bilibili
  operation: file-operations
  policy_sha256: 6e8e73109dd43108bc96445fe5fb962e20e71bd5fabb4922fa485aa95e9accb6
  commands:
    download:
      executor: none
      execution_state: disabled
      semantic_effect: local_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Video BV ID (e.g., BV1xxx)
        name: bvid
        positional: true
        required: true
        type: str
      - default: ./bilibili-downloads
        help: Output directory
        name: output
        required: false
        type: str
      - default: best
        help: Video quality (best, 1080p, 720p, 480p)
        name: quality
        required: false
        type: str
      - default: false
        help: 跳过付费内容预检直接下载（已购买/已充电/已开通会员时用）
        name: force
        required: false
        type: boolean
      - help: 分P 选集序号（从 1 开始）。多 P 视频下载该集；缺省下载默认 P1
        name: page
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs:
      - workspace-relative output
      sensitive_output: []
---

# Bilibili: file-operations

Create or download workspace files.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `download` | `disabled` | `local_write` / `high` | Not executable; use the declared fallback if permitted<br>下载B站视频（需要 yt-dlp） | `bvid` (str, required, positional); `output` (str, optional, default='./bilibili-downloads'); `quality` (str, optional, default='best'); `force` (boolean, optional, default=False); `page` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
