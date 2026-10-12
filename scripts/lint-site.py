#!/usr/bin/env python3
"""Hard-rule checks for the public site. Folders starting with _ are never published and are skipped.
(a) no HOLD/draft/personal pieces published  (b) every essay has sources
(c) no VERIFY/internal markers  (e) no private paths or private doc links"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = ("_", ".git", "stage4")
errors = []
def pages():
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if any(part.startswith(SKIP) for part in rel.parts):
            continue
        yield rel, p.read_text(encoding="utf-8", errors="replace")
STATUS = re.compile(r'<meta\s+name="status"\s+content="(hold|draft|personal)"', re.I)
HOLDTXT = re.compile(r'HOLD publish|HARD HOLD|not for publication|\bPERSONAL\b — do not', re.I)
MARKERS = re.compile(r'Soft VERIFY|\[VERIFY|\bVERIFY\b|\[unverified|\(unverified\)|\bTODO\b|\bFIXME\b|LIST-LOCK|approved for publication')
PRIVATE = re.compile(r'(/home/|/workspace/|file://|C:\\\\Users|docs\.google\.com/document/d/|drive\.google\.com/file/d/)', re.I)
SOURCES = re.compile(r'<h[2-4][^>]*>\s*(Sources|References|Further reading|Notes)', re.I)
EXTLINK = re.compile(r'href="https?://(?!aryehleibtoren\.com|aryeh-leibt\.github\.io)', re.I)
def body(t):
    return re.sub(r'<(script|style)[^>]*>.*?</\1>', '', t, flags=re.S | re.I)
for rel, text in pages():
    b = body(text)
    if STATUS.search(text) or HOLDTXT.search(b):
        errors.append(f"(a) held/draft/personal piece is public: {rel}")
    for m in MARKERS.finditer(b):
        errors.append(f"(c) internal marker '{m.group(0)}' in {rel}"); break
    for m in PRIVATE.finditer(text):
        errors.append(f"(e) private path or private doc link '{m.group(0)}' in {rel}"); break
    if rel.parts[0] == "writing" and rel.name != "index.html":
        if not (SOURCES.search(b) or EXTLINK.search(b)):
            errors.append(f"(b) no sources heading or source link: {rel}")
for e in errors: print("::error::" + e if "--gh" in sys.argv else e)
print(f"{len(errors)} problem(s)")
sys.exit(1 if errors else 0)
