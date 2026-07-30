# Yollomi: destructive-actions

Delete, remove, revoke, or perform administrative changes.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `remove-bg` | `destructive_or_admin` / `critical` | `opencli yollomi remove-bg "<image>" [--output "<output>"] [--no-download <true\|false>] -f json`<br>Remove image background with AI (free) | `image` (str, required, positional); `output` (str, optional, default='./yollomi-output'); `no-download` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
