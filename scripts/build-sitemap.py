#!/usr/bin/env python3
"""build-sitemap.py: write sitemap.xml for search engines.

Run it from the repo root after adding or removing a page:
    python3 scripts/build-sitemap.py

What it lists: every .html page the site serves, as its public URL
(folder/index.html -> folder/). It leaves out folders that start with "_"
or "." (such as _held/, which is never published), 404.html and offline.html,
and about.html / contact.html (exact copies of /about/ and /contact/).

English/Hebrew pairs: any page under /he/ whose English twin exists at the
same path (/he/about/ -> /about/), plus the Hebrew essays mapped to an English
essay with a different slug in HE_EN_PAIRS below, gets hreflang links
(en, he, and x-default -> English) on both entries.

lastmod: each URL gets <lastmod> from the page file's last git commit date.
Run it on a full clone (a shallow clone gives wrong dates); untracked files
get no lastmod.
Uses only Python's standard library.
"""
import os
import subprocess
from xml.sax.saxutils import escape

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "https://aryehleibtoren.com"
EXCLUDE = {"404.html", "offline.html", "about.html", "contact.html"}

# Hebrew essay -> English twin (path form used by urls()). Keep in sync when a pair is added.
HE_EN_PAIRS = {
    "/he/writing/1318-names/": "/writing/1318-names.html",
    "/he/writing/aniyah-soarah/": "/writing/the-storm-tossed-banner.html",
    "/he/writing/ayeka-7-oct-at-three/": "/writing/ayeka-7-oct-at-three.html",
    "/he/writing/kamza-bar-kamza-anvetanut/": "/writing/kamza-bar-kamza-covenantal-leadership.html",
    "/he/writing/korach-chukat-machloket/": "/writing/korach-chukat-covenantal-leadership.html",
    "/he/writing/nachamu-hester-vegilui/": "/writing/calibrated-concealment-nachamu.html",
    "/he/writing/named-for-no-one/": "/writing/named-for-no-one-the-draft-and-the.html",
    "/he/writing/odfim-heskem-odafim/": "/writing/odfim-how-a-surplus-vote-agreement.html",
    "/he/writing/one-more-seat/": "/writing/one-more-seat-if-both-clear.html",
    "/he/writing/right-or-palestine/": "/writing/right-or-palestine-the-arithmetic.html",
    "/he/writing/shalach-et-ami-veyaavduni/": "/writing/exodus-as-political-archetype.html",
    "/he/writing/the-61-that-isnt-there/": "/writing/the-61-that-isnt-there.html",
    "/he/writing/the-gate-at-alumim/": "/writing/the-gate-at-alumim-memory-non-domination.html",
    "/he/writing/the-village-ceiling/": "/writing/the-village-ceiling.html",
    "/he/writing/two-ballots-two-days-apart/": "/writing/two-ballots-two-days-apart.html",
    "/he/writing/where-is-your-brother/": "/writing/where-is-your-brother.html",
}
# No English twin found (leave unpaired until Writing confirms):
# /he/writing/ayeka-short/, /he/writing/leaders-and-dwarfs-october/, /he/writing/one-bus-one-big-question/


def urls():
    found = set()
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith(("_", "."))]
        for name in filenames:
            if not name.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), ROOT).replace(os.sep, "/")
            if rel in EXCLUDE:
                continue
            if rel == "index.html":
                found.add("/")
            elif rel.endswith("/index.html"):
                found.add("/" + rel[: -len("index.html")])
            else:
                found.add("/" + rel)
    return found


def lastmod(u):
    """Last git commit date (YYYY-MM-DD) of the file behind URL u, or "" if untracked."""
    rel = "index.html" if u == "/" else (u.lstrip("/") + "index.html" if u.endswith("/") else u.lstrip("/"))
    return subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel],
                          cwd=ROOT, capture_output=True, text=True).stdout.strip()


def main():
    pages = urls()
    pairs = {}
    for u in pages:
        if u.startswith("/he/"):
            en = u[3:]  # "/he/about/" -> "/about/"
            if en in pages:
                pairs[en] = u
                pairs[u] = u
    for he, en in HE_EN_PAIRS.items():
        if he in pages and en in pages:
            pairs[en] = he
            pairs[he] = he
    EN_OF = dict(HE_EN_PAIRS)

    def twin(u):
        if u in EN_OF:
            return EN_OF[u]
        return u[3:] if u.startswith("/he/") else u

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
             '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for u in sorted(pages, key=lambda x: (x.startswith("/he/"), x != "/", x)):
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(SITE + u)}</loc>")
        lm = lastmod(u)
        if lm:
            lines.append(f"    <lastmod>{lm}</lastmod>")
        if u in pairs:
            en, he = twin(u), pairs[u]
            for lang, href in (("en", en), ("he", he), ("x-default", en)):
                lines.append(f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{escape(SITE + href)}" />')
        lines.append("  </url>")
    lines.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"sitemap.xml: {len(pages)} pages, {len(pairs) // 2} English/Hebrew pairs")


if __name__ == "__main__":
    main()
