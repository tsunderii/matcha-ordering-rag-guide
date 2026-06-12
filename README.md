# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

Beginner’s guide to ordering matcha at specialty tea cafes — this system covers practical knowledge for people who are new to matcha and want to understand how to order matcha drinks from modern tea shops and boba-style cafes. This includes common drink types, sweetness levels, milk choices, cheese foam or cream toppings, iced vs. hot matcha, matcha quality, flavor profiles, and popular customizations.

This knowledge is valuable because specialty tea cafe menus often include matcha drinks with unfamiliar terms such as matcha latte, matcha cloud, jasmine matcha, salted cheese, ceremonial matcha, or culinary matcha. Official menus usually list drink names, ingredients, and prices, but they do not always explain what the drink tastes like, whether it is beginner-friendly, how strong the matcha flavor is, or how customers customize it. An unofficial guide can combine cafe menus, tea education articles, reviews, and community discussions to help beginners make better ordering decisions.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

Paste this into your `README.md`:

```txt
| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Molly Tea Menu | Official cafe menu | https://www.mollytea.co.th/en/menu/ |
| 2 | Molly Tea Bellevue Delivery Menu | Delivery menu / item descriptions | https://www.grubhub.com/restaurant/molly-tea-bellevue-103-bellevue-way-northeast-bellevue/13106344 |
| 3 | Molly Tea San Gabriel Delivery Menu | Delivery menu / item descriptions | https://www.grubhub.com/restaurant/molly-tea-425-w-valley-blvd-san-gabriel/12261624 |
| 4 | HEYTEA Cloud Matcha Latte Menu Page | Menu page / drink details | https://theheyteamenu.us/cloud-matcha-latte/ |
| 5 | HEYTEA Supreme Matcha Latte Menu Page | Menu page / drink details | https://theheyteamenu.us/supreme-matcha-latte/ |
| 6 | Reddit r/MatchaEverything: HEYTEA’s matcha discussion | Forum discussion / customer opinions | https://www.reddit.com/r/MatchaEverything/comments/1las3u9/i_might_get_roasted_for_this_but_i_think_heyteas/ |
| 7 | Reddit r/bubbletea: HEYTEA favorite bubble tea spot discussion | Forum discussion / customer opinions | https://www.reddit.com/r/bubbletea/comments/1kz2jgp/heytea_is_my_favorite_bubble_tea_spot_whats_yours/ |
| 8 | Reddit r/MatchaEverything: Sweet tasting matcha powders for beginners | Forum discussion / beginner matcha opinions | https://www.reddit.com/r/MatchaEverything/comments/1j9bw6b/sweet_tasting_matcha_powders_for_beginners/ |
| 9 | Food & Wine: Ceremonial Grade Matcha Doesn’t Actually Exist in Japan | Article / matcha quality explanation | https://www.foodandwine.com/ceremonial-vs-culinary-matcha-8641415 |
| 10 | Ikimatcha: Which Matcha to Buy? Ceremonial vs Culinary | Article / matcha grade guide | https://ikimatcha.co/blogs/news/which-matcha-to-buy |
```


---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
