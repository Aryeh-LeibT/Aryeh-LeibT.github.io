#!/usr/bin/env python3
"""build-sitemap.py: write sitemap.xml for search engines.

Run it from the repo root after adding or removing a page:
    python3 scripts/build-sitemap.py

What it lists: every .html page the site serves, as its public URL
(folder/index.html -> folder/). It leaves out folders that start with "_"
or "." (such as _held/, which is never published), 404.html and offline.html,
and about.html / contact.html (exact copies of /about/ and /contact/).

English/Hebrew pairs: any page under /he/ whose English twin exists gets
hreflang links (en, he, and x-default -> English) on both entries.
Uses only Python's standard library.
"""
import os
from xml.sax.saxutils import escape

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "https://aryehleibtoren.com"
EXCLUDE = {"404.html", "offline.html", "about.html", "contact.html"}


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


def main():
    pages = urls()
    pairs = {}
    for u in pages:
        if u.startswith("/he/"):
            en = u[3:]  # "/he/about/" -> "/about/"
            if en in pages:
                pairs[en] = u
                pairs[u] = u
    def twin(u):
        return u[3:] if u.startswith("/he/") else u

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
             '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for u in sorted(pages, key=lambda x: (x.startswith("/he/"), x != "/", x)):
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(SITE + u)}</loc>")
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
