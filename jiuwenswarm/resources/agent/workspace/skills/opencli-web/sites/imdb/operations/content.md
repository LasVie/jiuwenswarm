---
opencli_contract:
  version: 2
  site: imdb
  operation: content
  policy_sha256: 9bcc770927c80f736973e88ea56c2464aba627184a7b4c65f2bddeed6e566d90
  commands:
    person:
      executor: browser_manifest_public_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
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
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    reviews:
      executor: browser_manifest_public_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
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
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    title:
      executor: browser_manifest_public_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
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
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Imdb: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `person` | `enabled` | `public_read` / `low` | `opencli_execute(site="imdb", operation="content", command="person", arguments={"id":"<id>"})`<br>Get actor or director info | `id` (str, required, positional); `limit` (int, optional, default=10) |
| `reviews` | `enabled` | `public_read` / `low` | `opencli_execute(site="imdb", operation="content", command="reviews", arguments={"id":"<id>"})`<br>Get user reviews for a movie or TV show | `id` (str, required, positional); `limit` (int, optional, default=10) |
| `title` | `enabled` | `public_read` / `low` | `opencli_execute(site="imdb", operation="content", command="title", arguments={"id":"<id>"})`<br>Get movie or TV show details | `id` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
