---
number: 18
group: "Extras"
short: "Setup guide"
question: "How do I set it up, click by click?"
hint: "There are 5 steps. Step 3 is about 2 login codes."
answer: "Ask for the robot. The X API did not work, so switch to the free scraper. Save 2 login codes with the helper script. Install the fixed scraper. Make the first video and approve it."
cssclasses: [l2-daily]
tags: [ai101, project-2, setup]
---

# 🛠️ Setup guide: how I set it up

> [!info] 📅 When
> I did this on **October 5, 2026**, in this order. **Anyone** can follow it.

## 1️⃣ Ask for the robot

I asked Claude Code to build a daily crypto video robot. It showed me a plan and **3 choices**. I picked these:

- 📡 **Where to get posts:** the X API.
- 🖼️ **How to draw the cards:** Remotion.
- 🌐 **The website:** public.

## 2️⃣ The X API did not work

X did **not** let me buy credits. My xAI key was **blocked** too.

> [!warning] 🔑 Lesson: never paste a key in a chat
> I pasted my xAI key into the chat. **Do not do that.** Anyone who sees a key can use it.
> **Do this:** delete the key. Make a new one.

## 3️⃣ Switch to the free way

The robot logs in to X **like a person**. It uses **2 login codes** from my browser.

**Get the codes:**

1. 🌐 In Chrome, go to **x.com**. Log in.
2. 🖱️ Right-click the page. Click **Inspect**. Click the **Application** tab.
3. 🍪 On the left, click **Cookies**. Then click **https://x.com**.
4. 🔎 In the **Filter** box, type `auth_token`. Copy the long text in the **Value** column.
5. 💻 In Terminal, run this command:
   `/bin/bash ~/crypto-l2-daily/scripts/set_x_cookies.sh`
6. 📋 Paste the code. Press **Return**. Nothing shows on the screen. This is correct.
7. 🔁 In Chrome, change the filter to `ct0`. Copy that **Value**. Paste it in Terminal. Press **Return**.
8. ✅ Terminal says **Saved**.
9. ❌ Close the X tab. **Do not click Log out.** Log out kills the codes.

> [!warning] 🍪 Lesson: keep login codes secret
> I pasted a login code in the chat by mistake. I logged out of X to kill it. Then I got fresh codes.

## 4️⃣ Fix the scraper

X changed its website. This broke the scraper. Claude checked the code of a **fixed copy**. Then I installed it:

```bash
cd ~/crypto-l2-daily && uv pip install --python .venv/bin/python "twikit @ git+https://github.com/unclecode/twikit.git@6a73ab97f4de09f79139f6308c9fb80029a9f5f7"
```

## 5️⃣ Make the first video and approve it

1. ▶️ Make the video:
   `/bin/bash ~/crypto-l2-daily/scripts/daily.sh`
2. 👀 Watch it.
3. ✅ Approve it:
   `/bin/bash ~/crypto-l2-daily/scripts/approve_sample.sh 2026-10-05`

> [!success] 🎉 Done
> Now it runs **by itself** every day at **6 PM**.

## 🚑 If something breaks

The log is `~/crypto-l2-daily/logs/daily.log`.

| 📜 What the log says | 🔧 What to do |
|---|---|
| `X rejected the session cookies` | Do step 3 again with **fresh codes**. |
| `Couldn't get KEY_BYTE indices` or `kept refusing ... (404)` | X changed its site again. Ask Claude to find a **new scraper fix**. |
| `NOT LIVE` | Run the **retry command** that the log gives you. |
| Nothing for today | The Mac was **asleep** at 6 PM. Run `sudo pmset repeat wakeorpoweron MTWRFSU 17:55:00` **one time**. Then the Mac wakes at 5:55 PM. |

## 🗂️ Add an old day to the archive

1. Run this command:
   `/bin/bash ~/crypto-l2-daily/scripts/backfill.sh 2026-09-01`
2. Add **1 line** to `config/archive_notes.json`. Say **why** the day matters. Give a **real source**.
