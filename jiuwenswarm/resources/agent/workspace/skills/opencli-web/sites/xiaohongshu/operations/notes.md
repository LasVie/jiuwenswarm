# Xiaohongshu Note Operations

This operation contract is selected by the Xiaohongshu site router. It
authorizes only the commands listed below. Keep all parent routing, shell,
confirmation, and fallback rules in force.

| Command | Access | Exact usage | Purpose and important options |
|---|---|---|---|
| `comments` | read | `opencli xiaohongshu comments <note-url> [--limit <count>] [--with-replies true\|false] -f json` | Read comments and optional nested replies. Supply the full note URL with `xsec_token`; limit defaults to 20 and is capped at 50. |
| `download` | read | `opencli xiaohongshu download <note-url-or-xhslink> [--output <directory>] -f json` | Download a note's images and videos. The default output is `./xiaohongshu-downloads`. |
| `liked` | read | `opencli xiaohongshu liked [--id <user-id-or-profile-url>] [--limit <count>] -f json` | List liked notes for the current or specified user. Limit defaults to 20. |
| `note` | read | `opencli xiaohongshu note <note-url> -f json` | Read note content and engagement data. Supply the full note URL with `xsec_token`. |
| `notifications` | read | `opencli xiaohongshu notifications [--type mentions\|likes\|connections] [--limit <count>] -f json` | Read account notifications. Defaults: type `mentions`, limit 20. |
| `saved` | read | `opencli xiaohongshu saved [--id <user-id-or-profile-url>] [--limit <count>] -f json` | List saved notes for the current or specified user. Limit defaults to 20. |
| `user` | read | `opencli xiaohongshu user <user-id-or-profile-url> [--limit <count>] -f json` | Read public notes from a user profile. Limit defaults to 15. |

## Read note data

1. Preserve full note URLs, including `xsec_token`, exactly as received.
2. Collect only the identifier, URL, limit, and reply option required by the
   selected command.
3. Run one exact command and inspect both exit status and structured output.
4. A read failure may fall back to `browser_agent` when no write occurred.

`download` is read-class in OpenCLI but writes local files. Confirm the absolute
output directory before execution and do not overwrite existing user files.
