import re, pathlib, sys
root = pathlib.Path(__file__).parent
ok = True
for page in root.rglob("*.html"):
    html = page.read_text()
    # anything the browser fetches (src, link href, url()) must be local
    for ref in re.findall(r'(?:src|<link[^>]*href)="([^"]+)"', html):
        if ref.startswith(("http:", "https:", "//")):
            print(f"{page}: external load {ref}"); ok = False
        elif not ref.startswith("/") and not (page.parent / ref).exists():
            print(f"{page}: missing {ref}"); ok = False
    for anchor in re.findall(r'href="#([^"]+)"', html):
        if f'id="{anchor}"' not in html:
            print(f"{page}: missing anchor #{anchor}"); ok = False
css = (root / "assets/site.css").read_text()
for ref in re.findall(r'url\("([^"]+)"\)', css):
    if not (root / "assets" / ref).exists():
        print(f"site.css: missing {ref}"); ok = False
for anchor in ("datenschutz", "impressum", "hilfe"):
    assert f'id="{anchor}"' in (root / "elternmonate/index.html").read_text(), anchor
print("OK" if ok else "FAIL"); sys.exit(0 if ok else 1)
