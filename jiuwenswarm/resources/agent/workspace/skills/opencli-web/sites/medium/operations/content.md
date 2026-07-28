---
opencli_contract:
  version: 2
  site: medium
  operation: content
  policy_sha256: c654ec10f2f7132724c538d77ffe77a2570004b4b119220d9f409705d799e50d
  commands:
    tag:
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
      - help: Lowercase tag slug (e.g. "programming", "machine-learning")
        name: tag
        positional: true
        required: true
        type: str
      - default: 20
        help: Max articles (1-25 — single RSS page)
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
---

# Medium: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `tag` | `enabled` | `public_read` / `low` | `opencli_execute(site="medium", operation="content", command="tag", arguments={"tag":"<tag>"})`<br>Latest Medium articles tagged with a given keyword (RSS feed) | `tag` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
