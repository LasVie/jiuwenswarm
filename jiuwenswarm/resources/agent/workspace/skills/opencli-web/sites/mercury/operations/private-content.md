# Mercury: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `reimbursement-plan` | `private_content_read` / `medium` | `opencli mercury reimbursement-plan --receipt "<receipt>" --amount "<amount>" [--currency "<currency>"] --date "<date>" --merchant "<merchant>" [--category "<category>"] --notes "<notes>" [--ocr-wait-seconds "<ocr-wait-seconds>"] [--close-after-review <true\|false>] -f json`<br>Validate Mercury reimbursement inputs and print the draft plan without opening a browser | `receipt` (str, required); `amount` (str, required); `currency` (str, optional, default='CNY'); `date` (str, required); `merchant` (str, required); `category` (str, optional, default='Marketing & Advertising'); `notes` (str, required); `ocr-wait-seconds` (str, optional, default='8'); `close-after-review` (boolean, optional, default=False) | auth=required; transport=local; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `reimbursement-plan`: sensitive output: private content, account identifiers
