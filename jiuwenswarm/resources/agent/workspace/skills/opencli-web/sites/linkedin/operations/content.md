# Linkedin: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `job-detail` | `public_read` / `low` | `opencli linkedin job-detail "<job-url>" -f json`<br>Read one LinkedIn job page with description, apply URL, workplace type, applicants, and company metadata | `job-url` (string, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
