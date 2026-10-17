# Logo system — review v1
The new SVGs contain editable paths and geometric shapes, with no embedded image or live font. They are a clean geometric interpretation of the observed lid + separated E + ODISHA hierarchy, not an exact tracing of the serif JPEG.

Files: `assets/logo/primary.svg` (640 × 410), `mono.svg` (same geometry, ink with transparent E counter), `reversed.svg` (cream with chilli E counter), `compact.svg` (32 × 32 icon). All backgrounds are transparent. The mono version uses a vector mask to knock out the E counter. Confirm mask support in vendor software before production.

Minimum reviewed full-name display: 160 CSS px wide; recommended everyday use 200+ px. Below that use the compact icon with the full business name in adjacent text. Icon inspected at 16, 24, 32, 48 px; 16 is identifiable as a lid but cramped, so use 24+ px wherever possible. Do not put the tagline inside the small mark. For print, start at 35 mm full-name width, subject to real substrate proof; this is a recommendation, not a tested print minimum.

Clearspace: at least 24/640 of artwork width around the SVG bounding box; never stretch, rotate the whole logo, bridge DUM to E, recolor by dish, add an outline, or use the illustration as a substitute for the mark. Keep “ODISHA” at the supplied size. The compact symbol alone is not a readable business name.

Source generator: `sources/build_identity.py`; edits regenerate SVGs. Preserve exact SVG paths for reuse. PNGs in proofs are screen exports only. Professional similarity/trademark review has not been performed. Human approval of the new lettering is pending G6.
