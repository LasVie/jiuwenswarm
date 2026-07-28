# Xiaohongshu Account Operations

This operation contract is selected by the Xiaohongshu site router. It
authorizes only the commands listed below. Keep all parent routing, shell,
confirmation, and fallback rules in force.

| Command | Access | Exact usage | Purpose and important options |
|---|---|---|---|
| `login` | write | `opencli xiaohongshu login [--timeout <seconds>] --window foreground --site-session persistent -f json` | Open login and wait for the user to authenticate. Timeout defaults to 300 seconds. |
| `whoami` | read | `opencli xiaohongshu whoami --site-session persistent -f json` | Show the currently authenticated Xiaohongshu account. |

## Login safely

1. Use `whoami` first when the task only needs the current account identity.
2. Use `login` only when authentication is missing or the user requests an
   account change.
3. Keep the login browser in the foreground and use a persistent site session.
4. Let the user enter credentials directly in the browser. Never request,
   receive, or relay a password, cookie, or verification code in chat.
5. Once login starts, do not retry it through `browser_agent`; report timeout
   or uncertainty and let the user decide whether to try again.
