# Setup guide: how I set it up

This is what I did on October 5, 2026, in order. Anyone can follow it.

## 1. Asked for the robot

I asked Claude Code to build a daily crypto video robot. It showed me a plan and three choices. I picked:

- **where to get posts:** the X API;
- **how to draw the cards:** Remotion;
- **the website:** public.

## 2. The X API didn't work

X wouldn't let me buy credits. My xAI key was blocked too.

> **Lesson:** I pasted my xAI key into the chat. Never do that. Anyone who sees a key can use it. Delete it and make a new one.

## 3. Switched to the free way

The robot logs in to X like a person, using two login codes from my browser.

How to get the codes:

1. In Chrome, go to **x.com** and log in.
2. Right-click the page → **Inspect** → click the **Application** tab.
3. On the left: **Cookies** → **https://x.com**.
4. In the **Filter** box, type `auth_token`. Copy the long text in the **Value** column.
5. In Terminal, run:
   ```bash
   /bin/bash ~/crypto-l2-daily/scripts/set_x_cookies.sh
   ```
6. Paste the code and press Return. Nothing shows on screen; that's on purpose.
7. Back in Chrome, change the filter to `ct0`. Copy that **Value**, paste it in Terminal, and press Return.
8. Terminal says **Saved**.
9. Close the X tab. **Don't click Log out**, because that kills the codes.

> **Lesson:** I pasted a login code in the chat by mistake. I logged out of X to kill it, then got fresh codes.

## 4. Fixed the scraper

X changed its website, which broke the scraper. I installed a fixed copy after Claude checked its code:

```bash
cd ~/crypto-l2-daily && uv pip install --python .venv/bin/python "twikit @ git+https://github.com/unclecode/twikit.git@6a73ab97f4de09f79139f6308c9fb80029a9f5f7"
```

## 5. Made the first video and approved it

```bash
/bin/bash ~/crypto-l2-daily/scripts/daily.sh
```

I watched it, then approved it:

```bash
/bin/bash ~/crypto-l2-daily/scripts/approve_sample.sh 2026-10-05
```

Now it runs by itself every day at 6 PM.

## If something breaks

| What the log says (`~/crypto-l2-daily/logs/daily.log`) | What to do |
|---|---|
| `X rejected the session cookies` | Do step 3 again with fresh codes |
| `Couldn't get KEY_BYTE indices` or `kept refusing ... (404)` | X changed its site again. Ask Claude to find a new scraper fix. |
| `NOT LIVE` | Run the retry command the log gives you |
| Nothing for today | The Mac was asleep at 6 PM. Run `sudo pmset repeat wakeorpoweron MTWRFSU 17:55:00` once, so it wakes at 5:55 PM |

## Add an old day to the archive

```bash
/bin/bash ~/crypto-l2-daily/scripts/backfill.sh 2026-09-01
```

Then add one line to `config/archive_notes.json` saying why the day matters, with a real source.
