# Mercury: financial-actions

Financial or reimbursement state changes.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `reimbursement-draft` | `financial_write` / `critical` | `opencli mercury reimbursement-draft --receipt "<receipt>" --amount "<amount>" [--currency "<currency>"] --date "<date>" --merchant "<merchant>" [--category "<category>"] --notes "<notes>" [--ocr-wait-seconds "<ocr-wait-seconds>"] [--close-after-review <true\|false>] -f json`<br>Create a Mercury reimbursement draft from a local receipt, correct OCR fields, and stop at Review | `receipt` (str, required); `amount` (str, required); `currency` (str, optional, default='CNY'); `date` (str, required); `merchant` (str, required); `category` (str, optional, default='Marketing & Advertising'); `notes` (str, required); `ocr-wait-seconds` (str, optional, default='8'); `close-after-review` (boolean, optional, default=False) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
