---
opencli_contract:
  version: 2
  site: google
  operation: web-search
  policy_sha256: 8f8e9b5f1df0ce31cba6ad236f14011d957450747655c76b7cc1583a8e22d329
  commands:
    search:
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
      - help: Search query
        name: keyword
        positional: true
        required: true
        type: str
      - default: 10
        help: Number of results (1-100)
        name: limit
        required: false
        type: int
        constraints:
          minimum: 1
          maximum: 100
      - default: en
        help: Language short code (e.g. en, zh)
        name: lang
        required: false
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Google: web-search

Read browser-rendered web search results.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="google", operation="web-search", command="search", arguments={"keyword":"<keyword>"})`<br>Search Google | `keyword` (str, required, positional); `limit` (int, optional, default=10, minimum=1,maximum=100); `lang` (str, optional, default='en') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
