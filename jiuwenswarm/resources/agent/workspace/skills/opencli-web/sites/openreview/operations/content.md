---
opencli_contract:
  version: 2
  site: openreview
  operation: content
  policy_sha256: 096b115ccc93e419a9ef5dc5776b3179c3bbaceb07a04d5e78ab0bb9aee19b59
  commands:
    author:
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
      - help: OpenReview profile id (e.g. "~Yoshua_Bengio1"). Find it on the author profile URL on openreview.net.
        name: profile
        positional: true
        required: true
        type: str
      - default: 50
        help: Max submissions (1-1000)
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
    paper:
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
      - help: OpenReview note id (e.g. "5sRnsubyAK")
        name: id
        positional: true
        required: true
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    reviews:
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
      - help: OpenReview forum id (same as paper id)
        name: forum
        positional: true
        required: true
        type: str
      - default: 4000
        help: Per-row text truncation (min 200)
        name: max-length
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    venue:
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
      - help: Venue name ("ICLR 2024 oral") or invitation ("ICLR.cc/2025/Conference/-/Submission")
        name: venue
        positional: true
        required: true
        type: str
      - default: 25
        help: Max results (max 200)
        name: limit
        required: false
        type: int
      - default: 0
        help: Pagination offset
        name: offset
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

# Openreview: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `author` | `enabled` | `public_read` / `low` | `opencli_execute(site="openreview", operation="content", command="author", arguments={"profile":"<profile>"})`<br>List OpenReview submissions by an author profile id (newest first) | `profile` (str, required, positional); `limit` (int, optional, default=50) |
| `paper` | `enabled` | `public_read` / `low` | `opencli_execute(site="openreview", operation="content", command="paper", arguments={"id":"<id>"})`<br>Show full metadata for a single OpenReview paper | `id` (str, required, positional) |
| `reviews` | `enabled` | `public_read` / `low` | `opencli_execute(site="openreview", operation="content", command="reviews", arguments={"forum":"<forum>"})`<br>Show full review thread (paper + reviews + decisions) for an OpenReview forum | `forum` (str, required, positional); `max-length` (int, optional, default=4000) |
| `venue` | `enabled` | `public_read` / `low` | `opencli_execute(site="openreview", operation="content", command="venue", arguments={"venue":"<venue>"})`<br>List papers at an OpenReview venue (e.g. "ICLR 2024 oral" or full invitation id) | `venue` (str, required, positional); `limit` (int, optional, default=25); `offset` (int, optional, default=0) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
