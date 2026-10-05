# ai-use-log.md

Every run on October 5, 2026, in order. The AI was Claude (Claude Code).

| Date | What I asked the AI to do | What it produced | What I kept, changed, or rejected |
|------|------------------------------|------------------|------------------------------------|
| Oct 5 | Build a daily crypto video robot from my plan | A plan, plus three choices for me (X source, video tool, approval) | Kept. I chose the official X API, Remotion, and a public repo. |
| Oct 5 | Test the whole pipeline with fake posts | A test video with fake accounts (never published) | Rejected the first look: the account name was bigger than the title. The AI made a custom card design. |
| Oct 5 | Run with the official X API | Nothing. I couldn't buy X credits. | Changed plan. |
| Oct 5 | Use my xAI key instead | The AI checked the key: my xAI team was blocked. | Rejected. The AI warned me I had pasted my key in chat, so I should delete it. |
| Oct 5 | Use a free scraper | The robot, using twikit with my X login codes | Kept. I pasted my login code in chat by mistake, logged out to kill it, and used the safe helper script instead. |
| Oct 5 | First real run | Error: "Couldn't get KEY_BYTE indices" | The AI found the cause (Source 2). I installed the fixed copy myself after it checked the code. |
| Oct 5 | Second run | Bitcoin worked, Dogecoin failed (404) | The AI made the robot use one connection for all searches. |
| Oct 5 | Third run: first real cards | 8 cards. See [[outputs/first-run]]. | Rejected 4 cards: a price guess, a "crypto shiller," and two tiny promo accounts. |
| Oct 5 | Tighter filters | 7 cards; Dogecoin "Quiet today" | Kept. See [[outputs/revised-run]]. |
| Oct 5 | Make the video | The voice ran 98 seconds for a 70-second video | Changed: read fewer words aloud, show all words on the card. |
| Oct 5 | Approve and publish | Live on the website | I approved it with `approve_sample.sh`. |
| Oct 5 | Add 3 important archive days | July 22, August 2, September 30, with real posts | Rejected the first try: an October post showed up on old days, plus a government "DOGE" post and fancy-font text. Kept the fixed version. |
| Oct 5 | Add more than a quote to each slide | "What is this?" line, source link, like count | Kept. |
| Oct 5 | Build this Obsidian vault | This folder | Kept. I should rewrite [[intent]] in my own words. |
