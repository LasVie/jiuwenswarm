---
name: opencli-xiaohongshu
description: Use through the preinstalled opencli-web Skill for any Xiaohongshu or 小红书 task covered by the OpenCLI adapter, including login, search, reading notes and comments, downloads, creator analytics, drafts, publishing, follows, and deletion.
---

# OpenCLI Xiaohongshu

This is a bundled site module, not an independently installed Skill. Load it
with the Skill tool by passing:

```json
{
  "skill_name": "opencli-web",
  "relative_file_path": "sites/xiaohongshu/SKILL.md"
}
```

Keep the routing and fallback rules from `opencli-web` in force.

## Choose an exact operation

The module covers every command currently packaged by the Xiaohongshu adapter:

- Account and session: `login`, `whoami`.
- Discovery and content: `ask`, `search`, `feed`, `note`, `comments`, `user`,
  `liked`, `saved`, `notifications`, `download`.
- Creator analytics: `creator-profile`, `creator-stats`, `creator-notes`,
  `creator-notes-summary`, `creator-note-detail`.
- Drafts and publishing: `drafts`, `draft-open`, `draft-delete`,
  `draft-clear`, `publish`.
- Account mutations: `follow`, `unfollow`, `delete-note`.

Read [references/command-catalog.md](references/command-catalog.md) before
invoking a command. It defines the exact usage, important arguments, access
class, and safety rule for all commands. Immediately before execution, confirm
the installed adapter schema with:

```text
opencli xiaohongshu <command> --help -f yaml
```

If the command is absent from the catalog or the installed schema conflicts
with it, do not guess. Treat the OpenCLI route as unsupported and return to the
fallback rules in `opencli-web`.

## Run read operations

1. Collect only the inputs required by the selected command.
2. Prefer structured output with `-f json`.
3. Run one exact documented command and inspect its exit status and output.
4. A read failure may fall back to `browser_agent` if no write occurred and the
   browser route is otherwise allowed.

`download` is classified as read by OpenCLI but writes files locally. Confirm
the output directory and avoid overwriting user files.

## Gate write operations

OpenCLI classifies `ask`, `login`, `follow`, `unfollow`, `delete-note`,
`draft-delete`, `draft-clear`, and `publish` as writes.

- `login` requires the user to complete authentication in the foreground
  browser session. Never request or handle a password in chat.
- `delete-note`, `draft-delete`, and `draft-clear` default to dry-run. Run the
  dry-run first, show the exact target, obtain final confirmation, and only then
  repeat once with `--execute true`.
- `follow` and `unfollow` change the account immediately. Obtain final A2UI
  confirmation for the exact user before one execution.
- Once any write command starts, never retry it with `browser_agent`. Use a
  documented read operation to verify the outcome or report uncertainty.

## Draft and publish a post

Publishing uses the guarded wrapper rather than a direct `opencli` invocation.
Read [references/publish-contract.md](references/publish-contract.md) for the
payload and result envelope.

1. Collect the exact title, content, media or text cards, and topics.
2. On the Web channel, show draft variants with `social_post_draft_select`.
3. After the user approves draft creation, write the selected values to a UTF-8
   JSON payload. Omit `mode` or set it to `"draft"`.
4. Invoke the wrapper with the Python interpreter and absolute module path:

   ```text
   python "<opencli-web-directory>/sites/xiaohongshu/scripts/publish.py" --payload "<payload.json>"
   ```

5. Inspect the JSON envelope and report the draft result. Stop before public
   publishing.

Never invoke `opencli xiaohongshu publish` directly. The wrapper validates the
payload, defaults to draft mode, preserves argument boundaries, and classifies
fallback safety.

## Public publish gate

1. Render final A2UI confirmation with `social_post_confirm`. Its context must
   exactly match the selected title, content, media or text cards, and topics.
2. Only after confirmation, set `"mode": "publish"` and include:

   ```json
   {
     "confirmation": {
       "action": "social_post_confirm",
       "id": "stable-unique-confirmation-id"
     }
   }
   ```

3. Run `scripts/publish.py` exactly once for that confirmation ID.
4. Respect `social_post_cancel` by stopping without running the wrapper.

If publishing times out or returns an ambiguous failure, do not retry and do
not switch to `browser_agent`. Verify with a documented read command when
possible; otherwise report that the outcome is unknown and require a new,
explicit confirmation before any later attempt.
