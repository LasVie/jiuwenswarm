---
opencli_contract:
  version: 2
  site: twitter
  operation: file-operations
  policy_sha256: ea1c61e10694164a7221301d4eb1fd14fec218da88d65957161ff72d1a564726
  commands:
    download:
      executor: none
      execution_state: disabled
      semantic_effect: local_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Twitter username (with or without @) to scan their profile media. Either <username> or --tweet-url is required.
        name: username
        positional: true
        required: false
        type: str
      - help: Single tweet URL to download. Use this OR <username>, not both required at once.
        name: tweet-url
        required: false
        type: str
      - default: 10
        help: Maximum number of media items to download when scanning a profile (default 10). Ignored when --tweet-url is used.
        name: limit
        required: false
        type: int
      - default: ./twitter-downloads
        help: Output directory (default ./twitter-downloads). A per-source subdir is created inside.
        name: output
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs:
      - workspace-relative output
      sensitive_output: []
---

# Twitter: file-operations

Create or download workspace files.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `download` | `disabled` | `local_write` / `high` | Not executable; use the declared fallback if permitted<br>Download Twitter/X media (images and videos). Provide either <username> to fetch every media item from their profile via the GraphQL UserMedia endpoint with cursor pagination, or --tweet-url to download a single tweet. | `username` (str, optional, positional); `tweet-url` (str, optional); `limit` (int, optional, default=10); `output` (str, optional, default='./twitter-downloads') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
