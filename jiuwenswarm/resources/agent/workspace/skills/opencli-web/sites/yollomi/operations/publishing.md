---
opencli_contract:
  version: 2
  site: yollomi
  operation: publishing
  policy_sha256: ee2545bccbf6c52893001c0918b7503f043bcac13306e93647f8fc8ce9b8d5e2
  commands:
    edit:
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
      - help: Input image URL (upload via "opencli yollomi upload" first)
        name: image
        positional: true
        required: true
        type: str
      - help: Editing instruction (e.g. "Make it look vintage")
        name: prompt
        positional: true
        required: true
        type: str
      - choices:
        - qwen-image-edit
        - qwen-image-edit-plus
        default: qwen-image-edit
        help: Edit model
        name: model
        required: false
        type: str
      - default: ./yollomi-output
        help: Output directory
        name: output
        required: false
        type: str
      - default: false
        help: Only show URL
        name: no-download
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs:
      - workspace-relative input when declared by adapter
      file_outputs: []
      sensitive_output: []
    upload:
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
      - help: Local file path to upload
        name: file
        positional: true
        required: true
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

# Yollomi: publishing

Publish, create, edit, or upload remote content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `edit` | `disabled` | `public_write` / `high` | Not executable; use the declared fallback if permitted<br>Edit images with AI text prompts (Qwen image edit) | `image` (str, required, positional); `prompt` (str, required, positional); `model` (str, optional, default='qwen-image-edit', choices=qwen-image-edit,qwen-image-edit-plus); `output` (str, optional, default='./yollomi-output'); `no-download` (boolean, optional, default=False) |
| `upload` | `disabled` | `public_write` / `high` | Not executable; use the declared fallback if permitted<br>Upload an image or video to Yollomi (returns URL for other commands) | `file` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
