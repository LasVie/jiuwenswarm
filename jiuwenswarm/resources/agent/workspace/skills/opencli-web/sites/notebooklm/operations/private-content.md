# Notebooklm: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `current` | `private_content_read` / `medium` | `opencli notebooklm current -f json`<br>Show metadata for the currently opened NotebookLM notebook tab | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `get` | `private_content_read` / `medium` | `opencli notebooklm get -f json`<br>Get rich metadata for the currently opened NotebookLM notebook | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `history` | `private_content_read` / `medium` | `opencli notebooklm history -f json`<br>List NotebookLM conversation history threads in the current notebook | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `list` | `private_content_read` / `medium` | `opencli notebooklm list -f json`<br>List NotebookLM notebooks via in-page batchexecute RPC in the current logged-in session | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `note-list` | `private_content_read` / `medium` | `opencli notebooklm note-list -f json`<br>List saved notes from the Studio panel of the current NotebookLM notebook | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `notes-get` | `private_content_read` / `medium` | `opencli notebooklm notes-get "<note>" -f json`<br>Get one note from the current NotebookLM notebook by title from the visible note editor | `note` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `open` | `private_content_read` / `medium` | `opencli notebooklm open "<notebook>" -f json`<br>Open one NotebookLM notebook in the adapter session by id or URL | `notebook` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `source-fulltext` | `private_content_read` / `medium` | `opencli notebooklm source-fulltext "<source>" -f json`<br>Get the extracted fulltext for one source in the currently opened NotebookLM notebook | `source` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `source-get` | `private_content_read` / `medium` | `opencli notebooklm source-get "<source>" -f json`<br>Get one source from the currently opened NotebookLM notebook by id or title | `source` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `source-guide` | `private_content_read` / `medium` | `opencli notebooklm source-guide "<source>" -f json`<br>Get the guide summary and keywords for one source in the currently opened NotebookLM notebook | `source` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `source-list` | `private_content_read` / `medium` | `opencli notebooklm source-list -f json`<br>List sources for the currently opened NotebookLM notebook | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `summary` | `private_content_read` / `medium` | `opencli notebooklm summary -f json`<br>Get the summary block from the currently opened NotebookLM notebook | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `current`: Source-audited against OpenCLI 1.8.6 notebooklm/current.js; reads authenticated notebook content or metadata without changing remote notebook state.; sensitive output: private notebook content, account identifiers
- `get`: Source-audited against OpenCLI 1.8.6 notebooklm/get.js; reads authenticated notebook content or metadata without changing remote notebook state.; sensitive output: private notebook content, account identifiers
- `history`: Source-audited against OpenCLI 1.8.6 notebooklm/history.js; reads authenticated notebook content or metadata without changing remote notebook state.; sensitive output: private notebook content, account identifiers
- `list`: Source-audited against OpenCLI 1.8.6 notebooklm/list.js; reads authenticated notebook content or metadata without changing remote notebook state.; sensitive output: private notebook content, account identifiers
- `note-list`: Source-audited against OpenCLI 1.8.6 notebooklm/note-list.js; reads authenticated notebook content or metadata without changing remote notebook state.; sensitive output: private notebook content, account identifiers
- `notes-get`: Source-audited against OpenCLI 1.8.6 notebooklm/notes-get.js; reads authenticated notebook content or metadata without changing remote notebook state.; sensitive output: private notebook content, account identifiers
- `open`: Source-audited against OpenCLI 1.8.6 notebooklm/open.js; reads authenticated notebook content or metadata without changing remote notebook state.; sensitive output: private notebook content, account identifiers
- `source-fulltext`: Source-audited against OpenCLI 1.8.6 notebooklm/source-fulltext.js; reads authenticated notebook content or metadata without changing remote notebook state.; sensitive output: private notebook content, account identifiers
- `source-get`: Source-audited against OpenCLI 1.8.6 notebooklm/source-get.js; reads authenticated notebook content or metadata without changing remote notebook state.; sensitive output: private notebook content, account identifiers
- `source-guide`: Source-audited against OpenCLI 1.8.6 notebooklm/source-guide.js; reads authenticated notebook content or metadata without changing remote notebook state.; sensitive output: private notebook content, account identifiers
- `source-list`: Source-audited against OpenCLI 1.8.6 notebooklm/source-list.js; reads authenticated notebook content or metadata without changing remote notebook state.; sensitive output: private notebook content, account identifiers
- `summary`: Source-audited against OpenCLI 1.8.6 notebooklm/summary.js; reads authenticated notebook content or metadata without changing remote notebook state.; sensitive output: private notebook content, account identifiers
