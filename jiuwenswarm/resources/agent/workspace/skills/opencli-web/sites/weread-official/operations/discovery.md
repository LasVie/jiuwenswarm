---
opencli_contract:
  version: 2
  site: weread-official
  operation: discovery
  policy_sha256: 30b07dfc9f4d9329ce4ee190e87ecf7b2f149b7cbc99d034b073df3568170aae
  commands:
    list-apis:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: required
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    search:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: required
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: Search keyword
        name: keyword
        positional: true
        required: true
        type: str
      - choices:
        - all
        - ebook
        - webnovel
        - audio
        - author
        - fulltext
        - booklist
        - mp
        - article
        default: ebook
        help: Search type (all/ebook/webnovel/audio/author/fulltext/booklist/mp/article)
        name: scope
        required: false
        type: str
      - help: Page size (gateway default 15 when omitted)
        name: count
        required: false
        type: int
      - default: 0
        help: Pagination offset, use searchIdx of last item from previous page
        name: max-idx
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Weread Official: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `list-apis` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>List every api_name supported by the WeRead agent gateway | none |
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Search WeRead store via the official agent gateway | `keyword` (str, required, positional); `scope` (str, optional, default='ebook', choices=all,ebook,webnovel,audio,author,fulltext,booklist,mp,article); `count` (int, optional); `max-idx` (int, optional, default=0) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
