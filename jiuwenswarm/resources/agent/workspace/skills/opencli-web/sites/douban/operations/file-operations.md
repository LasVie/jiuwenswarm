---
opencli_contract:
  version: 2
  site: douban
  operation: file-operations
  policy_sha256: f2948e86776e79b572c3bb5f9dc2f05ec01adfcba950f4341f135f84b9933578
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
      - help: 电影 subject ID
        name: id
        positional: true
        required: true
        type: str
      - default: Rb
        help: 豆瓣 photos 的 type 参数，默认 Rb（海报）
        name: type
        required: false
        type: str
      - default: 120
        help: 最多下载多少张图片
        name: limit
        required: false
        type: int
      - help: 只下载指定 photo_id 的图片
        name: photo-id
        required: false
        type: str
      - default: ./douban-downloads
        help: 输出目录
        name: output
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

# Douban: file-operations

Create or download workspace files.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `download` | `disabled` | `local_write` / `high` | Not executable; use the declared fallback if permitted<br>下载电影海报/剧照图片 | `id` (str, required, positional); `type` (str, optional, default='Rb'); `limit` (int, optional, default=120); `photo-id` (str, optional); `output` (str, optional, default='./douban-downloads') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
