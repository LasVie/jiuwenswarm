---
opencli_contract:
  version: 2
  site: mubu
  operation: private-content
  policy_sha256: 6534b6c3bc5f230ccd43aef6103de7cd2a12ebaa15c33ec788de606b9b876553
  commands:
    doc:
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
      - help: 文档 ID
        name: id
        positional: true
        required: true
        type: str
      - default: md
        help: 输出格式：md（默认，缩进列表 Markdown，适合导入 Obsidian）或 text（纯文本，适合终端阅读）
        name: output
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
    docs:
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
      - default: '0'
        help: 文件夹 ID（默认根目录 0）
        name: folder
        required: false
        type: str
      - default: false
        help: 只显示快速访问的文档和文件夹
        name: starred
        required: false
        type: bool
      - default: 50
        help: 最多显示条数
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    notes:
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
      - default: false
        help: 概览模式：只输出日期和条数，不含速记内容。可与任意时间范围参数组合。
        name: list
        required: false
        type: bool
      - help: 单日，格式 YYYY-MM-DD。不指定时间范围则默认今天（系统本地时间）。
        name: date
        required: false
        type: str
      - help: 整月，格式 YYYY-MM。
        name: month
        required: false
        type: str
      - help: 整年，格式 YYYY（整数）。
        name: year
        required: false
        type: int
      - help: 范围起始日，格式 YYYY-MM-DD。须与 --to 同时使用。
        name: from
        required: false
        type: str
      - help: 范围截止日，格式 YYYY-MM-DD。须与 --from 同时使用。
        name: to
        required: false
        type: str
      - default: md
        help: 输出格式：md（默认，Markdown）或 text（纯文本）
        name: output
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
    recent:
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
      - default: 20
        help: 最多显示条数
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    search:
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
      - help: 搜索关键词
        name: query
        positional: true
        required: true
        type: str
      - default: 100
        help: 最多显示条数（默认 100，结果被截断时用 --limit N 调大）
        name: limit
        required: false
        type: int
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

# Mubu: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `doc` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>读取幕布文档内容（默认输出 Markdown，可用 --output text 输出纯文本） | `id` (str, required, positional); `output` (str, optional, default='md') |
| `docs` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>列出幕布文档（默认根目录，--starred 查看快速访问列表） | `folder` (str, optional, default='0'); `starred` (bool, optional, default=False); `limit` (int, optional, default=50) |
| `notes` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>读取幕布速记（默认今天）。支持 --date/--month/--year/--from/--to 指定时间范围，--list 为概览模式（日期+条数）。 | `list` (bool, optional, default=False); `date` (str, optional); `month` (str, optional); `year` (int, optional); `from` (str, optional); `to` (str, optional); `output` (str, optional, default='md') |
| `recent` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>最近编辑的幕布文档 | `limit` (int, optional, default=20) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>全局搜索幕布文档和文件夹（标题+内容，服务端全量匹配）。结果含 type/id/name/path/hits/snippet 字段。 | `query` (str, required, positional); `limit` (int, optional, default=100) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
