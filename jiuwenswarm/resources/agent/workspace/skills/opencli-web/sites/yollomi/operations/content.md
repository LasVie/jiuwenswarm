---
opencli_contract:
  version: 2
  site: yollomi
  operation: content
  policy_sha256: 1dc5c27c1c16b3f548734e283e44fae66c638a89c782d30389c972cf85f73d20
  commands:
    models:
      executor: none
      execution_state: disabled
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
      confirmation: unsupported
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
| `models` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>List available Yollomi AI models (image, video, tools) | `type` (str, optional, default='all', choices=all,image,video,tool) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
