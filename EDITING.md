# Editing the WaldeComms site

| What | Where | Rebuild? |
|---|---|---|
| Colours | `css/site.css`, the `:root` block on line 4 (`--y` yellow, `--p` pink, `--m` mint, `--i` ink, `--c` cream) | Yes (`python3 build.py`, so files get a new version) |
| Sizes (type, spacing, cards, Niki, header) | the size tokens `:root` block in `css/site.css` (`--fs-h1`, `--sec-pad`, `--card-w`, `--niki-hero` ...) | Yes |
| Words: case studies, quotes, team, bios, nav, email | `content.py` | Yes |
| Coverage clippings | `../coverage/coverage.json` | Yes |
| Page layout, headlines inside page templates | `build.py` | Yes |

Never edit the `.html` files: the next build overwrites them. No hex colours outside `:root` (the header SVGs in `img/` are the only exception).

## Publish
1. Back up first: `git tag backup-$(date +%Y%m%d-%H%M) && git push --tags`
2. `python3 build.py`
3. `python3 qa.py` must print `ALL PASS` (Chromium + WebKit, every page, 1204x753 and 390x844).
4. `git add -A && git commit -m "..." && git push`
5. Wait ~60s for GitHub Pages, then `python3 qa.py https://finlaysonnick74-source.github.io/waldecomms-preview` and look at every screenshot in `../qa/shots/`.

## Why no hard refresh is needed
Every build stamps a version (`VER`, a hash of all CSS/JS/SVG/content) onto every CSS, JS, image and internal link, and CSS `url()` graphics get their own hash. Each page carries no-cache meta tags and a tiny guard that checks the live page's version and swaps to it once if the browser showed an old copy.

## What qa.py guards (each one was a real complaint)
Intro plays on launch, logo replays it, page scrolls after it; every section and Niki fit the screen; nothing wider than the screen; coverage images not repeated; mobile menu solid, tappable, scroll-locked, Escape closes; marquee names on one line; header identical on every page; consistent sizes; no-cache meta and versioned refs on every page; no console errors.
