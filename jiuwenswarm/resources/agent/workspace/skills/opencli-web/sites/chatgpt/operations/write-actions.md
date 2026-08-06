# Chatgpt: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `model` | `reversible_remote_write` / `high` | `opencli chatgpt model "<fast\|speed\|instant\|极速\|balanced\|balance\|medium\|均衡\|advanced\|high\|thinking\|高级\|very-high\|ultra\|xhigh\|x-high\|extra-high\|超高\|gpt-5.6-pro\|gpt-5-6-pro\|gpt-5.6-sol-pro\|gpt-5-6-sol-pro\|gpt-5.6\|gpt-5-6\|5.6-pro\|5.6\|pro\|professional\|专业>" [--project "<project>"] -f json`<br>Switch ChatGPT web model or intelligence level (GPT-5.6 Pro, fast, balanced, advanced, very-high, pro) | `model` (str, required, positional, choices=fast,speed,instant,极速,balanced,balance,medium,均衡,advanced,high,thinking,高级,very-high,ultra,xhigh,x-high,extra-high,超高,gpt-5.6-pro,gpt-5-6-pro,gpt-5.6-sol-pro,gpt-5-6-sol-pro,gpt-5.6,gpt-5-6,5.6-pro,5.6,pro,professional,专业); `project` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `project-file-add` | `reversible_remote_write` / `high` | `opencli chatgpt project-file-add "<file>" --id "<id>" -f json`<br>Upload files to a ChatGPT project as project knowledge (not just conversation attachments) | `file` (str, required, positional); `id` (str, required) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
