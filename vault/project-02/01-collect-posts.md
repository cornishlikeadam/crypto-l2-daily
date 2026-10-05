# Step 1: Collect the posts

**What starts this step:** the clock hits 6:00 PM (New York time). The Mac's scheduler (cron) runs `scripts/daily.sh`.

**What goes in:** four X searches, one per coin, for the 24 hours before 6 PM:

- Bitcoin: `(Bitcoin OR BTC) (Lightning OR Ark OR "layer 2" OR L2)`
- Dogecoin: `(Dogecoin OR DOGE) ("layer 2" OR L2 OR Dogechain OR community)`
- Monero: `(Monero OR XMR) (FCMP OR CARROT OR hardfork OR upgrade)`
- Litecoin: `(Litecoin OR LTC) (Lightning OR MWEB OR "layer 2")`

**What this step does:** `scripts/collect_x.py` logs in to X with my saved login codes and grabs the top 25 posts for each search.

**Directions for the robot:**

1. Search X once per coin, using one connection for all four searches.
2. Keep only posts with an account name and a date.
3. Save everything it found to `data/raw/YYYY-MM-DD.json` (kept on my Mac only).

**Good looks like:** the log says something like `Bitcoin: 25 posts`, `Dogecoin: 25 posts`, `Monero: 18 posts`, `Litecoin: 9 posts`.

**Human check:** if the log says "X rejected the session cookies," nothing goes forward that day. I get fresh login codes with `scripts/set_x_cookies.sh` (see [[setup-guide]]).
