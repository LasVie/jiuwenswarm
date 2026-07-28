---
opencli_contract:
  version: 2
  site: archive
  operation: discovery
  policy_sha256: f1d3b75584e23215c6623efc6fa3acef8c524be933a547aca5a6ca3623d0273b
  commands:
    search:
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
      - help: Full-text query (matches title, description, creator, subject).
        name: query
        positional: true
        required: true
        type: str
      - help: 'Restrict to mediatype: texts, movies, audio, software, image, web, data, collection'
        name: mediatype
        required: false
        type: string
      - default: downloads
        help: 'Sort key: downloads, date, addeddate, week, title'
        name: sort
        required: false
        type: string
      - default: 20
        help: Max items (max 100; one API page).
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

# Archive: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="archive", operation="discovery", command="search", arguments={"query":"<query>"})`<br>Search Internet Archive items across books, movies, audio, software, and web. | `query` (str, required, positional); `mediatype` (string, optional); `sort` (string, optional, default='downloads'); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
