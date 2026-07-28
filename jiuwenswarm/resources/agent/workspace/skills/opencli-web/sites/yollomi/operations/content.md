---
opencli_contract:
  version: 2
  site: yollomi
  operation: content
  policy_sha256: 29c712a7ecebc308bdeab47ef374b43b0b015ee9cd287061fae1d4606f8f481f
  commands:
    models:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: local
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - choices:
        - all
        - image
        - video
        - tool
        default: all
        help: Filter by model type
        name: type
        required: false
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Yollomi: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `models` | `enabled` | `public_read` / `low` | `opencli_execute(site="yollomi", operation="content", command="models")`<br>List available Yollomi AI models (image, video, tools) | `type` (str, optional, default='all', choices=all,image,video,tool) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
