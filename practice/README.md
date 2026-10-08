# JavaScript practice (course exercises): PRACTICE ONLY

**This branch (`course-js-practice`) must never be merged into `main`.**
GitHub Pages publishes only the `main` branch, so nothing on this branch is
on aryehleibtoren.com. That is the point: it is a safe place to practise.

## What is here

| File | What it is |
| --- | --- |
| `index.html` | The practice page: two exercises, each in its own box. |
| `practice.js` | The JavaScript, with a comment on almost every line. |

The exercises come from the course notebook:

1. **Variables** (page 12): `var myNumber = 3; // a number` and
   `var myString = ...`. The notebook stops after `myString =`, so the file
   uses `"Hello, world"`. Change it to anything you like (keep the quotes).
   The values are printed with `console.log` and also shown on the page.
2. **A button that changes text** (page 13, "JS - change"): clicking the
   button changes the text above it, and clicking again changes it back.

## How to open it on your computer

First get the branch onto your computer:

```
git fetch origin
git switch course-js-practice
```

Then either:

- **Easiest:** double-click `practice/index.html`. It opens in your browser.
  (The page borrows the site's stylesheet with `../css/styles.css`, which
  works from a double-click too.)
- **Like a real web server:** in the top folder of the repo run

  ```
  python -m http.server 8000
  ```

  (or `python3 -m http.server 8000`) and open
  http://localhost:8000/practice/ in your browser. Press Ctrl+C to stop.

To see the `console.log` messages, press **F12** in the browser and click
the **Console** tab. After you edit `practice.js`, save and reload the page.

When you're done, `git switch main` takes you back to the real site.
