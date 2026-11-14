#!/usr/bin/env python3
"""build-feed.py: write feed.xml (RSS 2.0) with the 20 newest essays.

Run it from the repo root after adding an essay (on a full clone, because
dates can fall back to git):
    python3 scripts/build-feed.py

Which essays: the on-site writing/<slug>.html links in writing/index.html,
in the order that page lists them, first 20. Pages on HOLD in
add-seo-head.py are left out.
Each item: title (the essay's first <h1>), link, guid, pubDate (same date
rule as the JSON-LD in add-seo-head.py; left out if no date is found) and
description (the page's meta description).
Uses only Python's standard library.
"""
import html
import importlib.util
import os
import re
from datetime import datetime
from xml.sax.saxutils import escape

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "https://aryehleibtoren.com"
LIMIT = 20

spec = importlib.util.spec_from_file_location("seo", os.path.join(ROOT, "scripts", "add-seo-head.py"))
seo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(seo)


def text_of(fragment):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", fragment)).split())


def main():
    index = open(os.path.join(ROOT, "writing", "index.html"), encoding="utf-8").read()
    slugs = []
    for m in re.finditer(r'href="(?:\./|/writing/)?([a-z0-9-]+)\.html"', index):
        rel = f"writing/{m.group(1)}.html"
        if rel in seo.HOLD or rel in seo.NOT_ESSAYS or rel in slugs:
            continue
        if os.path.exists(os.path.join(ROOT, rel)):
            slugs.append(rel)
        if len(slugs) == LIMIT:
            break

    items = []
    for rel in slugs:
        page = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        url = f"{SITE}/{rel}"
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S)
        title = text_of(h1.group(1)) if h1 else text_of(re.search(r"<title>(.*?)</title>", page, re.S).group(1))
        desc = re.search(r'<meta name="description" content="([^"]*)"', page)
        item = ["    <item>", f"      <title>{escape(title)}</title>", f"      <link>{url}</link>",
                f'      <guid isPermaLink="true">{url}</guid>']
        date = seo.published(page, rel)
        if date:
            d = datetime.strptime(date, "%Y-%m-%d")
            item.append(f"      <pubDate>{d.strftime('%a, %d %b %Y')} 00:00:00 +0000</pubDate>")
        if desc:
            item.append(f"      <description>{escape(html.unescape(desc.group(1)))}</description>")
        item.append("    </item>")
        items += item

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
             "  <channel>",
             "    <title>Aryeh Leib Toren — Writing</title>",
             f"    <link>{SITE}/writing/</link>",
             f'    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml" />',
             f"    <description>{escape(text_of(re.search(r'<meta name=\"description\" content=\"([^\"]*)\"', index).group(1)))}</description>",
             "    <language>en</language>",
             *items,
             "  </channel>",
             "</rss>"]
    with open(os.path.join(ROOT, "feed.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"feed.xml: {len(slugs)} essays")


if __name__ == "__main__":
    main()
