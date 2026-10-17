# Dum E Odisha

Start at [Project studio](index.html) or [Current brand guide — review 02](brand-system/review-v2/index.html).

The owner confirmed **Dum E Odisha** and supplied [@dum_e_odisha](https://www.instagram.com/dum_e_odisha/). The current proposal pairs warmer serif lettering with gouache/pencil-style generated food imagery. Nano Banana MCP supplied the logo and packaging study; built-in image generation supplied the food illustration. New work is prepared for review, not labeled owner-approved or print-ready.

## Project map

| Folder | Contents / use |
|---|---|
| `brand-system/review-v2/explorations/` | Three new logo directions, current-identity mockups, Odia/Hindi font lab, wall concepts and banner/TV/poster exports |
| `brand-system/review-v2/assets/` | Current logo PNGs, illustration originals/WebP, guide CSS and JS |
| `brand-system/review-v2/applications/` | Portable editable social and order-label HTML; live fields and print controls |
| `brand-system/review-v2/data/` | Canonical business profile and separate researched candidates; unknown operations remain null |
| `brand-system/review-v2/docs/` | Toolkit outputs, public research, guidelines and handover |
| `brand-system/review-v2/sources/` | Generation prompts, export/build/render/check scripts |
| `brand-system/review-v2/proofs/` | Browser screenshots, export proofs and measured checks; not source artwork |
| `brand-system/review-v1/` | Earlier geometric vector proposal, retained for comparison |
| `brand/` | Historical studies, thirteen directions, research and bundles; paths preserved |
| `deployment-vercel/` | Older pinned static build package; not switched to this proposal |
| `operations/` | Relocation and integrity evidence |

The archive stays in place to keep cross-links and bundle reconstruction intact. Current work is separated by version, source type and purpose. Historical filenames containing “final” do not establish owner approval.

## Preview and rebuild

Open HTML directly or run `python3 -m http.server 8765 --bind 127.0.0.1` from this folder and visit `http://127.0.0.1:8765/`. Application HTML contains embedded artwork and makes no external network calls.

```sh
node brand-system/review-v2/sources/export-assets.cjs
node brand-system/review-v2/sources/export-dum-club.cjs
python3 brand-system/review-v2/sources/build-dum-club.py
node brand-system/review-v2/sources/render-dum-club.cjs
python3 brand-system/review-v2/sources/build-applications.py
python3 brand-system/review-v2/sources/build-doc-pages.py
python3 brand-system/review-v2/sources/build-explorations.py
python3 brand-system/review-v2/sources/build-food-round.py
node brand-system/review-v2/sources/render-food-round.cjs
node brand-system/review-v2/sources/render-explorations.cjs
node brand-system/review-v2/sources/render.cjs
python3 brand-system/review-v2/sources/validate.py
```

Node scripts use existing Sharp/Playwright in this machine's bundled runtime. Set `DUM_E_NODE_MODULES` to another module directory when needed. Renderer uses installed Google Chrome; override `DUM_E_BROWSER` or `DUM_E_BASE_URL` as needed. No global dependencies are installed by this task. Python validation needs only the standard library. After intentional artifact changes, refresh hashes with `python3 brand-system/review-v2/sources/validate.py --refresh-manifest`, then validate again.

## Readiness and recovery

See [handover](brand-system/review-v2/docs/handover-manifest.md), [validation](brand-system/review-v2/docs/validation-report.md) and [decisions](brand-system/review-v2/docs/decision-log.md). Logo exports are transparent **raster** PNGs; vector reconstruction and physical print proof remain production tasks. A fresh browser read of the owner-linked Instagram bio confirmed Bhubaneswar, catering/bulk orders and +91 78942 65632; that phone matches Zomato and connects the researched listings. The sourced profile includes contact/location records, with current menu, hours, prices and allergens still unresolved. No operational facts were invented.

Relocated 2026-10-17 from `/Users/string1301/Documents/ChatGPT/Dum E Biryani`; original 819-file inventory: `operations/relocation-verification.json`. The project is versioned on the main branch with origin at https://github.com/ramanujamgond/dum-e-odisha.git. Historical relocation records describe the earlier uncommitted state. Generated ZIP download bundles remain local and must be regenerated in a fresh clone; source designs are included in Git.

Latest exploration: [four food-brand directions](brand-system/review-v2/explorations/round-02/index.html), based on the owner-supplied Dribbble and Behance screenshots. Each includes a standalone logo, a coordinated brand board, palette, graphic rules and tradeoffs. Earlier directions remain available.

Focused owner-reference refinement: [The Dum Club, refined](brand-system/review-v2/explorations/dum-club-refinement/index.html). Retains the original rounded lettering, lid, rice cue and saffron/chilli palette. Includes faithful and negative-space alternatives, measured golden-ratio name-line layout, one-ink/reverse proofs, packaging, wall and TV applications. The construction diagram is not a vector logo.


Latest owner-requested experiments: [image-only Handi Host and mixed Hindi/Odia logos](brand-system/review-v2/explorations/round-03/index.html). Rebuild with `python3 brand-system/review-v2/sources/build-symbol-script-round.py`, then export and check with `node brand-system/review-v2/sources/render-symbol-script-round.cjs`. The mixed-script pages offer initial, middle and final-word variants and preserve actual Unicode text in licensed local fonts.
