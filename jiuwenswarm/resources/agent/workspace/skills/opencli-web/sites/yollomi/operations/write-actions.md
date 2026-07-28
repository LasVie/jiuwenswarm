---
opencli_contract:
  version: 2
  site: yollomi
  operation: write-actions
  policy_sha256: ee2545bccbf6c52893001c0918b7503f043bcac13306e93647f8fc8ce9b8d5e2
  commands:
    background:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Image URL (upload via "opencli yollomi upload" first)
        name: image
        positional: true
        required: true
        type: str
      - default: ''
        help: Background description (optional)
        name: prompt
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
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    face-swap:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Source face image URL
        name: source
        required: true
        type: str
      - help: Target photo URL
        name: target
        required: true
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
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    object-remover:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Image URL
        name: image
        positional: true
        required: true
        type: str
      - help: Mask image URL (white = area to remove)
        name: mask
        positional: true
        required: true
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
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    restore:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Image URL to restore
        name: image
        positional: true
        required: true
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
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    try-on:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Person photo URL (upload via "opencli yollomi upload" first)
        name: person
        required: true
        type: str
      - help: Clothing image URL
        name: cloth
        required: true
        type: str
      - choices:
        - upper
        - lower
        - overall
        default: upper
        help: Clothing type
        name: cloth-type
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
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    upscale:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Image URL to upscale
        name: image
        positional: true
        required: true
        type: str
      - choices:
        - '2'
        - '4'
        default: '2'
        help: Upscale factor (2 or 4)
        name: scale
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
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    video:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Text prompt describing the video
        name: prompt
        positional: true
        required: true
        type: str
      - default: kling-2-1
        help: Model (kling-2-1, openai-sora-2, google-veo-3-1, wan-2-5-t2v, ...)
        name: model
        required: false
        type: str
      - help: Input image URL for image-to-video
        name: image
        required: false
        type: str
      - choices:
        - '1:1'
        - '16:9'
        - '9:16'
        - '4:3'
        - '3:4'
        default: '16:9'
        help: Aspect ratio
        name: ratio
        required: false
        type: str
      - default: ./yollomi-output
        help: Output directory
        name: output
        required: false
        type: str
      - default: false
        help: Only show URL, skip download
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

# Yollomi: write-actions

Change remote service state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `background` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Generate AI background for a product/object image (5 credits) | `image` (str, required, positional); `prompt` (str, optional, default=''); `output` (str, optional, default='./yollomi-output'); `no-download` (boolean, optional, default=False) |
| `face-swap` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Swap faces between two photos (3 credits) | `source` (str, required); `target` (str, required); `output` (str, optional, default='./yollomi-output'); `no-download` (boolean, optional, default=False) |
| `object-remover` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Remove unwanted objects from images (3 credits) | `image` (str, required, positional); `mask` (str, required, positional); `output` (str, optional, default='./yollomi-output'); `no-download` (boolean, optional, default=False) |
| `restore` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Restore old or damaged photos with AI (4 credits) | `image` (str, required, positional); `output` (str, optional, default='./yollomi-output'); `no-download` (boolean, optional, default=False) |
| `try-on` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Virtual try-on — see how clothes look on a person (3 credits) | `person` (str, required); `cloth` (str, required); `cloth-type` (str, optional, default='upper', choices=upper,lower,overall); `output` (str, optional, default='./yollomi-output'); `no-download` (boolean, optional, default=False) |
| `upscale` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Upscale image resolution with AI (1 credit) | `image` (str, required, positional); `scale` (str, optional, default='2', choices=2,4); `output` (str, optional, default='./yollomi-output'); `no-download` (boolean, optional, default=False) |
| `video` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Generate videos with AI (text-to-video or image-to-video) | `prompt` (str, required, positional); `model` (str, optional, default='kling-2-1'); `image` (str, optional); `ratio` (str, optional, default='16:9', choices=1:1,16:9,9:16,4:3,3:4); `output` (str, optional, default='./yollomi-output'); `no-download` (boolean, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
