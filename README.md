# crypto-l2-daily

A 70-second card slideshow every day at 18:00 America/New_York. Each edition covers the last 24 hours of X posts about Bitcoin L2 (Lightning, Ark, sidechains), Dogecoin, Monero (FCMP++/CARROT) and Litecoin (Lightning/MWEB). Every card names the account behind the post and links to it.

Site: https://cornishlikeadam.github.io/crypto-l2-daily/

## How a run works

`scripts/daily.sh` runs each step in order:

1. **`scripts/collect_x.py`**: searches X for the last 24 hours using `X_BEARER_TOKEN` from `.env`.
   - Drops price calls, giveaways and unlabeled rumors.
   - Writes `data/YYYY-MM-DD.json`.
   - A coin with no surviving post gets "Quiet today." Nothing is invented.
2. **`scripts/render.py`**: drives OpenMontage's `animated-explainer` pipeline.
   - Runs with OpenMontage's own Python, as a separate project.
   - Writes artifacts and checkpoints to `OpenMontage/projects/crypto-l2-YYYY-MM-DD/`.
   - Narrates with Piper TTS.
   - Renders the card deck in `remotion/` through `video_compose` (Remotion, atelier mode).
3. **`scripts/build_site.py`**: copies `final.mp4` into `site/days/YYYY-MM-DD/`, then rebuilds `site/index.html` and `site/feed.json`.
4. **Publish**: commits `site/` and `data/`, pushes, and waits until GitHub Pages serves the new page. A run that can't push says so and prints the push command.

## Approval

`config/pipeline.json` sets `human_approval_default`.

- **`true`** (the first sample): the run stops at OpenMontage's publish gate. To approve the sample, run `scripts/approve_sample.sh YYYY-MM-DD`. This records the approval, flips the setting to `false` and publishes.
- **`false`**: daily runs pass every gate under that standing approval.

## License note

OpenMontage (AGPLv3) lives in `../OpenMontage` and is called, not copied. Nothing from it is vendored here. `remotion/` is original code that depends only on the `remotion` npm packages installed in OpenMontage's composer.
