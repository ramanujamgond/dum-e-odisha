# Vercel deployment

Target: `ramanujam-gonds-projects/dum-e-odisha` (team `team_csIjLTvLXbtNDPZ0UEZrhky2`).

Static source is pinned to GitHub commit `270f2916f64c14a24ac6180d0e55ee6ba9dfc1e1` in `ramanujamgond/dum-e-odisha`. The build downloads that public commit, copies its brand directory to `public/`, creates a homepage from `brand-review.html`, and reconstructs all eight original ZIP bundles. Every bundle entry is checked by SHA-256 against its original contents. The CLI uploads only this small build package; artwork is fetched during the Vercel build. No paid upgrade is required.

Build: `python3 build.py`. No dependencies or environment secrets are required. For local testing against an existing checkout, set `DUM_E_SOURCE` to its root path.

Before redeploying, verify `vercel whoami --format json`, link explicitly to the target above, and run `vercel project inspect --non-interactive`. Deploy using `vercel deploy --prod --scope ramanujam-gonds-projects --project dum-e-odisha`.

The source commit remains pinned until deliberately updated. This deployment package is saved locally and was not committed to GitHub.
