---
opencli_contract:
  version: 2
  site: dblp
  operation: content
  policy_sha256: 55d63ee00b219be20681378d7fb15288353ba81056caf2b1e42c9fca47c03978
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
      - help: Author name (e.g. "Yoshua Bengio"). Optional when --pid is given.
        name: author
        positional: true
        required: false
        type: str
      - help: Canonical dblp PID (e.g. "56/953"). Bypasses author search.
        name: pid
        required: false
        type: str
      - default: 20
        help: Max publications (1-200)
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
      - help: dblp record key (round-tripped from the `key` column of `dblp search`)
        name: key
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
      - help: Venue name or acronym (e.g. "ICLR", "neural networks")
        name: query
        positional: true
        required: true
        type: str
      - default: 20
        help: Max venues (1-100, single dblp page)
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

# Dblp: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `author` | `enabled` | `public_read` / `low` | `opencli_execute(site="dblp", operation="content", command="author")`<br>List dblp publications by a given author (newest first; resolves to top PID match) | `author` (str, optional, positional); `pid` (str, optional); `limit` (int, optional, default=20) |
| `paper` | `enabled` | `public_read` / `low` | `opencli_execute(site="dblp", operation="content", command="paper", arguments={"key":"<key>"})`<br>Fetch a dblp record by canonical key (e.g. conf/nips/VaswaniSPUJGKP17) | `key` (str, required, positional) |
| `venue` | `enabled` | `public_read` / `low` | `opencli_execute(site="dblp", operation="content", command="venue", arguments={"query":"<query>"})`<br>Search dblp venue registry (conferences / journals) by name or acronym | `query` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
