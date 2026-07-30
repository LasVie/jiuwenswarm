# Linkedin: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `profile-analytics` | `private_account_read` / `medium` | `opencli linkedin profile-analytics [--profile-url "<profile-url>"] -f json`<br>Read visible LinkedIn profile dashboard metrics such as profile views, post impressions, and search appearances | `profile-url` (string, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `profile-experience` | `private_account_read` / `medium` | `opencli linkedin profile-experience [--profile-url "<profile-url>"] -f json`<br>Read visible LinkedIn profile experience entries with titles, dates, locations, skills, media, and URLs | `profile-url` (string, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `profile-projects` | `private_account_read` / `medium` | `opencli linkedin profile-projects [--profile-url "<profile-url>"] -f json`<br>Read visible LinkedIn profile projects with descriptions, dates, skills, media, and URLs | `profile-url` (string, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `profile-read` | `private_account_read` / `medium` | `opencli linkedin profile-read [--profile-url "<profile-url>"] -f json`<br>Read visible LinkedIn profile sections: headline, About, experience, education, services, and featured sections | `profile-url` (string, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `whoami` | `private_account_read` / `medium` | `opencli linkedin whoami -f json`<br>Show the current logged-in linkedin account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `profile-analytics`: sensitive output: account identifiers
- `profile-experience`: sensitive output: account identifiers
- `profile-projects`: sensitive output: account identifiers
- `profile-read`: sensitive output: account identifiers
- `whoami`: sensitive output: account identifiers
