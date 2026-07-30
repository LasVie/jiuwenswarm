# Dockerhub: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `image` | `public_read` / `low` | `opencli dockerhub image "<image>" -f json`<br>Fetch a Docker Hub repository's public metadata (stars, pulls, last updated, status) | `image` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
