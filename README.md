# Dum E Odisha

Brand-design project copied from the Dum E Biryani workspace. The current collection contains 13 identity concepts and 49 application mockups, with earlier design rounds retained.

## View the project

Open `brand/brand-review.html` in a browser, or serve the repository locally:

```sh
python3 -m http.server 8000
```

Then visit `http://localhost:8000/brand/brand-review.html`. Application mockups are in `brand/brand-applications.html`, and previous rounds are linked from `brand/brand-history.html`.

## Included files

The `brand/` directory retains the original HTML guides, artwork, manifests, research, and generation/validation scripts. No deployment configuration is added.

Generated ZIP bundles, Python caches, dependency directories, environment secrets, and build output are excluded from version control. ZIP download links in the guides refer to locally generated bundles and will not work in a fresh clone until those bundles are regenerated. Original ZIPs remain in the source workspace.

To rebuild the current complete bundle, install Pillow in your Python environment and run:

```sh
python3 brand/scripts/complete_applications.py
python3 brand/scripts/validate_complete_applications.py
```

The generation script also rewrites the current guides, manifests, and validation inputs; review those changes before committing. Older bundles have their own historical generation scripts in `brand/scripts/`.

## Validation

The current source collection passed `validate_complete_applications.py` before publication: 616 local references, 147 image instances, and 595 offline archive references, with no errors. This check used the original generated archive, which is intentionally excluded from Git. Browser rendering was not checked in this publication pass.

The replacement commit preserves the repository's prior Git history.
