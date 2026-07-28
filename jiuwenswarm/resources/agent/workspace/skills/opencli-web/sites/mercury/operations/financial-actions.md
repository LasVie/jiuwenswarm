---
opencli_contract:
  version: 2
  site: mercury
  operation: financial-actions
  policy_sha256: a1376e6ba8694455786c63a7039937f24f5b24f3bccff07d273186601fe14613
  commands:
    reimbursement-draft:
      executor: none
      execution_state: disabled
      semantic_effect: financial_write
      risk: critical
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Local receipt/proof file path
        name: receipt
        required: true
        type: str
      - help: Original-currency amount, e.g. 140.00
        name: amount
        required: true
        type: str
      - default: CNY
        help: Original currency code
        name: currency
        required: false
        type: str
      - help: Expense date as YYYY-MM-DD
        name: date
        required: true
        type: str
      - help: Merchant shown on the reimbursement
        name: merchant
        required: true
        type: str
      - default: Marketing & Advertising
        help: Mercury expense category
        name: category
        required: false
        type: str
      - help: Business purpose / reimbursement notes
        name: notes
        required: true
        type: str
      - default: '8'
        help: Seconds to wait after receipt upload before correcting OCR-overwritten fields
        name: ocr-wait-seconds
        required: false
        type: str
      - default: false
        help: Close the Review dialog after verification; final Submit is still never clicked
        name: close-after-review
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Mercury: financial-actions

Financial or reimbursement state changes.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `reimbursement-draft` | `disabled` | `financial_write` / `critical` | Not executable; use the declared fallback if permitted<br>Create a Mercury reimbursement draft from a local receipt, correct OCR fields, and stop at Review | `receipt` (str, required); `amount` (str, required); `currency` (str, optional, default='CNY'); `date` (str, required); `merchant` (str, required); `category` (str, optional, default='Marketing & Advertising'); `notes` (str, required); `ocr-wait-seconds` (str, optional, default='8'); `close-after-review` (boolean, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
