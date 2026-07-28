---
opencli_contract:
  version: 2
  site: dockerhub
  operation: content
  policy_sha256: 38bfbe736ebb3e8db159d38435a0576801a39d531ced8bddb6f0367ebc17e1e4
  commands:
    image:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: Image name (e.g. "nginx", "library/nginx", "bitnami/redis")
        name: image
        positional: true
        required: true
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Dockerhub: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `image` | `enabled` | `public_read` / `low` | `opencli_execute(site="dockerhub", operation="content", command="image", arguments={"image":"<image>"})`<br>Fetch a Docker Hub repository's public metadata (stars, pulls, last updated, status) | `image` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
