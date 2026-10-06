# crypto-l2-daily

A 70-second card slideshow every day at 18:00 America/New_York. Each edition covers the last 24 hours of X posts about Bitcoin L2 (Lightning, Ark, sidechains), Dogecoin, Monero (FCMP++/CARROT) and Litecoin (Lightning/MWEB). Every card names the account behind the post and links to it.

Site: https://not2l8-l2-daily.vercel.app/ (archive with every video: https://cornishlikeadam.github.io/crypto-l2-daily/)

## How a run works

`scripts/daily.sh` runs each step in order:

1. **`scripts/collect_x.py`**: searches X for the last 24 hours. Free route: an X account's browser cookies (`X_AUTH_TOKEN`, `X_CT0` in `.env`) with the open-source twikit library. Paid route: `X_BEARER_TOKEN`.
   - Drops price calls, giveaways and unlabeled rumors.
   - Writes `data/YYYY-MM-DD.json`.
   - A coin with no surviving post gets "Quiet today." Nothing is invented.
2. **`scripts/render.py`**: drives OpenMontage's `animated-explainer` pipeline.
   - Runs with OpenMontage's own Python, as a separate project.
   - Writes artifacts and checkpoints to `OpenMontage/projects/crypto-l2-YYYY-MM-DD/`.
   - Narrates with Piper TTS.
   - Renders the card deck in `remotion/` through `video_compose` (Remotion, atelier mode).
3. **`scripts/build_site.py`**: copies `final.mp4` into `site/days/YYYY-MM-DD/`, then rebuilds `site/index.html` and `site/feed.json`.
4. **Publish**: commits `site/` and `data/` to `main` (backup), pushes `site/` to `gh-pages` (full archive), deploys the last 14 days to Vercel, and waits until the new page answers. A run that can't push or deploy says so and prints the command to retry.

## Approval

`config/pipeline.json` sets `human_approval_default`.

- **`true`** (the first sample): the run stops at OpenMontage's publish gate. To approve the sample, run `scripts/approve_sample.sh YYYY-MM-DD`. This records the approval, flips the setting to `false` and publishes.
- **`false`**: daily runs pass every gate under that standing approval.

## License note

OpenMontage (AGPLv3) lives in `../OpenMontage` and is called, not copied. Nothing from it is vendored here. `remotion/` is original code that depends only on the `remotion` npm packages installed in OpenMontage's composer.
