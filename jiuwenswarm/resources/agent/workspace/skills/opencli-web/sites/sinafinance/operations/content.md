---
opencli_contract:
  version: 2
  site: sinafinance
  operation: content
  policy_sha256: 4da364824284b2a791afdae01ce7b10e3add231b1296676d121f44fa916ab7fc
  commands:
    stock:
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
      - help: Stock name or code (e.g. 贵州茅台, 腾讯控股, AAPL)
        name: key
        positional: true
        required: true
        type: string
      - default: auto
        help: 'Market: cn, hk, us, auto (default: auto searches cn → hk → us)'
        name: market
        required: false
        type: string
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Sinafinance: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `stock` | `enabled` | `public_read` / `low` | `opencli_execute(site="sinafinance", operation="content", command="stock", arguments={"key":"<key>"})`<br>新浪财经行情（A股/港股/美股） | `key` (string, required, positional); `market` (string, optional, default='auto') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
