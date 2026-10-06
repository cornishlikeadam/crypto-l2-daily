# Step 5: Put it on the website

**What starts this step:** Step 3 made a good video (and, for the first video, Step 4 said yes).

**What goes in:** `final.mp4` and the card list.

**What this step does:** `scripts/build_site.py` builds the web pages, then the robot sends them to the internet.

**Directions for the robot:**

1. Copy the video to `site/days/YYYY-MM-DD/`.
2. Rebuild the home page, the day page, the archive page, `feed.json`, and the day's note in this vault ([[archive/README]]).
3. Save a backup to GitHub.
4. Send the website to Vercel.
5. Load the new day's page. Only if it loads, write "LIVE" in `logs/daily.log`.

**Good looks like:** https://not2l8-l2-daily.vercel.app/ shows today's video at the top, with the cards under it.

**Human check:** if the page does not load, the log says "NOT LIVE" and gives the exact command to try again. The robot never says "live" when it isn't.
