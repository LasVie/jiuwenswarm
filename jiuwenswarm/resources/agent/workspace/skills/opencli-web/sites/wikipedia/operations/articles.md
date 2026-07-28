---
opencli_contract:
  version: 2
  site: wikipedia
  operation: articles
  policy_sha256: 230e0d7012b645670f11323ce167ae5cb4746e97d5dcc90cde4a2fd4a9d6e798
  commands:
    page:
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
      - help: Article title (e.g. "Transformer (machine learning model)")
        name: title
        positional: true
        required: true
        type: string
      - default: en
        help: Language code (en, zh, ja, de, ...).
        name: lang
        required: false
        type: string
        constraints:
          pattern: ^[a-z]{2,3}(?:-[a-z0-9]+)?$
      - default: 0
        help: Cap to first N paragraphs (0 = full article).
        name: paragraphs
        required: false
        type: int
        constraints:
          minimum: 0
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    summary:
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
      - help: Article title (e.g. "Transformer (machine learning model)")
        name: title
        positional: true
        required: true
        type: str
      - default: en
        help: Language code (e.g. en, zh, ja)
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

# Wikipedia: articles

Read encyclopedia pages and summaries.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `page` | `enabled` | `public_read` / `low` | `opencli_execute(site="wikipedia", operation="articles", command="page", arguments={"title":"<title>"})`<br>Full plain-text extract of a Wikipedia article (optional paragraph cap). | `title` (string, required, positional); `lang` (string, optional, default='en', pattern=^[a-z]{2,3}(?:-[a-z0-9]+)?$); `paragraphs` (int, optional, default=0, minimum=0) |
| `summary` | `enabled` | `public_read` / `low` | `opencli_execute(site="wikipedia", operation="articles", command="summary", arguments={"title":"<title>"})`<br>Get Wikipedia article summary | `title` (str, required, positional); `lang` (str, optional, default='en') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
