# Brief and evidence-led gap audit
Review v1 · 2026-10-17

Goal: make the name consistently recognizable and make the project usable by someone preparing a label, social post or future website. Success is a clearly named entry page, editable logo sources, correct monochrome/reversed variants, intact existing links, evidence-tagged copy and a recoverable old project.

## Evidence ledger
| ID | Observed evidence / source | Limitation | Design consequence |
|---|---|---|---|
| E1 | `brand/research/final-direction-research.md`, Decision: “The name must read Dum E Odisha.” | Local authored recommendation; original owner approval not attached | Retain name; do not infer a rename from folder name |
| E2 | `brand/final-design/manifest.json`: revision 06, high-resolution opaque JPEGs, not vector | “Final” is not an approval record | Preserve visual equity; create true editable geometry |
| E3 | Actual pixels in final logo: chilli DUM, distinct E tile, ODISHA, lid and tagline | Raster texture and typography are not technical specifications | Keep word separation and palette; remove text dependency from logo |
| E4 | `brand/brand-review.html` presents 13 routes and many historical rounds | A discovery gallery is not an operational asset index | Add a new root review entry and explicit legacy link |
| E5 | `deployment-vercel/build.py` fetches pinned commit; local override exists | Public site will not change when local sources change | Preserve deployment package and run offline override in disposable copy |
| E6 | `.git/config`, status and log inspected: no remote, unborn master, brand and deployment untracked | This is not the remote GitHub history | Preserve .git exactly; do not imply a committed backup exists |
| E7 | Existing manifests attribute some imagery to Nano Banana MCP | No present-generation execution evidence or full terms attached | Keep provenance attribution; no blanket licensing clearance |
| E8 | All 819 original files hashed before/after move; exact match | File integrity, not validation of business claims | Relocation accepted technically |

All evidence inspected 2026-10-17 from local files. Paths above are relative to project root. Inference: takeaway packaging and digital discovery are relevant because the source kit already contains those applications. Validate priority with owner. Unknown: customer motivations, recipes, sourcing, allergens, delivery operations and legal registrations.

## Prioritized gaps and resolutions
P0 name / approval ambiguity: preserve Dum E Odisha; all new files marked review. Pending owner approval explicitly recorded.
P0 production master: new font-independent path SVGs replace the need to trace a JPEG, but remain a proposed typographic refinement.
P1 navigation: add root index, review-v1 hierarchy, source/proof separation and asset manifest. Keep legacy tree stable so 13 concept pages and ZIP reconstruction remain recoverable.
P1 practical copy: replace unsubstantiated sales claims with category, real placeholders and service language that admits unknowns.
P1 rights: item-level ledger; no fonts bundled. New generated illustration labeled editorial rather than actual food.
P1 validation: size proofs, palette calculations, local link scan, SVG structure and offline build recorded in validation report.
P2 owner/vendor work: confirm menu and audience, test with customers, obtain print proof and check rights before release. These are not claimed complete.

Recovery: old assets stay in `brand/`; the old parent path is recorded in the relocation manifest. Do not automatically delete previous rounds. New files can be removed without rewriting the original asset tree.
