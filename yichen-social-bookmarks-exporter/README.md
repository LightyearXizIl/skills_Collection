# yichen-social-bookmarks-exporter

Export the currently accessible Xiaohongshu favorites, Douyin favorites, and X bookmarks into local URL files, then validate counts, duplicates, and URL shape.

## Privacy boundary

- Private collections are read only after explicit authorization for the current task.
- The workflow does not like, favorite, comment, follow, publish, or modify account data.
- It does not print or export cookies, browser storage, passwords, or token databases.
- Xiaohongshu URLs may contain `xsec_token`; those URLs stay only in the user's requested local export file.
- No real cookies, tokens, account identifiers, private URLs, export results, or personal filesystem paths are included in this repository.

## Routes

- Xiaohongshu: reuse the user's authenticated Chrome tab and scroll the Favorites → Notes panel.
- Douyin: reuse the user's authenticated Chrome tab and scroll the Favorites → Videos panel.
- X: call a separately installed Field Theory `ft` CLI build whose version contains `graphql-only`.

The X route is an optional external dependency. This repository does not include Field Theory, private query IDs, cookies, or credentials.

## Third-party attribution

- Field Theory CLI: [afar1/fieldtheory-cli](https://github.com/afar1/fieldtheory-cli)
- Upstream license: MIT
- Local license copy: [`../licenses/afar1-fieldtheory-cli-LICENSE.txt`](../licenses/afar1-fieldtheory-cli-LICENSE.txt)
- Integration type: optional external command-line runtime; no Field Theory source code or binary is vendored in this repository

The required `graphql-only` version marker identifies a user-maintained compatibility and safety overlay. It is not an official upstream Field Theory release name, and that modified runtime is not distributed here. Modified Field Theory builds must retain the upstream copyright and MIT license notice and must not be represented as official upstream releases.

## Platform compliance

- Use the workflow only for collections and bookmarks the user is authorized to access.
- Keep requests low-frequency and do not bypass access controls, CAPTCHA, rate limits, or platform security measures.
- X internal GraphQL and page-DOM collection are unofficial compatibility routes and may stop working or trigger platform controls.
- Users remain responsible for current platform terms and applicable laws.
- Xiaohongshu, Douyin, X, and Field Theory names belong to their respective owners. This project is not affiliated with or endorsed by them.
- `chrome:control-chrome` is supplied by the host agent environment and is not distributed by this repository.

## Files

- `SKILL.md`: workflow and safety rules
- `references/chrome-collections.md`: Chrome navigation and bottom-detection details
- `scripts/chrome_collectors.mjs`: read-only Xiaohongshu and Douyin collectors
- `scripts/export_x_links.py`: URL-only export from the local Field Theory index
- `scripts/validate_link_file.py`: privacy-safe URL-file validation

## Install

Copy `yichen-social-bookmarks-exporter/` into a skill directory loaded by Claude Code or Codex, keeping the directory name unchanged.

Common locations include:

- `~/.agents/skills/yichen-social-bookmarks-exporter/`
- `~/.claude/skills/yichen-social-bookmarks-exporter/`
- `~/.codex/skills/yichen-social-bookmarks-exporter/`

Restart the agent session after installation.

## Requirements

- An agent environment that provides `chrome:control-chrome` for Xiaohongshu and Douyin
- Node.js 18+ for `chrome_collectors.mjs`
- Python 3.9+ for the X exporter and link validator
- Optional: a compatible Field Theory `ft` CLI build reporting `graphql-only`

## Validation examples

```bash
python3 "<SKILL_DIR>/scripts/validate_link_file.py" \
  --platform douyin "/absolute/output/douyin.txt"

python3 "<SKILL_DIR>/scripts/export_x_links.py" \
  --output "/absolute/output/x-bookmarks.txt"
```

The X command refuses to overwrite an existing file unless `--overwrite` is passed. The Skill itself requires explicit user approval before any overwrite.

## License

Original files in this Skill follow the repository-level license. Field Theory remains under its upstream MIT License; see the attribution and license copy above.
