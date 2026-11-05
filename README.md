# apps.grekko.de

Static site for Gregory Igelmund's apps: an index at `/` and one folder per App with its Datenschutz, Impressum and Hilfe (the App's privacy policy and support URL in App Store Connect).

- Hosted by GitHub Pages, deployed by the `check` workflow (`.github/workflows/check.yml`) only after `check.py` passes on `main`. Custom domain in Settings › Pages (no `CNAME` file: Actions deploys ignore it). DNS: `apps` CNAME to `grekko.github.io` in Cloudflare, DNS only.
- Only `index.html`, `elternmonate/` and `assets/` are published. A new App folder must be added to the `cp` step in the workflow.
- Plain HTML, no build step. Fonts are self-hosted on purpose: the pages must load nothing from other servers. They are IBM's own Latin1 WOFF2 files from the npm package `@ibm/plex-sans` (`fonts/split/woff2/`), unmodified, and `check.py` fails on any character on a page outside their `unicode-range`.
- `/elternmonate/` and its anchors `#datenschutz`, `#impressum`, `#hilfe` are linked from the App binary and App Store Connect. Never move them.
- Run `python3 check.py` before pushing. CI runs it too, on pushes to `main` and on pull requests (`.github/workflows/check.yml`).
