---
opencli_contract:
  version: 2
  site: 1point3acres
  operation: content
  policy_sha256: 0dbf244c9dd700c1aecb310892b943018ea6fe2ca7e725c441382de5c8b20b26
  commands:
    digest:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: 返回条数（默认 20，最多 50）
        name: limit
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    forum:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: 版块 ID，例如 145（海外面经）、198（海外职位内推）、27（研究生申请）
        name: fid
        positional: true
        required: true
        type: str
      - default: 1
        help: 页码（默认 1）
        name: page
        required: false
        type: int
      - default: 20
        help: 返回条数（默认 20，最多 50）
        name: limit
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    forums:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: ''
        help: 按版块名关键字过滤（子串匹配，中英文）
        name: filter
        required: false
        type: string
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    hot:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: 返回条数（默认 20，最多 50）
        name: limit
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    latest:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: 返回条数（默认 20，最多 50）
        name: limit
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    thread:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: 帖子 ID（数字，见 `hot`/`latest` 返回的 tid）
        name: tid
        positional: true
        required: true
        type: str
      - default: 1
        help: 楼层分页页码（默认 1）
        name: page
        required: false
        type: int
      - default: 10
        help: 返回楼层条数（默认 10，含主楼）
        name: limit
        required: false
        type: int
      - default: 400
        help: 每楼正文截断长度（默认 400 字符，最少 50）
        name: contentLimit
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    user:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: 用户名或 uid（纯数字按 uid 查，否则按用户名）
        name: who
        positional: true
        required: true
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# 1Point3Acres: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `digest` | `enabled` | `public_read` / `low` | `opencli_execute(site="1point3acres", operation="content", command="digest")`<br>一亩三分地 精华帖（编辑推荐 / 加精） | `limit` (int, optional, default=20) |
| `forum` | `enabled` | `public_read` / `low` | `opencli_execute(site="1point3acres", operation="content", command="forum", arguments={"fid":"<fid>"})`<br>浏览一亩三分地某个版块的帖子列表（按 fid） | `fid` (str, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=20) |
| `forums` | `enabled` | `public_read` / `low` | `opencli_execute(site="1point3acres", operation="content", command="forums")`<br>一亩三分地 所有版块（fid + 版块名） | `filter` (string, optional, default='') |
| `hot` | `enabled` | `public_read` / `low` | `opencli_execute(site="1point3acres", operation="content", command="hot")`<br>一亩三分地 今日热门帖子（按热度排序，约 50 条） | `limit` (int, optional, default=20) |
| `latest` | `enabled` | `public_read` / `low` | `opencli_execute(site="1point3acres", operation="content", command="latest")`<br>一亩三分地 最新发帖（按发帖时间倒序） | `limit` (int, optional, default=20) |
| `thread` | `enabled` | `public_read` / `low` | `opencli_execute(site="1point3acres", operation="content", command="thread", arguments={"tid":"<tid>"})`<br>一亩三分地 帖子详情 + 楼层（主楼 + 回复） | `tid` (str, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=10); `contentLimit` (int, optional, default=400) |
| `user` | `enabled` | `public_read` / `low` | `opencli_execute(site="1point3acres", operation="content", command="user", arguments={"who":"<who>"})`<br>一亩三分地 用户空间（用户组 / 积分 / 大米 / 帖子数 等） | `who` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
