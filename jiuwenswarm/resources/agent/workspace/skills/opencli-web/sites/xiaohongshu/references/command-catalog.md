# Xiaohongshu command catalog

This catalog describes every command exposed by the packaged Xiaohongshu
adapter. OpenCLI's `access` classification is included, but the stricter
confirmation and retry rules in `SKILL.md` always take precedence.

Before execution, verify the chosen command with:

```text
opencli xiaohongshu <command> --help -f yaml
```

Use `-f json` for machine-readable results. Browser-backed commands also accept
`--window foreground|background`, `--site-session ephemeral|persistent`, and
`--keep-tab true|false`.

| Command | Access | Usage | Purpose and important options |
|---|---|---|---|
| `ask` | write | `opencli xiaohongshu ask <query> [--timeout <seconds>] [--source-limit <count>] -f json` | Ask 小红书点点 and return an answer with sources. Defaults: timeout 90, source limit 10. |
| `comments` | read | `opencli xiaohongshu comments <note-url> [--limit <count>] [--with-replies true\|false] -f json` | Read comments and optional nested replies. Supply the full note URL with `xsec_token`; limit defaults to 20 and is capped at 50. |
| `creator-note-detail` | read | `opencli xiaohongshu creator-note-detail <note-id> -f json` | Read one creator note's content metrics, traffic sources, audience profile, and trends. |
| `creator-notes` | read | `opencli xiaohongshu creator-notes [--limit <count>] -f json` | List creator notes and per-note views, likes, saves, and comments. Limit defaults to 20. |
| `creator-notes-summary` | read | `opencli xiaohongshu creator-notes-summary [--limit <count>] [--timeout <seconds>] -f json` | Summarize recent creator notes and key metrics. Defaults: limit 3, timeout 180. |
| `creator-profile` | read | `opencli xiaohongshu creator-profile -f json` | Read the current creator account profile, followers, following, likes, and growth level. |
| `creator-stats` | read | `opencli xiaohongshu creator-stats [--period seven\|thirty] -f json` | Read creator totals and daily trends for seven or thirty days. |
| `delete-note` | write | `opencli xiaohongshu delete-note <note-id> [--execute true] -f json` | Verify a published note target by default. After final confirmation, `--execute true` deletes it. |
| `download` | read | `opencli xiaohongshu download <note-url-or-xhslink> [--output <directory>] -f json` | Download a note's images and videos. The default output is `./xiaohongshu-downloads`; confirm the destination first. |
| `draft-clear` | write | `opencli xiaohongshu draft-clear [--type image\|video\|article\|audio\|all] [--execute true] -f json` | Count matching local drafts by default. After final confirmation, `--execute true` clears them. |
| `draft-delete` | write | `opencli xiaohongshu draft-delete <draft-id> [--type image\|video\|article\|audio] [--execute true] -f json` | Verify one local draft by default. After final confirmation, `--execute true` deletes it. |
| `draft-open` | read | `opencli xiaohongshu draft-open <draft-id> [--type image\|video\|article\|audio] -f json` | Read one local draft's title, content, images, and update time. |
| `drafts` | read | `opencli xiaohongshu drafts [--type image\|video\|article\|audio] -f json` | List local drafts of the selected type. |
| `feed` | read | `opencli xiaohongshu feed [--limit <count>] -f json` | Read the home recommendation feed. Limit defaults to 20. |
| `follow` | write | `opencli xiaohongshu follow <user-id-or-profile-url> -f json` | Follow a user immediately. Require final confirmation for the exact account. |
| `liked` | read | `opencli xiaohongshu liked [--id <user-id-or-profile-url>] [--limit <count>] -f json` | List liked notes for the current or specified user. Limit defaults to 20. |
| `login` | write | `opencli xiaohongshu login [--timeout <seconds>] --window foreground --site-session persistent -f json` | Open login and wait for the user to authenticate. Timeout defaults to 300 seconds. |
| `note` | read | `opencli xiaohongshu note <note-url> -f json` | Read note content and engagement data. Supply the full note URL with `xsec_token`. |
| `notifications` | read | `opencli xiaohongshu notifications [--type mentions\|likes\|connections] [--limit <count>] -f json` | Read account notifications. Defaults: type `mentions`, limit 20. |
| `publish` | write | `python "<opencli-web-directory>/sites/xiaohongshu/scripts/publish.py" --payload "<payload.json>"` | Create an image/text draft or publish after `social_post_confirm`. Always use the guarded wrapper and publish contract. |
| `saved` | read | `opencli xiaohongshu saved [--id <user-id-or-profile-url>] [--limit <count>] -f json` | List saved notes for the current or specified user. Limit defaults to 20. |
| `search` | read | `opencli xiaohongshu search <query> [--limit <count>] -f json` | Search notes. Limit defaults to 20. |
| `unfollow` | write | `opencli xiaohongshu unfollow <user-id-or-profile-url> -f json` | Unfollow a user immediately. Require final confirmation for the exact account. |
| `user` | read | `opencli xiaohongshu user <user-id-or-profile-url> [--limit <count>] -f json` | Read public notes from a user profile. Limit defaults to 15. |
| `whoami` | read | `opencli xiaohongshu whoami --site-session persistent -f json` | Show the currently authenticated Xiaohongshu account. |

## Output handling

- Treat a non-zero exit status as failure even if stdout contains partial data.
- Do not include credentials, cookies, tokens, or full browser traces in user
  output or logs.
- For write commands, report whether execution started. Never silently retry an
  operation that may already have changed account state.
- When a read command returns URLs or IDs needed by a later write, preserve the
  exact values and show the target to the user at the confirmation gate.
