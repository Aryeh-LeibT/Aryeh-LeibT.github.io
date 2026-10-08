# Aryeh Leib Thorne Toren

Personal site on GitHub Pages: https://aryehleibtoren.com/

- Home, About, Contact, Subscribe, Support the writing
- Writing: `/writing/` is the essay hub (featured essays, with older pieces in `/writing/archive.html`)
- Elections 2026 (`/elections-2026/`) and Torah: Tishrei & Bereishit (`/torah/`)
- Course work from ITC First Steps stage 4 under `/stage4`

Source of the class pages: `Aryeh-LeibT/portfolio_Thorne_Aryeh_stage4` (kept as its own repo).

## The course checklist's "content page"

The course notes list `About.html` and then `content.html`, each with links.
On this site:

- `about.html` / `/about/` is the About page.
- `content.html` is the content page: one list linking every section of the
  site (Writing, Elections 2026, Torah, About, Contact, Subscribe, Support,
  Course), with one line on each. It is linked from the footer of every page
  ("Site contents"), not from the top menu, so the menu stays at 8 links.
- `/writing/` is the essay hub, where the essays themselves are listed.

## How to check links

Before you push a change, run this from the top folder of the repo:

```
python3 scripts/check-links.py
```

It reads every page the site serves (it skips `_held/` and folders that start
with `_` or `.`), follows every internal link and image, and tells you which
ones point to a file that does not exist. "No broken internal links." means
all is well. If it finds broken links it lists each page, line number and
link, and exits with an error, so a GitHub Action can stop a bad merge (the Action file
is not in the repo yet; it needs to be added by someone with workflow permission).
Outside links (https://...) are not checked.

To see the site on your own computer first:

```
python3 -m http.server 8000
```

then open http://localhost:8000/ in a browser. Press Ctrl+C to stop it.
