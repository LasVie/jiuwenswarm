---
opencli_contract:
  version: 2
  site: xianyu
  operation: publishing
  policy_sha256: ebd8a84d1da58f221ddd26e7f2067415e1c69f404feaca2ac7f9fa2b790beecc
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
      - help: 商品标题
        name: title
        positional: true
        required: true
        type: str
      - help: 商品描述/详情
        name: description
        positional: true
        required: true
        type: str
      - help: 出售价格（元）
        name: price
        positional: true
        required: true
        type: float
      - help: 成色：全新 / 几乎全新 / 轻微使用 / 明显使用 / 老旧
        name: condition
        positional: true
        required: true
        type: str
      - help: 商品分类关键词（如：手机、衣服、图书）
        name: category
        positional: true
        required: true
        type: str
      - help: 原价（选填，用于显示折扣）
        name: original_price
        required: false
        type: float
      - help: 所在地区（选填，如：杭州）
        name: location
        required: false
        type: str
      - help: 本地图片路径，多张用逗号分隔（选填，如：/tmp/a.jpg,/tmp/b.jpg）
        name: images
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

# Xianyu: publishing

Publish, create, edit, or upload remote content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `publish` | `disabled` | `public_write` / `high` | Not executable; use the declared fallback if permitted<br>发布闲鱼宝贝（需先在浏览器中登录闲鱼） | `title` (str, required, positional); `description` (str, required, positional); `price` (float, required, positional); `condition` (str, required, positional); `category` (str, required, positional); `original_price` (float, optional); `location` (str, optional); `images` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
