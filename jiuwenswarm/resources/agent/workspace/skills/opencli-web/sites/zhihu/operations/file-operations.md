---
opencli_contract:
  version: 2
  site: zhihu
  operation: file-operations
  policy_sha256: 72cfde1a8e42b9be48a1414fe1c119c65782c8b4c07c241be09bd6fcad8a4929
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
      - help: Article URL (zhuanlan.zhihu.com/p/xxx)
        name: url
        required: true
        type: str
      - default: ./zhihu-articles
        help: Output directory
        name: output
        required: false
        type: str
      - default: false
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

# Zhihu: file-operations

Create or download workspace files.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `download` | `disabled` | `local_write` / `high` | Not executable; use the declared fallback if permitted<br>导出知乎文章为 Markdown 格式 | `url` (str, required); `output` (str, optional, default='./zhihu-articles'); `download-images` (boolean, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
