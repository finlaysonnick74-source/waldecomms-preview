# testing/: reusable regression kit (Playwright, Python)

One script, one JSON config. Copy this folder into any new build.

## Install (once per machine)
```bash
pip install playwright pillow && python3 -m playwright install chromium
```

## Run in a new build
```bash
cp -r site-starter-kit/testing ./testing
cp testing/config.example.json testing/config.json   # set base_url and the pages list
python3 -m http.server 8099 &                        # or: npm run dev / astro preview / netlify dev
python3 testing/regress.py testing/config.json       # exits 1 if anything fails
python3 testing/regress.py testing/config.json --update-baselines   # accept the current visuals as the new baseline
```
Outputs go to `out_dir`: `report.md` (a pass/fail matrix plus failure details), `results.json`, and one screenshot per page and viewport. Baselines live in `<out_dir>/../baselines/`.

## Config
| key | meaning |
|---|---|
| `base_url` | Server root. Any running server works, including a live site. |
| `pages` | Paths to test. |
| `viewports` | Default `1366x768`, `1280x800`, `390x844`. |
| `cta_selector` | What counts as the primary CTA; at least one must be visible in the first viewport. |
| `require_tel_mailto` | `true` for local-business sites: the page must have both a tel: and a mailto: link. |
| `check_external_links` | Also request off-site links (slower). |
| `ignore_console` | Substrings of console errors or requests to ignore. |
| `min_contrast` | AA threshold for body text (large text automatically uses 3:1). |
| `diff_threshold` | Fraction of pixels allowed to change compared with the baseline. |

## Checks (per page × viewport)
- `loads`: HTTP 2xx/3xx.
- `console_errors`: console errors and uncaught page errors.
- `broken_requests`: any request that fails or returns 4xx/5xx, plus images that fail to decode.
- `broken_internal_links`: every same-origin `<a href>` is requested.
- `horizontal_overflow`: the document is wider than the viewport. Offending elements are listed; elements clipped by overflow:hidden are ignored.
- `tel_mailto_valid`: tel: links use E.164-ish digits; mailto: links contain a valid address.
- `img_alt`: every `<img>` has an alt attribute (`alt=""` is allowed for decorative images).
- `contrast`: WCAG ratio for text on solid backgrounds. Text over images or gradients is counted as "skipped"; use the Innovo gradient-contrast approach for those.
- `cta_above_fold`: at least one CTA intersects the first viewport.
- `forms_wired`: each form has named fields and a submit control. A missing action/Netlify attribute is reported in the detail.
- `visual_diff`: pixel diff against the baseline.

Runs use `reduced_motion: reduce` for deterministic screenshots. That also catches the "content invisible when motion is off" bug.

## Proof runs (27 Oct 2026, see `runs/`)
- `runs/kit`: this repo's gallery and all 19 demos × 3 viewports. The first run found 9 real issues (newsletter form unwired, two 390px overflows) and they're fixed. The final run has 0 failures.
- `runs/bw`: the BuildIT site (`/workspace/bw`, 16 pages × 3 viewports). 10 failures, all `cta_above_fold` at 390px: the header CTA collapses into the mobile menu, so no CTA is visible on first load. The original build was left unchanged.
