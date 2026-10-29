#!/usr/bin/env python3
"""add-seo-head.py: add search and share tags to the <head> of essays.

Run it from the repo root after adding an essay:
    python3 scripts/add-seo-head.py            # all essays
    python3 scripts/add-seo-head.py writing/new-essay.html he/writing/new/index.html

What it adds (only tags that are missing; it never edits or removes a line,
and it only inserts lines just before </head>):
  English essays (writing/<slug>.html):
    canonical, og:url, og:description (copied from the meta description),
    og:image (images/cards/card-<slug>.webp if it exists, else images/aryeh.jpg),
    og:site_name, twitter:card ("summary_large_image" with a 1200x630 card,
    "summary" with the portrait photo), twitter:site,
    hreflang en/he/x-default when the essay has a Hebrew twin, and
    BlogPosting JSON-LD.
  Hebrew essays (he/writing/<slug>/index.html):
    hreflang en/he/x-default when the essay has an English twin, and
    BlogPosting JSON-LD with "inLanguage": "he".

JSON-LD dates (a field is left out rather than guessed):
  datePublished: 1) <time datetime="YYYY-MM-DD"> on the page, 2) the date in the
  <p class="byline"> line, 3) the file's first commit date in git.
  dateModified: the file's last commit date in git.
  Run on a full clone; a shallow clone gives wrong git dates.
  headline: the first <h1>, left out if it is missing or longer than 110 characters.

Pages on HOLD below are skipped until Aryeh decides; pages on SHARE_HOLD get
only canonical, hreflang and JSON-LD without description or image. Elections pages are never touched.
Uses only Python's standard library.
"""
import html
import importlib.util
import json
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "https://aryehleibtoren.com"
PERSON_ID = SITE + "/#person"
DEFAULT_IMAGE = SITE + "/images/aryeh.jpg"
HOLD = set()  # pages skipped entirely until Aryeh decides (none at the moment)
# Share tags on HOLD (no og:*/twitter:* added, and no description or image in the
# JSON-LD) until Aryeh decides. Its meta description quotes poll sources.
SHARE_HOLD = {"writing/count-to-sixty-one.html"}
NOT_ESSAYS = {"writing/index.html", "writing/archive.html"}
MONTHS = {m: i for i, m in enumerate(
    "January February March April May June July August September October November December".split(), 1)}


