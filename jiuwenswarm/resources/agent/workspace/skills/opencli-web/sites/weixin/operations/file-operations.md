---
opencli_contract:
  version: 2
  site: weixin
  operation: file-operations
  policy_sha256: 4ae15f5bbeb75a3b75bca630d6636e358ee66ade40db74e20828f65545a93601
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
      - help: WeChat article URL (mp.weixin.qq.com/s/xxx)
        name: url
        required: true
        type: str
      - default: ./weixin-articles
        help: Output directory
        name: output
        required: false
        type: str
      - default: true
        help: Download images locally
        name: download-images
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs:
      - workspace-relative output
      sensitive_output: []
---

# Weixin: file-operations

Create or download workspace files.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `download` | `disabled` | `local_write` / `high` | Not executable; use the declared fallback if permitted<br>下载微信公众号文章为 Markdown 格式 | `url` (str, required); `output` (str, optional, default='./weixin-articles'); `download-images` (boolean, optional, default=True) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
