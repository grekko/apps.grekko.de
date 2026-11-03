import html, re, pathlib, sys
root = pathlib.Path(__file__).parent
ok = True
css = (root / "assets/site.css").read_text()
# each @font-face's unicode-range; a character must be in all of them (every weight)
ranges = [[(int(a, 16), int(b or a, 16)) for a, b in re.findall(r"U\+([0-9A-F]+)(?:-([0-9A-F]+))?", r, re.I)]
          for r in re.findall(r"unicode-range:([^;}]+)", css)]
assert ranges, "no unicode-range in site.css"
for page in root.rglob("*.html"):
    html_text = page.read_text()
    # anything the browser fetches (src, link href, url()) must be local
    for ref in re.findall(r'(?:src|<link[^>]*href)="([^"]+)"', html_text):
        if ref.startswith(("http:", "https:", "//")):
            print(f"{page}: external load {ref}"); ok = False
        elif not ref.startswith("/") and not (page.parent / ref).exists():
            print(f"{page}: missing {ref}"); ok = False
    for anchor in re.findall(r'href="#([^"]+)"', html_text):
        if f'id="{anchor}"' not in html_text:
            print(f"{page}: missing anchor #{anchor}"); ok = False
    # links to other local pages: target must exist, and so must its #anchor
    for ref in re.findall(r'<a\b[^>]*href="([^"]+)"', html_text):
        if ref.startswith(("http:", "https:", "//", "mailto:", "#")):
            continue
        path, _, anchor = ref.partition("#")
        target = root / path.lstrip("/") if path.startswith("/") else page.parent / path
        if target.is_dir():
            target = target / "index.html"
        if not target.is_file():
            print(f"{page}: missing link {ref}"); ok = False
        elif anchor and f'id="{anchor}"' not in target.read_text():
            print(f"{page}: missing anchor {ref}"); ok = False
    # a character outside the font's unicode-range silently renders in the fallback font
    for ch in sorted(set(html.unescape(html_text)) - set("\t\n\r\f")):
        if not all(any(a <= ord(ch) <= b for a, b in r) for r in ranges):
            print(f"{page}: character U+{ord(ch):04X} {ch!r} not in the font"); ok = False
for ref in re.findall(r'url\("([^"]+)"\)', css):
    if not (root / "assets" / ref).exists():
        print(f"site.css: missing {ref}"); ok = False
for anchor in ("datenschutz", "impressum", "hilfe"):
    assert f'id="{anchor}"' in (root / "elternmonate/index.html").read_text(), anchor
print("OK" if ok else "FAIL"); sys.exit(0 if ok else 1)
