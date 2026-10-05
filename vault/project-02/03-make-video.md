# Step 3: Make the video

**What starts this step:** Step 2 saves `data/YYYY-MM-DD.json`.

**What goes in:** the checked posts from Step 2.

**What this step does:** `scripts/render.py` asks OpenMontage (a free video maker) to turn the posts into a 70-second card video.

**Directions for the robot:**

1. Make 8 to 10 cards: a title card, one card per post, a "Quiet today" card for any empty coin, and a sources card at the end.
2. On each card show:
   - a big title, like **Monero · FCMP++**;
   - the post's own sentence in quotes;
   - a simple **"What is this?"** line, like "MWEB is Litecoin's optional privacy feature";
   - the source link and the like count, bottom left;
   - the account name and date, bottom right.
3. Read each card out loud with Piper, a free robot voice. If it runs past 70 seconds, read fewer words of each post (the card still shows them all). Never speed the voice up past about 1.15×.
4. Save the video to `OpenMontage/projects/crypto-l2-YYYY-MM-DD/renders/final.mp4`.

**Good looks like:** the video is exactly 70 seconds, 1920×1080, has sound, and every card is readable.

**Human check:** the robot checks the length, the size and the sound by itself. If any of them is wrong, it stops and publishes nothing.
