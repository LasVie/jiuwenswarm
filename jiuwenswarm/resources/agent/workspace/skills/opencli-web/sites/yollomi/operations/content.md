# Yollomi: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `models` | `public_read` / `low` | `opencli yollomi models [--type "<all\|image\|video\|tool>"] -f json`<br>List available Yollomi AI models (image, video, tools) | `type` (str, optional, default='all', choices=all,image,video,tool) | auth=none; transport=local; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `models`: Reads the static adapter-local model table.
