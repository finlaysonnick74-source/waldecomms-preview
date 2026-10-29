# DESIGN-RULES: mandatory for every build

**Mandatory.** Every site built from this kit must pass this doc and `RULES.md`. `testing/regress.py` now runs `testing/design_check.py` by default (opt out only with `--no-design`), and a build is not shippable until both are green.

## 0. Universal design principles (published standards, general best practice)
These are general industry standards, not rules from a specific client conversation. A ✔ means `testing/design_check.py` checks it automatically. The remaining rules are on the human review list.

### Accessibility: WCAG 2.2 AA (https://www.w3.org/TR/WCAG22/)
- U1 ✔ **Target size:** interactive targets ≥ 24×24 CSS px (SC 2.5.8, https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum). Kit standard is 44×44, per Apple HIG (https://developer.apple.com/design/human-interface-guidelines/accessibility) and Material's 48dp (https://m3.material.io/foundations/designing/structure).
- U2 ✔ **Reflow:** no horizontal scrolling at 320 CSS px wide (SC 1.4.10, https://www.w3.org/WAI/WCAG22/Understanding/reflow).
- U3 ✔ **Text spacing:** with line-height 1.5, paragraph spacing 2×, letter-spacing .12em and word-spacing .16em, no content is lost or overflows (SC 1.4.12, https://www.w3.org/WAI/WCAG22/Understanding/text-spacing).
- U6 ✔ **Focus visible** on every focusable element (SC 2.4.7) and **not obscured** by sticky headers (SC 2.4.11, https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum).
- **Contrast:** text ≥ 4.5:1, large text ≥ 3:1 (SC 1.4.3), and UI parts/graphics ≥ 3:1 (SC 1.4.11). Checked by `regress.py`.
- U7 ✔ **Motion:** under `prefers-reduced-motion` there are no infinite animations and no parallax (SC 2.3.3, https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions).
- U8 ✔ **Pause, stop, hide:** anything that moves automatically for more than 5s (marquees, carousels, auto-cycling quotes) has a visible pause control (SC 2.2.2, https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide).

### Navigation and menus: W3C WAI-ARIA Authoring Practices (https://www.w3.org/WAI/ARIA/apg/)
- Menu toggles are `<button>` elements with `aria-expanded`, Escape closes the menu, and focus moves into and back out of the open menu. Use the disclosure pattern for site nav, not `role=menu` (https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-navigation/).
- Include a skip link, a single `<nav>` landmark with `aria-label`, and `aria-current="page"` on the current page link.

### Usability: Nielsen Norman Group
- Apply the 10 usability heuristics (https://www.nngroup.com/articles/ten-usability-heuristics/): visibility of system status, consistency and standards, recognition over recall, error prevention, and minimalist design.
- **Hierarchy and scanning:** users scan in F- and layer-cake patterns (https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/). Front-load headings, put the value proposition and primary CTA above the fold (https://www.nngroup.com/articles/scrolling-and-attention/), and give each page one goal. U9 ✔ checks for exactly one `<h1>` per page.
- **Navigation:** keep it visible and short, use labels people already understand, and mark the current location (https://www.nngroup.com/articles/navigation-ia-tips/). Hick's law means fewer choices give faster decisions, so limit top-level nav to about 7 items or fewer (https://lawsofux.com/hicks-law/).
- **Fitts's law:** make primary actions large and close to where users are already looking or tapping (https://lawsofux.com/fittss-law/).
- **Gestalt:** proximity, similarity and alignment (https://www.nngroup.com/articles/gestalt-proximity/). Related items sit closer together than unrelated ones, elements of the same kind look the same, and everything aligns to the grid.
- **Carousels:** auto-rotation hurts usability, so give users control and don't hide key content in later slides (https://www.nngroup.com/articles/designing-effective-carousels/, https://baymard.com/blog/homepage-carousel).

### Layout, spacing and type scale: Material Design 3 and Apple HIG
- **8pt spacing grid** with 4pt for fine steps (M3 https://m3.material.io/foundations/layout/understanding-layout/spacing). All margins, gaps and paddings come from 4/8/16/24/32/48/64/96.
- **Layout grid:** 4 columns on compact, 8 on medium and 12 on expanded widths, with breakpoints near 600 / 840 / 1200 px (M3 window size classes, https://m3.material.io/foundations/layout/applying-layout/window-size-classes). Margins are ≥ 16px on phones and 24px+ on larger screens.
- **Modular type scale:** use a fixed set of display, headline, title, body and label sizes (M3 https://m3.material.io/styles/typography/type-scale-tokens; HIG https://developer.apple.com/design/human-interface-guidelines/typography). Use fluid `clamp()` between the steps and never ad-hoc sizes.
- **Whitespace and balance:** generous whitespace separates groups. Balance visual weight across the layout and leave a clear focal point per section.
- **Mobile-first, responsive images:** author the CSS mobile-first. Use `srcset`/`sizes` or appropriately sized WebP/AVIF, set `width`/`height` to prevent layout shift, and `loading="lazy"` below the fold (https://web.dev/articles/serve-responsive-images). U10 ✔ checks that no image is taller than the viewport.

### Typography: Butterick's Practical Typography (https://practicaltypography.com/)
- U5 ✔ **Body text:** 15–25px on the web (kit minimum 16px), line spacing 120–145% (kit ≥ 1.4) (https://practicaltypography.com/point-size.html, https://practicaltypography.com/line-spacing.html).
- U4 ✔ **Line length:** 45–90 characters, aim for 60–75 (https://practicaltypography.com/line-length.html). The check fails any paragraph over 90ch.
- **Fonts:** at most 2 families (https://practicaltypography.com/font-recommendations.html, https://practicaltypography.com/system-fonts.html). Use real bold and italic weights rather than faked ones, self-host WOFF2 with `font-display:swap`, and avoid all-caps for body text.
- **Consistency:** one style per role across the whole site (heading, link, button, card). This rule also appears in `RULES.md` §5: a fix on one page is applied everywhere.

### Where these came from
The §0 rules are compiled from the public standards linked above (general best practice). Sections 1–8 below came from the kit's own builds and Nick's feedback; each rule there is tagged with its source. When I searched the BuildIT/Tomas transcripts and the Tomas PDFs, they contained no explicit written list of universal design principles. The only design guidance in them is noted under [B]/[C] below and in `tomas-web-basics.pdf` ("Mobile first", plan the layout and site map before code, brand kit: logo, colours, fonts).

## Kit and build-specific rules

Compiled 29 Oct 2026 from rules agreed across the kit and Tomas's first BuildIT build. Before this, the kit had `RULES.md` (content, contrast, interaction, QA) but no single design-system doc. Each rule names its source. `RULES.md` still applies in full; this doc adds the visual system.

Sources: **[R]** `RULES.md` · **[T]** `shared/tokens-light.css` + `starter/css/site.css` · **[B]** BuildIT first build (`/workspace/buildit-new/site.css`, `pages.css`) · **[C]** BuildIT v2 `CONCEPT.md` · **[G]** `REUSE-GUIDE.md` · **[P]** `research/patterns.md` · **[N]** Nick's feedback on WaldeComms, 29 Oct 2026

## 1. Grid and containers
1. One content container per site: `width:min(var(--max), 100% - 40px)` with `--max` 1120–1240px. Never use fixed-px stages. [T][B]
2. Narrow measure for reading blocks: ≤ 800px container; paragraphs ≤ 58–62ch; headlines ≤ 16ch. [B][T]
3. Two-column hero/feature grids collapse to one column at ≤ 900px (secondary breakpoints 760 / 600 / 520). [B][T]
4. Card grids use `repeat(auto-fill,minmax(min(100%,Npx),1fr))` so nothing overflows at 390px. [T]
5. No horizontal overflow at any tested width; long words wrap (`overflow-wrap:anywhere`); tables scroll in their own box. [R]

## 2. Spacing
6. Section rhythm: vertical padding `clamp(64px, 10vw, 110–140px)` desktop; ≥ 56–72px mobile. First section clears the sticky header. [B][T]
7. Spacing steps from a small set (8 / 14 / 16 / 20 / 26 / 30 / 56px); gaps 14–20px for buttons and cards, 56px between hero columns. [B]
8. Header height token (`--hdr` 64–76px desktop, `--hdr-m` ~62px mobile); full-height sections use `calc(100dvh - var(--hdr))`. [T][N]

## 3. Type scale and fonts
9. Body 17–18px, line-height 1.55–1.6. Never below 16px for body copy; 13–15px only for labels/eyebrows/buttons. [T][B]
10. Fluid headings via clamp(): H1 `clamp(34px, 4.6–6vw, 56–100px)`, H2 `clamp(27px, 3vw, 36px)` (display-heavy brands may go larger), H3 ~20–24px. Lead 18–24px. [B][T]
11. Max 2 type families + 1 accent voice (BuildIT: display serif + sans + hand/mono accent). Self-hosted WOFF2 with `font-display:swap`. [C][P][B]
12. Eyebrows/kickers: 13px, weight 700–800, letter-spacing .1–.18em, uppercase. [T][B]
13. Huge display type (8–12vw) is only for one signature moment, and must also be capped by viewport height (`min(vw, vh)`). [P][N]

## 4. Hierarchy
14. One H1 per page; one primary CTA, max one secondary. Primary CTA above the fold at 390x844 and desktop on every page. [R][C]
15. One signature moment per site (an intro, a WebGL hero OR a scrubbed story, not all). [P]
16. Characters/illustrations are secondary to the message: hero character small (BuildIT ≤160–220px column), never pushes the headline or CTA below the fold. [C][B]

## 5. Sizing and viewport fit
17. Everything scales to the viewport: full-screen pieces use `100dvw/100dvh` (with vw/vh fallback); images `max-width:100%; height:auto`. [T][N]
18. No image or character taller than the viewport: cap with `max-height:min(80dvh, section height)` and `object-fit:contain`. [N]
19. Canvas: size from the element's box, devicePixelRatio capped at 2, recomputed on resize (outside the frame loop). [N]

## 6. Colour and contrast
20. Tokens in one `:root`; no stray hex in components. Body text ≥ 4.5:1, large ≥ 3:1. Calm base + one accent unless the brand is deliberately loud. [R][G]

## 7. Interaction, motion and mobile
21. Tap targets ≥ 44x44px (`--btn-h:44px`); visible `:focus-visible`; keyboard usable. [R][T]
22. Motion is transform/opacity only, rAF-driven, skippable intros once per session, all reduced under `prefers-reduced-motion`; scroll is never left locked. [R][C][N]
23. Sticky mobile CTA where booking matters; safe-area aware. [G]
24. `tel:` / `mailto:` links, alt text on every image. [R]

## 8. Testing
25. Test at 1366x768, 1280x800, 390x844 minimum, plus 1440x900, 768x1024 and the client's actual screen for anything full-screen. [R][N]
26. A fix on one page is applied site-wide via shared CSS. Rerun tests against the live URL after deploy. [R]
