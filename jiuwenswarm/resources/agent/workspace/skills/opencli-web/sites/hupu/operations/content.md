---
opencli_contract:
  version: 2
  site: hupu
  operation: content
  policy_sha256: 86a3ddfcf16b3fc55407f3ac6dca5cc09098caa7777218d355d2b7e11cea3261
  commands:
    detail:
      executor: browser_manifest_public_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: 帖子ID（9位数字）
        name: tid
        positional: true
        required: true
        type: str
      - default: false
        help: 是否包含热门回复
        name: replies
        required: false
        type: boolean
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Hupu: content

Read one public item, record, page, or resource.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `detail` | `enabled` | `public_read` / `low` | `opencli_execute(site="hupu", operation="content", command="detail", arguments={"tid":"<tid>"})`<br>获取虎扑帖子详情 (使用Next.js JSON数据) | `tid` (str, required, positional); `replies` (boolean, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
