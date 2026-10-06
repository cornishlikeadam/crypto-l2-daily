---
number: 8
group: "The 5 steps"
short: "The map"
question: "What is the order of the 5 steps?"
hint: "Input at the start, output at the end. One step has a 'no' path."
answer: "6 PM input → 1 Collect → 2 Check → 3 Make video → 4 Human check → 5 Publish → output. If the human check says no, the robot goes back to step 2."
cssclasses: [l2-daily]
tags: [ai101, project-2, diagram]
---

# 🗺️ The workflow map: Crypto L2 Daily

```mermaid
flowchart LR
    A["⏰ Input: 6 PM, X posts from the last 24 hours"] --> B["🔎 1 · Collect the posts"]
    B --> C["🧹 2 · Check the posts, remove junk"]
    C --> D["🎬 3 · Make the 70-second video"]
    D --> E{"🧑‍⚖️ 4 · Human check (first video only)"}
    E -->|yes| F["🌐 5 · Put it on the website"]
    E -->|no| C
    F --> G["✅ Output: video + cards + course + archive note"]
```

## 🔢 The same map in words

1. ⏰ **Input:** at 6 PM, the robot gets X posts from the last 24 hours.
2. 🔎 **Step 1:** collect the posts.
3. 🧹 **Step 2:** check the posts. Remove the junk.
4. 🎬 **Step 3:** make the 70-second video.
5. 🧑‍⚖️ **Step 4:** I check it. **Yes** → go to step 5. **No** → go back to step 2.
6. 🌐 **Step 5:** put it on the website.
7. ✅ **Output:** the video, the cards, the course pages and the archive note.

> [!tip] 🧩 Open the canvas
> `process-map.canvas` shows the **same 5 steps** in the **same order**. Open it in Obsidian.
