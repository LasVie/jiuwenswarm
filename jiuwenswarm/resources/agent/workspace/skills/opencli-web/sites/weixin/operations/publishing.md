---
opencli_contract:
  version: 2
  site: weixin
  operation: publishing
  policy_sha256: 81c0387fc9449bde1b851ade112157695e57b200fc5cdd0c45830aae2469f9af
  commands:
    create-draft:
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
      - help: 文章标题 (最长64字)
        name: title
        required: true
        type: str
      - help: 文章正文
        name: content
        positional: true
        required: true
        type: str
      - help: 作者名 (最长8字)
        name: author
        required: false
        type: str
      - help: 封面图片路径 (会先上传到正文再设为封面)
        name: cover-image
        required: false
        type: str
      - help: 文章摘要
        name: summary
        required: false
        type: str
      - default: 180
        help: 'Max seconds for the overall command (default: 180)'
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

# Weixin: publishing

Publish, create, edit, or upload remote content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `create-draft` | `disabled` | `public_write` / `high` | Not executable; use the declared fallback if permitted<br>创建微信公众号图文草稿 | `title` (str, required); `content` (str, required, positional); `author` (str, optional); `cover-image` (str, optional); `summary` (str, optional); `timeout` (int, optional, default=180) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