def he_en_pairs():
    spec = importlib.util.spec_from_file_location("bs", os.path.join(ROOT, "scripts", "build-sitemap.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.HE_EN_PAIRS


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def first_commit(rel):
    out = git("log", "--diff-filter=A", "--follow", "--format=%cs", "--", rel).splitlines()
    return out[-1] if out else ""


def published(text, rel):
    m = re.search(r'<time[^>]*datetime="(\d{4}-\d{2}-\d{2})', text)
    if m:
        return m.group(1)
    b = re.search(r'<p class="byline"[^>]*>(.*?)</p>', text, re.S)
    if b:
        d = re.search(r"\b(\d{1,2}) (" + "|".join(MONTHS) + r") (\d{4})\b", b.group(1))
        if d:
            return f"{d.group(3)}-{MONTHS[d.group(2)]:02d}-{int(d.group(1)):02d}"
    return first_commit(rel)


def path_of(rel):
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def attr(head, pattern):
    m = re.search(pattern, head)
    return m.group(1) if m else None


def jsonld(obj):
    body = json.dumps(obj, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return ['<script type="application/ld+json">', *body.splitlines(), "</script>"]


def process(rel, pairs, en_to_he):
    full = os.path.join(ROOT, rel)
    text = open(full, encoding="utf-8").read()
    if "</head>" not in text:
        return False
    head = text.split("</head>", 1)[0]
    he = rel.startswith("he/")
    url = SITE + path_of(rel)
    desc_raw = attr(head, r'<meta name="description" content="([^"]*)"')
    new = []
    share = rel not in SHARE_HOLD

    if not he and share:
        if 'rel="canonical"' not in head:
            new.append(f'<link rel="canonical" href="{url}" />')
        if "og:url" not in head:
            new.append(f'<meta property="og:url" content="{url}" />')
        if "og:description" not in head and desc_raw is not None:
            new.append(f'<meta property="og:description" content="{desc_raw}" />')
    image = attr(head, r'<meta property="og:image" content="([^"]*)"')
    if not he and share:
        slug = os.path.basename(rel)[:-5]
        card = os.path.join(ROOT, "images", "cards", f"card-{slug}.webp")
        if image is None:
            image = SITE + f"/images/cards/card-{slug}.webp" if os.path.exists(card) else DEFAULT_IMAGE
            new.append(f'<meta property="og:image" content="{image}" />')
        if "og:site_name" not in head:
            new.append('<meta property="og:site_name" content="Aryeh Leib Toren" />')
        if "twitter:card" not in head:
            kind = "summary" if image.endswith("/images/aryeh.jpg") else "summary_large_image"
            new.append(f'<meta name="twitter:card" content="{kind}" />')
        if "twitter:site" not in head:
            new.append('<meta name="twitter:site" content="@ALThorne_Toren" />')

    p = path_of(rel)
    twin_en, twin_he = (pairs.get(p), p) if he else (p, en_to_he.get(p))
    if twin_en and twin_he and "hreflang" not in head:
        new += [f'<link rel="alternate" hreflang="en" href="{SITE + twin_en}" />',
                f'<link rel="alternate" hreflang="he" href="{SITE + twin_he}" />',
                f'<link rel="alternate" hreflang="x-default" href="{SITE + twin_en}" />']

    if "application/ld+json" not in head:
        obj = {"@context": "https://schema.org", "@type": "BlogPosting", "mainEntityOfPage": url}
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S)
        if h1:
            title = " ".join(html.unescape(re.sub(r"<[^>]+>", "", h1.group(1))).split())
            if title and len(title) <= 110:
                obj["headline"] = title
        if desc_raw and share:
            obj["description"] = html.unescape(desc_raw)
        if image and share:
            obj["image"] = image.replace("https://aryeh-leibt.github.io", SITE)
        dp, dm = published(text, rel), git("log", "-1", "--format=%cs", "--", rel)
        if dp:
            obj["datePublished"] = dp
        if dm:
            obj["dateModified"] = dm
        obj["inLanguage"] = "he" if he else "en"
        obj["author"] = {"@type": "Person", "@id": PERSON_ID, "name": "Aryeh Leib Toren", "url": SITE + "/"}
        obj["publisher"] = {"@id": PERSON_ID}
        new += jsonld(obj)

    if not new:
        return False
    block = "".join("    " + line + "\n" for line in new)
    i = text.index("</head>")
    line_start = text.rfind("\n", 0, i) + 1
    text = text[:line_start] + block + text[line_start:]
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    return True


def essays():
    out = []
    for name in sorted(os.listdir(os.path.join(ROOT, "writing"))):
        rel = "writing/" + name
        if name.endswith(".html") and rel not in NOT_ESSAYS:
            out.append(rel)
    hedir = os.path.join(ROOT, "he", "writing")
    for name in sorted(os.listdir(hedir)):
        if os.path.isfile(os.path.join(hedir, name, "index.html")):
            out.append(f"he/writing/{name}/index.html")
    return out


def main():
    pairs = he_en_pairs()
    en_to_he = {en: he for he, en in pairs.items()}
    targets = sys.argv[1:] or essays()
    changed = 0
    for rel in targets:
        rel = rel.replace(os.sep, "/").lstrip("./")
        if rel in HOLD or re.match(r"(he/)?elections", rel):
            print(f"skipped (hold/elections): {rel}")
            continue
        if process(rel, pairs, en_to_he):
            changed += 1
    print(f"add-seo-head.py: {changed} page(s) updated")


if __name__ == "__main__":
    main()
