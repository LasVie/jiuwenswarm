---
opencli_contract:
  version: 2
  site: paperreview
  operation: publishing
  policy_sha256: 7c57f79b95a57b61fee3048b014fbe427f6b1438c98418b545beeb8d2073d190
  commands:
    submit:
      executor: none
      execution_state: disabled
      semantic_effect: public_write
      risk: high
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: write
      args:
      - help: Path to the paper PDF
        name: pdf
        positional: true
        required: true
        type: str
      - help: Email address for the submission
        name: email
        required: true
        type: str
      - help: Optional target venue such as ICLR or NeurIPS
        name: venue
        required: false
        type: str
      - default: false
        help: Validate the input and stop before remote submission
        name: dry-run
        required: false
        type: bool
      - default: false
        help: Request an upload slot but stop before uploading the PDF
        name: prepare-only
        required: false
        type: bool
      - default: 120
        help: 'Max seconds for the overall command (default: 120)'
        name: timeout
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs:
      - workspace-relative input when declared by adapter
      file_outputs: []
      sensitive_output: []
---

# Paperreview: publishing

Publish, create, edit, or upload remote content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `submit` | `disabled` | `public_write` / `high` | Not executable; use the declared fallback if permitted<br>Submit a PDF to paperreview.ai for review | `pdf` (str, required, positional); `email` (str, required); `venue` (str, optional); `dry-run` (bool, optional, default=False); `prepare-only` (bool, optional, default=False); `timeout` (int, optional, default=120) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
