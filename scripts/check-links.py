#!/usr/bin/env python3
"""check-links.py: find broken internal links on this site.

How it works (plain version):
  1. Walk every .html file the site serves (skips _held/, folders that start
     with "_" or ".", and node_modules).
  2. Read every href="..." and src="..." in each page.
  3. Ignore outside links (https://..., mailto:, tel:, javascript:, data:)
     and plain in-page anchors like href="#main".
  4. For each internal link, work out which file it points to:
       - "/writing/"           -> writing/index.html  (root-relative)
       - "../css/styles.css"   -> css/styles.css      (relative to the page)
       - "page.html#part"      -> page.html           (anchor is dropped)
     A folder link counts as working if the folder has an index.html.
     A link with no extension also passes if "<name>.html" exists
     (GitHub Pages serves /support as support.html).
  5. Print every link whose file does not exist, and exit with code 1
     if there are any (so a GitHub Action can fail the check).

Run it from the repo root:   python3 scripts/check-links.py
Uses only Python's standard library.
"""
import os
import sys
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKIP_DIRS = {"node_modules"}
EXTERNAL = ("http:", "https:", "mailto:", "tel:", "javascript:", "data:", "//")


class LinkCollector(HTMLParser):
    """Collects (line number, url) for every href= and src= in a page."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value is not None:
                self.links.append((self.getpos()[0], value.strip()))

    handle_startendtag = handle_starttag


def served_pages():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(
            d for d in dirnames
            if not d.startswith(("_", ".")) and d not in SKIP_DIRS
        )
        for name in sorted(filenames):
            if name.endswith(".html"):
                yield os.path.join(dirpath, name)


def target_exists(path):
    """True if the site would serve something at this file path."""
    if os.path.isdir(path):
        return os.path.isfile(os.path.join(path, "index.html"))
    if os.path.isfile(path):
        return True
    if not os.path.splitext(path)[1] and os.path.isfile(path + ".html"):
        return True
    return False


def check():
    broken = []
    pages = 0
    links = 0
    for page in served_pages():
        pages += 1
        parser = LinkCollector()
        with open(page, encoding="utf-8") as fh:
            parser.feed(fh.read())
        page_dir = os.path.dirname(page)
        for line, url in parser.links:
            if not url or url.startswith("#") or url.lower().startswith(EXTERNAL):
                continue
            parts = urlsplit(url)
            if parts.scheme or parts.netloc:
                continue
            path = unquote(parts.path)
            if not path:
                continue  # e.g. "?x=1" or "#top" on the same page
            links += 1
            if path.startswith("/"):
                target = os.path.join(ROOT, path.lstrip("/"))
            else:
                target = os.path.join(page_dir, path)
            target = os.path.normpath(target)
            if not target.startswith(ROOT) or not target_exists(target):
                broken.append((os.path.relpath(page, ROOT), line, url))
    return pages, links, broken


def main():
    pages, links, broken = check()
    print(f"Checked {links} internal links on {pages} pages.")
    if broken:
        print(f"{len(broken)} broken link(s):")
        for page, line, url in broken:
            print(f"  {page}:{line}  ->  {url}")
        return 1
    print("No broken internal links.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
