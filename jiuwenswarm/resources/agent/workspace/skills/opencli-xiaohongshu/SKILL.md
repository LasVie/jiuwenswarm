---
name: opencli-xiaohongshu
description: Use for Xiaohongshu or 小红书 website tasks involving an image/text note, post composition, draft creation, or publishing. Load opencli-web first, then use the guarded OpenCLI publish wrapper instead of browser_agent when this exact operation is supported.
---

# OpenCLI Xiaohongshu

This M1 skill supports the `xiaohongshu publish` adapter for image/text notes.
Read `opencli-web` first so its capability and fallback rules remain in force.

## Supported operation

Create a Xiaohongshu note from:

- a title of at most 20 characters;
- non-empty post content;
- either 1-9 image paths or one or more text-card strings;
- optional topics without `#`;
- an optional text-card style.

Read [references/publish-contract.md](references/publish-contract.md) for the
payload schema and result envelope. Other Xiaohongshu operations are unsupported
in M1 and must fall back through `opencli-web`.

## Required workflow

1. Collect the exact title, content, media/text cards, and topics.
2. On the Web channel, show draft variants with
   `social_post_draft_select`. Do not substitute plain text for required A2UI.
3. Obtain the user's approval before creating an account draft.
4. Write the selected values to a UTF-8 JSON payload. Omit `mode` or set it to
   `"draft"` for the first execution.
5. Invoke the wrapper with the Python interpreter and the absolute skill path:

   ```text
   python "<skill-directory>/scripts/publish.py" --payload "<payload.json>"
   ```

6. Inspect the wrapper's JSON envelope. If `fallback_allowed` is `false`, never
   repeat the same operation with `browser_agent`.
7. Report the draft result and stop before public publishing.

Never invoke `opencli xiaohongshu publish` directly. The wrapper supplies draft
mode by default, validates the payload, preserves argument boundaries, and
classifies fallback safety.

## Public publish gate

Publishing is a separate operation from draft creation.

1. Render final A2UI confirmation with `social_post_confirm` and ensure its
   context exactly matches the selected title, content, media/text cards, and
   topics.
2. Only after that action, set `"mode": "publish"` and include:

   ```json
   {
     "confirmation": {
       "action": "social_post_confirm",
       "id": "stable-unique-confirmation-id"
     }
   }
   ```

3. Run `scripts/publish.py` exactly once for that confirmation ID. The wrapper
   atomically consumes it before starting the write process.
4. Respect `social_post_cancel` by stopping without running the wrapper.

If publishing times out or returns an ambiguous failure, do not retry and do not
switch to `browser_agent`. Use a read-only verification if a supported route is
available; otherwise report that the outcome is unknown and request a new,
explicit confirmation before any later attempt.

## Fallback boundary

Fallback to `browser_agent` is permitted only when the wrapper returns
`fallback_allowed: true`, which is reserved for a missing/unavailable OpenCLI
runtime detected before the adapter starts. Invalid input, consumed
confirmation, and every result after process start are not fallback-safe.
