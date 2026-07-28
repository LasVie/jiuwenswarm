---
opencli_contract:
  version: 2
  site: yollomi
  operation: generation
  policy_sha256: 29c712a7ecebc308bdeab47ef374b43b0b015ee9cd287061fae1d4606f8f481f
  commands:
    generate:
      executor: none
      execution_state: disabled
      semantic_effect: quota_consumption
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Text prompt describing the image
        name: prompt
        positional: true
        required: true
        type: str
      - default: z-image-turbo
        help: Model ID (z-image-turbo, flux-schnell, nano-banana, flux-2-pro, ...)
        name: model
        required: false
        type: str
      - choices:
        - '1:1'
        - '16:9'
        - '9:16'
        - '4:3'
        - '3:4'
        default: '1:1'
        help: Aspect ratio
        name: ratio
        required: false
        type: str
      - help: Input image URL for image-to-image (upload via "opencli yollomi upload" first)
        name: image
        required: false
        type: str
      - default: ./yollomi-output
        help: Output directory
        name: output
        required: false
        type: str
      - default: false
        help: Only show URLs, skip download
        name: no-download
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Yollomi: generation

Generate remote content, start AI work, or consume quota.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `generate` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Generate images with AI (text-to-image or image-to-image) | `prompt` (str, required, positional); `model` (str, optional, default='z-image-turbo'); `ratio` (str, optional, default='1:1', choices=1:1,16:9,9:16,4:3,3:4); `image` (str, optional); `output` (str, optional, default='./yollomi-output'); `no-download` (boolean, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
