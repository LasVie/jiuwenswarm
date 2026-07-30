# Yollomi: generation

Generate remote content, start AI work, or consume quota.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `generate` | `quota_consumption` / `high` | `opencli yollomi generate "<prompt>" [--model "<model>"] [--ratio "<1:1\|16:9\|9:16\|4:3\|3:4>"] [--image "<image>"] [--output "<output>"] [--no-download <true\|false>] -f json`<br>Generate images with AI (text-to-image or image-to-image) | `prompt` (str, required, positional); `model` (str, optional, default='z-image-turbo'); `ratio` (str, optional, default='1:1', choices=1:1,16:9,9:16,4:3,3:4); `image` (str, optional); `output` (str, optional, default='./yollomi-output'); `no-download` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
