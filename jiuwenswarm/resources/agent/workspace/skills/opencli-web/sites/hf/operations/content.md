---
opencli_contract:
  version: 2
  site: hf
  operation: content
  policy_sha256: e8afd494921f63232510d673c2bf09fcb4870f7cd85f517bcc620b9698121449
  commands:
    datasets:
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
      - default: downloads
        help: 'Sort key: downloads, likes, trending, created_at, last_modified'
        name: sort
        required: false
        type: string
      - help: Optional name/owner substring filter.
        name: search
        required: false
        type: string
      - default: 20
        help: Max datasets (max 100; one API page).
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
    models:
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
      - default: downloads
        help: 'Sort key: downloads, likes, trending, created_at, last_modified'
        name: sort
        required: false
        type: string
      - help: Optional name/owner substring filter (e.g. "llama", "mistralai/")
        name: search
        required: false
        type: string
      - help: Filter by pipeline tag (e.g. text-generation, image-classification)
        name: pipeline
        required: false
        type: string
      - default: 20
        help: Max models (max 100; one API page).
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
      - help: arXiv id (e.g. "1706.03762") — same value HF uses to mirror the paper
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
    spaces:
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
      - default: likes
        help: 'Sort key: likes, created_at, last_modified'
        name: sort
        required: false
        type: string
      - help: Optional name/owner substring filter (e.g. "stability", "openai/")
        name: search
        required: false
        type: string
      - help: 'Filter by Space SDK: gradio / streamlit / docker / static'
        name: sdk
        required: false
        type: string
      - default: 20
        help: Max spaces (max 100; one API page).
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
    top:
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
      - default: 20
        help: Number of papers
        name: limit
        required: false
        type: int
      - default: false
        help: Return all papers (ignore limit)
        name: all
        required: false
        type: bool
      - help: Date (YYYY-MM-DD), defaults to most recent
        name: date
        required: false
        type: str
      - choices:
        - daily
        - weekly
        - monthly
        default: daily
        help: 'Time period: daily, weekly, or monthly'
        name: period
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

# Hf: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `datasets` | `enabled` | `public_read` / `low` | `opencli_execute(site="hf", operation="content", command="datasets")`<br>Top Hugging Face datasets (downloads / likes / trending / freshness). | `sort` (string, optional, default='downloads'); `search` (string, optional); `limit` (int, optional, default=20) |
| `models` | `enabled` | `public_read` / `low` | `opencli_execute(site="hf", operation="content", command="models")`<br>Top Hugging Face models (downloads / likes / trending / freshness). | `sort` (string, optional, default='downloads'); `search` (string, optional); `pipeline` (string, optional); `limit` (int, optional, default=20) |
| `paper` | `enabled` | `public_read` / `low` | `opencli_execute(site="hf", operation="content", command="paper", arguments={"id":"<id>"})`<br>Hugging Face paper detail by arXiv id (full title / summary / authors / AI keywords) | `id` (str, required, positional) |
| `spaces` | `enabled` | `public_read` / `low` | `opencli_execute(site="hf", operation="content", command="spaces")`<br>Top Hugging Face Spaces (likes / created_at / last_modified). | `sort` (string, optional, default='likes'); `search` (string, optional); `sdk` (string, optional); `limit` (int, optional, default=20) |
| `top` | `enabled` | `public_read` / `low` | `opencli_execute(site="hf", operation="content", command="top")`<br>Top upvoted Hugging Face papers | `limit` (int, optional, default=20); `all` (bool, optional, default=False); `date` (str, optional); `period` (str, optional, default='daily', choices=daily,weekly,monthly) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
