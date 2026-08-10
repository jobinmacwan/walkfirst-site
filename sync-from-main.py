#!/usr/bin/env python3
"""Mirror macwanapps.com/apps/walkfirst/ onto walkfirst.macwanapps.com.

Copies the page, stylesheet, scripts and images from the main site repo and
rewrites links so the page is self-contained on the subdomain. Run after any
WalkFirst page change in the main repo, then commit & push this repo.
"""
import pathlib, re, shutil

MAIN = pathlib.Path('/Users/jobinmacwan/Desktop/Workspace/ScreenTimeBlocking/macwanapps.com')
HERE = pathlib.Path(__file__).parent

# 1. Assets: stylesheet, scripts, and every /images/ file the page references
(HERE / 'css').mkdir(exist_ok=True)
(HERE / 'js').mkdir(exist_ok=True)
(HERE / 'images').mkdir(exist_ok=True)
shutil.copy(MAIN / 'css/site.css', HERE / 'css/site.css')
for f in ['analytics.js', 'site.js']:
    shutil.copy(MAIN / 'js' / f, HERE / 'js' / f)

page = (MAIN / 'apps/walkfirst/index.html').read_text()
for img in set(re.findall(r'/images/([A-Za-z0-9._-]+)', page)):
    src = MAIN / 'images' / img
    if src.exists():
        shutil.copy(src, HERE / 'images' / img)

# 2. Rewrite links for the subdomain
# Self-links point at the subdomain root
page = page.replace('href="/apps/walkfirst/"', 'href="/"')
# Every other site page goes to the main domain
for path in ['/support/', '/blog/introducing-walkfirst/', '/blog/', '/apps/rockiva/',
             '/press/', '/privacy/', '/terms/', '/profile/', '/#apps', '/#about']:
    page = page.replace(f'href="{path}"', f'href="https://macwanapps.com{path}"')
# Studio home link (nav icon + footer) — plain "/" would be the subdomain itself
page = page.replace('href="/" class="nav-home"', 'href="https://macwanapps.com/" class="nav-home"')
page = page.replace('<a href="/" class="brand">', '<a href="https://macwanapps.com/" class="brand">')
# RSS feed lives on the main domain
page = page.replace('href="/feed.xml"', 'href="https://macwanapps.com/feed.xml"')
# Canonical stays on the main domain (the subdomain is a mirror, not a duplicate)

(HERE / 'index.html').write_text(page)
print('synced: index.html +', len(list((HERE / 'images').glob('*'))), 'images')
