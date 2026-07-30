# Uiverse: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `preview` | `private_content_read` / `medium` | `opencli uiverse preview "<input>" [--output "<output>"] [--padding <padding>] -f json`<br>Capture a screenshot of the Uiverse preview element | `input` (str, required, positional); `output` (str, optional); `padding` (int, optional, default=8) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `preview`: sensitive output: private content, account identifiers
