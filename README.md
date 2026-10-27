# apps.grekko.de

Static site for Gregory Igelmund's apps: an index at `/` and one folder per App with its Datenschutz, Impressum and Hilfe (the App's privacy policy and support URL in App Store Connect).

- Hosted by GitHub Pages from `main`, custom domain in `CNAME`. DNS: `apps` CNAME to `grekko.github.io` in Cloudflare, DNS only.
- Plain HTML, no build step. Fonts are self-hosted on purpose: the pages must load nothing from other servers.
- `/elternmonate/` and its anchors `#datenschutz`, `#impressum`, `#hilfe` are linked from the App binary and App Store Connect. Never move them.
- Run `python3 check.py` before pushing.
