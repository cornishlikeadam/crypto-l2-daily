# decision-note.md

## The gap I found

My rule was "never invent a launch, partnership, or price." The first run didn't invent anything, but it **picked bad posts**: a price guess ("$CATE … will go to billion"), a self-described "crypto shiller," and tiny promo accounts.

Then the archive run showed a bigger gap. I asked for posts from July 22, and X sent back a Monero post from **October 5**. The robot trusted X's date filter, so a July video would have shown October news.

## What I changed

- In `scripts/collect_x.py`:
  - added rules that throw out other-coin tickers, market-cap guesses, "shill/NFA/DYOR" bios, posts with fewer than 5 likes, and accounts with fewer than 500 followers;
  - added a strict date check: the post's own date must be inside the 24 hours, or it's thrown out;
  - added a rule for the government "DOGE" office;
  - turned fancy fonts into normal letters;
  - removed copies.
- In `scripts/render.py`: the voice now reads fewer words of each post so it fits 70 seconds, and the card still shows the whole sentence.
- On every slide: a "What is this?" line, the source link, and the like count.

## Why

My intent says the AI must not decide what counts as news. Price hype and wrong-day posts are exactly the mistakes a viewer would believe. The date check protects the most basic promise: "the last 24 hours."

## What improved

- First run: 4 of 8 cards were bad. Revised run: none of the cards are price talk or ads (see [[outputs/first-run]] and [[outputs/revised-run]]).
- Archive days: 45 wrong-day posts were caught and removed across July 22, August 2, and September 30.

## What's unresolved

- **Words with two meanings:** "Lightning Lake" (a fishing trip) still counts as Bitcoin Lightning, because the robot matches words, not meaning.
- **Big news can be missed:** the biggest news of a day isn't always the most-liked post. On July 22 the Wavelength post made it; on September 30 the DogeOS post did not.
- **X can break the scraper:** this happens every few weeks. When it does, no video gets made that day.

## What stayed mine

- Choosing the free scraper, knowing X could limit my account.
- Choosing which three past days matter, each backed by a real source.
- Approving the first video before anything went public.

## What I would encode as a rule

**Never trust a website's date filter. Check every item's own date before you use it.**
