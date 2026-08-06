# Pinterest: publishing

Publish, create, edit, or upload remote content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `board-create` | `public_write` / `high` | `opencli pinterest board-create "<name>" [--description "<description>"] [--privacy "<public\|secret>"] -f json`<br>Create a new board on your account | `name` (string, required, positional); `description` (string, optional, default=''); `privacy` (string, optional, default='public', choices=public,secret) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `board-section-create` | `public_write` / `high` | `opencli pinterest board-section-create "<board>" --title "<title>" -f json`<br>Create a section inside one of your boards | `board` (string, required, positional); `title` (string, required) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `board-update` | `public_write` / `high` | `opencli pinterest board-update "<board>" [--name "<name>"] [--description "<description>"] [--privacy "<public\|secret>"] -f json`<br>Update the name, description, or privacy of your board | `board` (string, required, positional); `name` (string, optional, default=''); `description` (string, optional); `privacy` (string, optional, choices=public,secret) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `pin-create` | `public_write` / `high` | `opencli pinterest pin-create "<image>" --board "<board>" [--section "<section>"] [--title "<title>"] [--description "<description>"] [--link "<link>"] -f json`<br>Create a pin from a remote image URL onto a board | `image` (string, required, positional); `board` (string, required); `section` (string, optional, default=''); `title` (string, optional, default=''); `description` (string, optional, default=''); `link` (string, optional, default='') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `pin-update` | `public_write` / `high` | `opencli pinterest pin-update "<pin>" [--title "<title>"] [--description "<description>"] [--link "<link>"] [--board "<board>"] [--section "<section>"] -f json`<br>Update a pin's title, description, link, or board | `pin` (string, required, positional); `title` (string, optional, default=''); `description` (string, optional); `link` (string, optional); `board` (string, optional, default=''); `section` (string, optional, default='') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `board-create`: file inputs: workspace-relative input when declared by adapter
- `board-section-create`: file inputs: workspace-relative input when declared by adapter
- `board-update`: file inputs: workspace-relative input when declared by adapter
- `pin-create`: file inputs: workspace-relative input when declared by adapter
- `pin-update`: file inputs: workspace-relative input when declared by adapter
