---
name: opencli-web
description: Use at the start of any task involving a live website or webpage, including searching, reading, navigation, data extraction, form filling, login, posting, publishing, commenting, or account actions, even when the user does not mention OpenCLI. Check whether an installed OpenCLI site adapter covers the task before using browser_agent, then disclose the matching opencli-* site skill.
---

# OpenCLI Web Router

Use OpenCLI as the fast, deterministic path for supported website operations while
keeping `browser_agent` as the compatibility fallback.

## Route every live website task

1. Read this skill before starting `browser_agent`.
2. Match the website and requested operation against
   [references/sites.md](references/sites.md).
3. When there is an exact match, read the named site skill with the Skill tool
   and follow only that skill's documented commands and safeguards.
4. When there is no exact match, the named site skill is unavailable, or OpenCLI
   has a provable pre-execution infrastructure failure, use `browser_agent`.

Do not guess that a site's read adapter also supports writes. A route exists only
when both the site and the requested operation are listed.

## Enforce one automation path

- Never run OpenCLI and `browser_agent` concurrently for the same operation.
- Once an OpenCLI write process has started, do not retry the operation through
  `browser_agent`, even after a timeout or ambiguous result. Prefer a read-only
  verification when one exists; otherwise stop and report uncertainty.
- Treat a missing executable, an unavailable Skill, or an unsupported operation
  detected before execution as fallback-safe.
- Do not use direct Chrome/Edge launches or ad-hoc browser scripts. OpenCLI must
  be invoked only through the selected site skill's documented wrapper.
- Preserve all channel-specific confirmation gates. A site skill cannot waive a
  required user approval or A2UI confirmation.

## M1 boundary

M1 exposes one write route:

- Xiaohongshu image/text post drafting and publishing:
  `opencli-xiaohongshu`.

Use `opencli list -f json` only to investigate installed OpenCLI capabilities.
Do not turn a newly discovered command into an executable route until its site
skill defines inputs, confirmation behavior, fallback rules, and tests.
