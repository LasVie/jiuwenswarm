# Jimeng: generation

Generate remote content, start AI work, or consume quota.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `generate` | `quota_consumption` / `high` | `opencli jimeng generate "<prompt>" [--model "<model>"] [--wait <wait>] -f json`<br>即梦AI 文生图 — 输入 prompt 生成图片 | `prompt` (string, required, positional); `model` (string, optional, default='high_aes_general_v50'); `wait` (int, optional, default=40) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `new` | `quota_consumption` / `high` | `opencli jimeng new -f json`<br>即梦AI 新建会话（workspace） | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
