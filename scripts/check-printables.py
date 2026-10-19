#!/usr/bin/env python3
"""check-printables.py: every printable link on /printables/ points at a real file.

Parses printables/index.html and checks three things:

  1. Every internal href (nav, essays, images, PDFs) resolves to a file
     in this repo. External links (https://, mailto:) are skipped.
  2. The PDF links are exactly the PDFs that exist under printables/,
     except names that must stay unlinked: fz1073-who-vets-the-pilot,
     the-wave, and cfb-week-report-6-sep.
  3. Hebrew printables sit in the section marked lang="he" dir="rtl".
     he-will-appease-his-land-and-his.pdf is English (the title begins
     "He Will...") and must stay outside that section.

Prints the total number of PDF links and how many of them are Hebrew.
Exits 1 if any check fails, so the Site rules workflow can use it.

Run from the repo root:  python3 scripts/check-printables.py
Uses only Python's standard library.
"""
import os
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PAGE = os.path.join(ROOT, "printables", "index.html")
PDF_DIR = os.path.join(ROOT, "printables")
EXTERNAL = ("http:", "https:", "mailto:", "tel:", "javascript:", "data:", "//")
# English essay whose filename starts with "he-" because the title is
# "He Will Appease...". It has no Hebrew page under he/writing/.
ENGLISH_HE_PREFIX = "he-will-appease-his-land-and-his.pdf"
LABELS = ("type 1", "type 2", "master", "filing note", "filing notes")


class Collector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.links = []
        self.capture = None
        self.buf = []
        self.hebrew_section = False

    def handle_starttag(self, tag, attrs):
        ad = {k: (v or "") for k, v in attrs}
        self.stack.append((tag, ad))
        if tag == "section" and ad.get("id") == "hebrew":
            if ad.get("lang", "").lower().startswith("he") and ad.get("dir") == "rtl":
                self.hebrew_section = True
        if tag == "a" and "href" in ad:
            self.capture = ad["href"].strip()
            self.buf = []

    handle_startendtag = handle_starttag

    def handle_endtag(self, tag):
        if tag == "a" and self.capture is not None:
            in_he = any(
                t == "section" and a.get("lang", "").lower().startswith("he")
                for t, a in self.stack
            )
            text = "".join(self.buf).strip()
            self.links.append((self.getpos()[0], self.capture, text, in_he))
            self.capture = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.capture is not None:
            self.buf.append(data)


def target_exists(path):
    if os.path.isdir(path):
        return os.path.isfile(os.path.join(path, "index.html"))
    if os.path.isfile(path):
        return True
    if not os.path.splitext(path)[1] and os.path.isfile(path + ".html"):
        return True
    return False


def denied(name):
    stem = name.lower()
    if stem.endswith(".pdf"):
        stem = stem[: -len(".pdf")]
    if "who-vets-the-pilot" in stem or "cfb-week-report" in stem:
        return True
    return stem == "the-wave" or stem.startswith("the-wave-")


def pdf_name(url):
    path = unquote(urlsplit(url).path)
    name = os.path.basename(path)
    if name.lower().endswith(".pdf") and "/printables/" in ("/" + path.lstrip("/")):
        return name
    return None


def internal_target(url):
    if not url or url.startswith("#") or url.lower().startswith(EXTERNAL):
        return None
    parts = urlsplit(url)
    if parts.scheme or parts.netloc:
        return None
    path = unquote(parts.path)
    if not path:
        return None
    if path.startswith("/"):
        return os.path.normpath(os.path.join(ROOT, path.lstrip("/")))
    return os.path.normpath(os.path.join(os.path.dirname(PAGE), path))


def main():
    errors = []
    parser = Collector()
    with open(PAGE, encoding="utf-8") as fh:
        parser.feed(fh.read())
    if not parser.hebrew_section:
        errors.append('missing Hebrew section with lang="he" and dir="rtl"')

    on_disk = sorted(
        name for name in os.listdir(PDF_DIR)
        if name.lower().endswith(".pdf") and not denied(name)
    )
    linked = []
    hebrew = []
    for line, url, text, in_he in parser.links:
        target = internal_target(url)
        if target is not None and (not target.startswith(ROOT) or not target_exists(target)):
            errors.append(f"href does not resolve to a file: line {line} -> {url}")
        lowurl = url.lower()
        if (
            "who-vets-the-pilot" in lowurl
            or "cfb-week-report" in lowurl
            or "/the-wave" in lowurl
            or lowurl.endswith("/the-wave")
            or "the-wave.pdf" in lowurl
        ):
            errors.append(f"denied piece is linked: line {line} -> {url}")
        name = pdf_name(url)
        if not name and url.lower().split("?", 1)[0].endswith(".pdf"):
            errors.append(f"PDF href is not under /printables/: line {line} -> {url}")
            continue
        if not name:
            continue
        if denied(name):
            errors.append(f"denied PDF is linked: {name}")
        low = text.lower()
        for label in LABELS:
            if label in low:
                errors.append(f"internal label {label!r} in link text for {name}")
                break
        linked.append(name)
        if in_he:
            hebrew.append(name)
        if name.startswith("he-") and name != ENGLISH_HE_PREFIX and not in_he:
            errors.append(f"Hebrew PDF is outside the Hebrew section: {name}")
        if name == ENGLISH_HE_PREFIX and in_he:
            errors.append(f"{name} is English and must stay outside the Hebrew section")

    linked_set = set(linked)
    disk_set = set(on_disk)
    if len(linked) != len(linked_set):
        dupes = sorted({n for n in linked if linked.count(n) > 1})
        errors.append("duplicate PDF links: " + ", ".join(dupes))
    missing = sorted(disk_set - linked_set)
    extra = sorted(linked_set - disk_set)
    if missing:
        errors.append("PDFs on disk with no link: " + ", ".join(missing))
    if extra:
        errors.append("PDF links with no file: " + ", ".join(extra))
    if "fz1073-the-target-was-the-terminal.pdf" not in linked_set:
        errors.append("fz1073-the-target-was-the-terminal.pdf is not linked")

    english = len(linked) - len(hebrew)
    print(f"PDF links: {len(linked)}")
    print(f"Hebrew PDF links: {len(hebrew)}")
    print(f"English PDF links: {english}")
    if errors:
        print(f"{len(errors)} problem(s):")
        for err in errors:
            print("  " + err)
        return 1
    print("Every PDF href resolves to a file in the repo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
