---
opencli_contract:
  version: 2
  site: 51job
  operation: content
  policy_sha256: 2951d1b13f145eabdfdbdc2a92b34be6f1e48df005cc9472f539dab5ef41bcbd
  commands:
    company:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: 加密公司 ID（search 返回的 encCoId）
        name: encCoId
        positional: true
        required: true
        type: string
      - default: 20
        help: 返回职位数（1-50）
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    detail:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: 职位 ID（search 返回的 jobId）
        name: jobId
        positional: true
        required: true
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# 51Job: content

Read one public item, record, page, or resource.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `company` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>51job 公司简介 + 在招职位（按 encCoId） | `encCoId` (string, required, positional); `limit` (int, optional, default=20) |
| `detail` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>51job 职位详情（按 jobId） | `jobId` (string, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
