# Xiaohongshu Creator Analytics Operations

This operation contract is selected by the Xiaohongshu site router. It
authorizes only the commands listed below. Keep all parent routing, shell,
confirmation, and fallback rules in force.

| Command | Access | Exact usage | Purpose and important options |
|---|---|---|---|
| `creator-note-detail` | read | `opencli xiaohongshu creator-note-detail <note-id> -f json` | Read one creator note's content metrics, traffic sources, audience profile, and trends. |
| `creator-notes` | read | `opencli xiaohongshu creator-notes [--limit <count>] -f json` | List creator notes and per-note views, likes, saves, and comments. Limit defaults to 20. |
| `creator-notes-summary` | read | `opencli xiaohongshu creator-notes-summary [--limit <count>] [--timeout <seconds>] -f json` | Summarize recent creator notes and key metrics. Defaults: limit 3, timeout 180. |
| `creator-profile` | read | `opencli xiaohongshu creator-profile -f json` | Read the current creator account profile, followers, following, likes, and growth level. |
| `creator-stats` | read | `opencli xiaohongshu creator-stats [--period seven\|thirty] -f json` | Read creator totals and daily trends for seven or thirty days. |

## Read creator analytics

1. Use `creator-profile` for account-level identity and totals.
2. Use `creator-stats` for seven- or thirty-day aggregate trends.
3. Use `creator-notes` or `creator-notes-summary` for a recent-note collection,
   and `creator-note-detail` only after an exact note ID is known.
4. Preserve returned IDs and numeric values without rounding unless the user
   requests a derived summary.
5. A failed read may fall back to `browser_agent` when the parent router permits
   it and no account mutation occurred.
