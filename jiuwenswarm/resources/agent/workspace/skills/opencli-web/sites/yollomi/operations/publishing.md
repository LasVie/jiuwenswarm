# Yollomi: publishing

Publish, create, edit, or upload remote content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `edit` | `public_write` / `high` | `opencli yollomi edit "<image>" "<prompt>" [--model "<qwen-image-edit\|qwen-image-edit-plus>"] [--output "<output>"] [--no-download <true\|false>] -f json`<br>Edit images with AI text prompts (Qwen image edit) | `image` (str, required, positional); `prompt` (str, required, positional); `model` (str, optional, default='qwen-image-edit', choices=qwen-image-edit,qwen-image-edit-plus); `output` (str, optional, default='./yollomi-output'); `no-download` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `upload` | `public_write` / `high` | `opencli yollomi upload "<file>" -f json`<br>Upload an image or video to Yollomi (returns URL for other commands) | `file` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `edit`: file inputs: workspace-relative input when declared by adapter
- `upload`: file inputs: workspace-relative input when declared by adapter
