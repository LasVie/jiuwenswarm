---
opencli_contract:
  version: 2
  site: xiaoe
  operation: private-content
  policy_sha256: 143c3ff1e3210598ea7c52f03a254c27c39c99031d104f9d37dda08e5294cf56
  commands:
    catalog:
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
      - help: 课程页面 URL
        name: url
        positional: true
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private course content
      - account identifiers
    content:
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
      - help: 页面 URL
        name: url
        positional: true
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private course content
      - account identifiers
    courses:
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
      - purchase history
      - account identifiers
    play-url:
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
      - help: 小节页面 URL
        name: url
        positional: true
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private course media URL
      - account identifiers
---

# Xiaoe: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `catalog` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>小鹅通课程目录（支持普通课程、专栏、大专栏） | `url` (str, required, positional) |
| `content` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>提取小鹅通图文页面内容为文本 | `url` (str, required, positional) |
| `courses` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>列出已购小鹅通课程（含 URL 和店铺名） | none |
| `play-url` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>小鹅通视频/音频/直播回放 M3U8 播放地址 | `url` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
