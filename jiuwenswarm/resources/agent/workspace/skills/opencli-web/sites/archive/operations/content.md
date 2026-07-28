---
opencli_contract:
  version: 2
  site: archive
  operation: content
  policy_sha256: f1d3b75584e23215c6623efc6fa3acef8c524be933a547aca5a6ca3623d0273b
  commands:
    item:
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
      - help: Archive item identifier (e.g. "open-syllabus", "FinalFantasy2_356").
        name: identifier
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
    snapshots:
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
      - help: URL to look up (with or without scheme).
        name: url
        positional: true
        required: true
        type: str
      - help: Earliest year/timestamp (YYYY[MM[DD[hh[mm[ss]]]]])
        name: from
        required: false
        type: string
      - help: Latest year/timestamp (YYYY[MM[DD[hh[mm[ss]]]]])
        name: to
        required: false
        type: string
      - default: 20
        help: Max snapshots to return (max 1000).
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
    wayback:
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
      - help: URL to look up (with or without scheme).
        name: url
        positional: true
        required: true
        type: str
      - help: Target timestamp (YYYY[MM[DD[hh[mm[ss]]]]] or ISO date). Defaults to most recent snapshot.
        name: timestamp
        required: false
        type: string
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Archive: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `item` | `enabled` | `public_read` / `low` | `opencli_execute(site="archive", operation="content", command="item", arguments={"identifier":"<identifier>"})`<br>Fetch metadata for a single Internet Archive item by identifier. | `identifier` (str, required, positional) |
| `snapshots` | `enabled` | `public_read` / `low` | `opencli_execute(site="archive", operation="content", command="snapshots", arguments={"url":"<url>"})`<br>List Wayback Machine snapshots over time for a URL via the CDX API. | `url` (str, required, positional); `from` (string, optional); `to` (string, optional); `limit` (int, optional, default=20) |
| `wayback` | `enabled` | `public_read` / `low` | `opencli_execute(site="archive", operation="content", command="wayback", arguments={"url":"<url>"})`<br>Look up the closest Wayback Machine snapshot for a URL. | `url` (str, required, positional); `timestamp` (string, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
