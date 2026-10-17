# Validation — review v1, 2026-10-17
## Executed
- Relocation: SHA-256 compared for all 819 files before/after move. Rechecked after improvements: zero original files changed. Git state remains unborn, untracked original folders preserved.
- Original site: 56 legacy HTML pages, 1,097 local file references, zero missing targets. This scan checks file targets, not external availability or every fragment.
- Offline static build: exit 0 using original build.py in a disposable workspace copy with DUM_E_SOURCE pointing to relocated project. All eight ZIP bundles reconstructed with the original build script's per-entry SHA-256 checks. No network fetch and no deployment.
- New SVG assets parsed as XML; logo masters contain paths/shapes, no image embeddings or live text. Applications retain editable text. Mono E knockout uses an SVG mask.
- Sharp rendered primary, mono, reversed, compact, pattern and two application PNGs. Actual pixels visually reviewed in logo-proof-sheet.png, order-label.png and social-portrait.png. Name spelling, DUM/E separation, text clipping and hierarchy accepted for draft review. Compact 16 px is cramped; use 24+ px. Full lockup 160 px is readable in inspected proof; prefer 200+ px.
- Built-in generated illustration inspected: no accidental text, coherent pot/lid, right-weighted composition, useful left whitespace. It is illustrative rather than documentary; colors are not calibrated press inks.
- sRGB contrast calculated from linearized channel luminance: chilli/cream 8.16:1; ink/cream 14.46:1; ink/saffron 7.28:1; saffron/cream 1.99:1. Saffron-on-cream is decoration only, not reading text. These are palette measurements, not whole-site conformance.
- System Arial availability checked under /System/Library/Fonts/Supplemental; no font binary bundled or license inferred.

## Incomplete / blocked
Browser desktop/mobile review: attempted opening file:///Users/string1301/code_den/dum-e-biryani/brand-system/review-v1/index.html in user's Mac Chrome. Denied by browser security policy because file:// protocol is blocked; it did not open. No indirect browser workaround used. Responsive layout, zoom, keyboard flow and browser rendering are unverified. Manually review local HTML before approval.

No physical print proof, CMYK/spot separation, mask-compatibility vendor proof, trademark clearance, customer research, real menu stress test or Odia review. Application placeholders require verified content. New Nano Banana generation blocked on Figma–Weave account linking. Rights and final identity approval are pending.

## Machine evidence
`../../../operations/` contains relocation-verification.json, post-improvement-integrity.json, legacy-link-check.json, offline-build.json and review-validation.json. The reproducible standard-library script is `../sources/validate.py`. Manifest integrity excludes the manifest itself; the validation evidence lives outside the hashed review set.
