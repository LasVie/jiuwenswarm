---
opencli_contract:
  version: 2
  site: 1point3acres
  operation: discovery
  policy_sha256: 871c4a0582d2a9bf05ea6523c54836f1e728460cf923a19b3a4fa75d73290221
  commands:
    search:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: 搜索关键字
        name: query
        positional: true
        required: true
        type: str
      - default: 20
        help: 返回条数（默认 20，最多 50）
        name: limit
        required: false
        type: int
      - default: ''
        help: 限定版块 ID（可选）
        name: fid
        required: false
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# 1Point3Acres: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>一亩三分地 站内关键字搜索（需要登录） | `query` (str, required, positional); `limit` (int, optional, default=20); `fid` (string, optional, default='') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
