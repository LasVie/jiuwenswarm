---
opencli_contract:
  version: 2
  site: imdb
  operation: private-content
  policy_sha256: fd083ca847a711a5c62480c3fc988891b0f0b26e47829d25dc0c04763f96b18b
  commands:
    person:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: IMDb person ID (nm0634240) or URL
        name: id
        positional: true
        required: true
        type: str
      - default: 10
        help: Max filmography entries
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    reviews:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: IMDb title ID (tt1375666) or URL
        name: id
        positional: true
        required: true
        type: str
      - default: 10
        help: Number of reviews
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    search:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Search query
        name: query
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of results
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    title:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: IMDb title ID (tt1375666) or URL
        name: id
        positional: true
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    top:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: Number of results
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    trending:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: Number of results
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
---

# Imdb: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `person` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get actor or director info | `id` (str, required, positional); `limit` (int, optional, default=10) |
| `reviews` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get user reviews for a movie or TV show | `id` (str, required, positional); `limit` (int, optional, default=10) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Search IMDb for movies, TV shows, and people | `query` (str, required, positional); `limit` (int, optional, default=20) |
| `title` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get movie or TV show details | `id` (str, required, positional) |
| `top` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>IMDb Top 250 Movies | `limit` (int, optional, default=20) |
| `trending` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>IMDb Most Popular Movies | `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
