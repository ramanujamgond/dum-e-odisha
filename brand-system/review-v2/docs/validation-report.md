# Validation — review 02

Executed 17 October 2026 against actual files. This is a focused technical and visual review, not whole-product accessibility certification or customer research.

## Performed

- Chromium/Playwright rendered the guide at 1440 px, 390 px and 320 px widths. All had no horizontal page overflow. Full-page and hero screenshots are in `../proofs/`.
- Browser console/page errors and HTTP responses were monitored; no page exceptions or failed local resource requests were reported in the final run.
- Default social and label HTML were opened and their actual artboards captured. A longer 42-character dish name and a multi-line sample allergen string were edited and captured; the measured label canvas did not overflow. A longer social heading/caption was edited; its heading did not overlap the illustration. These are specific samples, not proof that every possible string will fit.
- The comparison disclosure opened, palette copying produced a status message, and all guide images had alt attributes. Keyboard focus visibility, named controls, skip navigation and native disclosure semantics are implemented. Keyboard Tab reached the skip link and Enter reached #main. At 320 CSS px the guide had no horizontal overflow; this is a narrow reflow check, not a full 400% zoom audit.
- Reduced-motion emulation returned `scroll-behavior: auto`. No autoplay or decorative animation exists.
- Raster variants and avatar were rendered and inspected. A clipped first avatar crop was corrected to include the whole symbol. The earlier stretched-image mobile layout was corrected by giving images responsive automatic height. Final screenshots reflect the corrected geometry.
- Local links, HTML anchors, CSS imports, JSON structure, owner-confirmed data, archive hashes, review-01 hashes and current review checksums are checked by `../sources/validate.py`. Its output is `../proofs/validation.json`.

Browser evidence: `../proofs/browser-checks.json`. Size/variant proof: `../proofs/logo-size-sheet.png`. Sources and exports are not represented as equivalent formats.

## Palette rules

WCAG relative-luminance calculations are recorded in validation.json. Chilli/cream, ink/cream, ink/saffron, leaf/cream and muted/cream are tested against 4.5:1 for ordinary text. Saffron/cream is measured but intentionally excluded from permitted text use because it fails that threshold. The textured illustration and logo are not ordinary body text; palette contrast alone does not validate every visual element.

## Visual judgment

The complete name reads clearly at application size; the gap before E remains visible in all colour variants. Small-size references are reviewed at 180 and 240 px. Use the lid rather than full name for compact spaces. Drawings have visible pencil/brush texture, an intelligible pot and lid, and no stray text. The food art includes chicken-like forms and must not stand in for a verified vegetarian menu item. Packaging preview is visually coherent but generated lettering/perspective is an approximation, not production artwork.

## Not run / next owner

Human disability/usability testing, consumer preference testing, market distinctiveness and professional trademark checks were not run. Neither were printer proofs, ink separations, substrate/grease testing, supplier dieline validation or regulated food-label approval. Current Instagram crop/safe areas were not verified from platform documentation. Later Odia/Hindi specimens were rendered with four local Noto fonts and checked for font loading and exact Unicode text preservation. Native linguistic suitability is not validated. Logo vectors are not delivered. Current menu, hours and operational availability remain unverified. The identity bridge was established through the owner-linked Instagram bio phone matching Zomato; the source evidence is in data/instagram-access.json. Owner approves the visual direction; a designer/printer handles the next production stage.

## HTML reading pages

All 17 source documents have static HTML reading pages, plus a brand-library index. Browser checks opened all 18 pages directly through file URLs at 1440, 390 and 320 px. No page overflow, missing main headings, Markdown destination links, page errors or failed resources were observed. Research tables scroll inside their container on mobile. Keyboard skip navigation reached the article. Evidence: `../proofs/document-checks.json`; visual captures: `document-desktop.png`, `document-mobile.png` and `document-library.png` in proofs. Rebuild with `python3 sources/build-doc-pages.py`; source documents remain available for maintenance.

## Idea and display extension

Browser evidence for the idea collection, four route pages, reference study and font lab is in `../explorations/proofs/browser-checks.json`. Twelve display canvases are exported from actual HTML compositions. The type lab loads four local Noto faces and switches the Odia/Hindi specimens between serif and sans. Generated wall mockups and logo sketches are separate from these exact typeset proofs. The original current logo has not been replaced.

## Food-brand round 02 evidence

The new food-brand collection uses four standalone logos and four applied identity boards. Actual image dimensions, reading-page checks at 1440/390/320 px, and changed-index link checks are recorded in `../explorations/round-02/proofs/browser-checks.json`. A first mascot study used low-contrast yellow for DUM E; the kept revision makes the whole name deep blue while retaining yellow only in the bowl. The earlier image is preserved as study-01. Palette text pairings measured for the HTML: blue/cream 9.87:1, red/cream 5.42:1, dark forest/cream 11.36:1 and editorial forest/cream 9.42:1. Accent labels use very dark ink, including 4.8:1 on terracotta. These digital palette checks do not certify generated raster art or printed materials.

## Dum Club focused refinement evidence

The actual source-shape exports and φ-layout measurements are recorded in ../explorations/dum-club-refinement/sources/geometry.json. Main-name/ODISHA image widths are 1000/618 px, producing 1.618122977 after rounding, a 0.0055% relative difference from φ. Clearspace is 90 px and line gap 56 px, rounded from the declared unit rules. This measures placed raster components, not idealized glyph curves. Two-ink, mono, reversed and 240/180 px size proofs are provided; the small example is a stress inspection rather than a print minimum. Browser results, selection-control checks, image loading and TV-panel measurements are saved in that family’s proofs/browser-checks.json. Generated wall/packaging pixels are application concepts, not proof of exact logo reproduction, physical installation or production readiness.

The final Dum Club browser run passed at 1440, 390 and 320 px with no horizontal overflow, missing image alt attributes or failed local resources. Both variant selectors update the corresponding PNG download. The editable TV heading accepts changes. The TV split measured 1186.625 and 733.375 CSS px, yielding 1.618033066:1. Export cleanup removes warm-paper specks from the one-ink ODISHA line while retaining the source letter forms; the original generated source and inspection crop remain available.


## Round 03 / pictorial and mixed-script checks

The local Chrome renderer exported eight transparent 1600 × 700 logo compositions and one 1600 × 900 editable display proof. All exact Unicode strings matched the recorded script matrix; bundled Hindi/Odia serif fonts loaded and no name spans or illustration bounds clipped. Five reading pages passed 1440, 390 and 320 px viewport checks with no horizontal overflow, missing image alt text or browser request/script errors. Six placement selections correctly updated the reading, pressed state, preview, download and editable-source link. The display headline is editable and the keyboard skip link receives focus. Root, main guide and exploration hub all link to the new collection.

The original pictorial PNG is 1254 × 1254 with actual alpha values spanning 0–255. The Nano Banana stamp interpretation is 1024 × 1024 on white, although 2K was requested. Original and simplified symbol were inspected at 128/96/48 px: the 48 px image retains a recognisable pot/lid silhouette but loses face/rice detail. The preferred raster starting size is at least 96 px for the stamp. These observations do not establish a physical-print minimum.

Evidence: [browser report](../explorations/round-03/proofs/browser-checks.json), [small-size proof](../explorations/round-03/proofs/small-size-proof.png), [desktop collection](../explorations/round-03/proofs/index-desktop.png), [mobile collection](../explorations/round-03/proofs/index-mobile.png). Colour master, stamp interpretation, Hindi and Odia primary exports and the reference crops were visually inspected. No native-reader, trademark, vector-contour or physical production verification is claimed.
