# Suno: generation

Generate remote content, start AI work, or consume quota.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `generate` | `quota_consumption` / `high` | `opencli suno generate ["<prompt>"] [--lyrics "<lyrics>"] [--tags "<tags>"] [--negative-tags "<negative-tags>"] [--title "<title>"] [--instrumental <true\|false>] [--model "<model>"] [--weirdness "<weirdness>"] [--style-weight "<style-weight>"] [--formats "<formats>"] [--op "<op>"] [--timeout <timeout>] [--sd <true\|false>] [--confirm-paid <true\|false>] -f json`<br>Generate music with Suno (V5.5 chirp-fenix by default) and download clips locally | `prompt` (str, optional, positional); `lyrics` (str, optional); `tags` (str, optional); `negative-tags` (str, optional); `title` (str, optional); `instrumental` (boolean, optional, default=False); `model` (str, optional); `weirdness` (str, optional); `style-weight` (str, optional); `formats` (str, optional); `op` (str, optional); `timeout` (int, optional, default=300); `sd` (boolean, optional, default=False); `confirm-paid` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
