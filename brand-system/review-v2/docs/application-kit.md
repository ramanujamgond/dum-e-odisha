# Applications — review 02

## Portrait social

`../applications/social-portrait.html`: 1080 × 1350 working canvas. Editable headline and caption; logo and artwork are embedded so the source opens offline. The owner-supplied Instagram handle is used. The layout is a design canvas, not a verified current Instagram safe-area specification. Inspect platform cropping before posting. No publishing or scheduling is performed.

Headline limit 42 characters; caption limit 70. The supplied copy is complete brand messaging without a fabricated promotion or menu. Test long lines with the input controls. Proofs include default and long-content states. Print/save-PDF uses an exact-sized CSS page; the delivered screen proof is PNG. A physical printer may scale it and must be checked.

## Order label

`../applications/order-label.html`: 900 × 550 working canvas. Editable dish (48 characters), portion (36), order ID (25), packed time (35), allergens (65). All uncertain fields are visibly bracketed in the default view. Local preview editing does not persist data or transmit it. Replace all placeholders with verified content before customer use.

This is an operational content template. It is not a legally reviewed label, food-safety instruction or printer dieline. No invented certifications, dietary symbols, regulatory number or QR destination appears. Long-content screenshot uses explicitly labeled sample content and must never be treated as an actual dish listing.

## Proof/source contract

HTML sources have live text and embedded raster images; they are editable layouts, not editable-vector artwork. PNGs in `proofs/` are visual exports, not sources. Rebuild HTML with `python3 sources/build-applications.py` after changing canonical imagery. Regenerate proofs with the render script. For missing imagery, keep the logo and operational content and remove the artwork block deliberately; do not leave a broken external image.

All application use is proposed pending owner design approval. Platform publishing and printer production require their own readiness checks.
