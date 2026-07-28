# Site capability map

Site modules are bundled under `opencli-web/sites/`. They are disclosed through
the same installed Skill by using the Skill tool's `relative_file_path`
argument; they are not separately installed or selected by the user.

| Website | Recognized domains | Coverage | Relative file path |
|---|---|---|---|
| Xiaohongshu / 小红书 | `www.xiaohongshu.com`, `creator.xiaohongshu.com`, Xiaohongshu note and profile links | All 25 commands documented in the bundled adapter catalog | `sites/xiaohongshu/SKILL.md` |

For Xiaohongshu, call the Skill tool with `skill_name: opencli-web` and
`relative_file_path: sites/xiaohongshu/SKILL.md`.

An adapter reported by `opencli list -f json` is not automatically a production
route. Until a site module documents its inputs, safety gates, fallback rules,
and supported operations, use `browser_agent`.
