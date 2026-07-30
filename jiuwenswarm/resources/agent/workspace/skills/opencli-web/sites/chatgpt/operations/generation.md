# Chatgpt: generation

Generate remote content, start AI work, or consume quota.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `ask` | `quota_consumption` / `high` | `opencli chatgpt ask "<prompt>" [--timeout <timeout>] [--new <true\|false>] [--conversation "<conversation>"] [--project "<project>"] [--wait <true\|false>] [--deep-research <true\|false>] [--web-search <true\|false>] -f json`<br>Send a prompt to ChatGPT web and wait for the response | `prompt` (str, required, positional); `timeout` (int, optional, default=120); `new` (boolean, optional, default=False); `conversation` (str, optional); `project` (str, optional); `wait` (boolean, optional, default=True); `deep-research` (boolean, optional, default=False); `web-search` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `image` | `quota_consumption` / `high` | `opencli chatgpt image "<prompt>" [--image "<image>"] [--project "<project>"] [--op "<op>"] [--sd <true\|false>] [--timeout <timeout>] -f json`<br>Generate images with ChatGPT web and save them locally | `prompt` (str, required, positional); `image` (str, optional); `project` (str, optional); `op` (str, optional); `sd` (boolean, optional, default=False); `timeout` (int, optional, default=240) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `new` | `quota_consumption` / `high` | `opencli chatgpt new [--project "<project>"] -f json`<br>Start a new ChatGPT web conversation | `project` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
