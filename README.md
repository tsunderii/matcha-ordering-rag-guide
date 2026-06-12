# The Unofficial Guide to Ordering Matcha — Project 1

## Project Overview

The Unofficial Guide to Ordering Matcha is a Retrieval-Augmented Generation (RAG)
system that answers beginner questions about ordering matcha drinks at specialty
tea and boba cafes. Rather than relying on a language model's general knowledge, the
system grounds every answer in a small, curated corpus of cafe menus, delivery
listings, community discussions, and matcha-education articles. A user question is
embedded, matched against a vector store of document chunks, and answered by an LLM
that is instructed to use only the retrieved text — or to decline when the corpus
does not cover the question. The goal is a guide that is both genuinely helpful to
newcomers and transparent about where its answers come from.

---

## Domain

Beginner’s guide to ordering matcha at specialty tea cafes — this system covers practical knowledge for people who are new to matcha and want to understand how to order matcha drinks from modern tea shops and boba-style cafes. This includes common drink types, sweetness levels, milk choices, cheese foam or cream toppings, iced vs. hot matcha, matcha quality, flavor profiles, and popular customizations.

This knowledge is valuable because specialty tea cafe menus often include matcha drinks with unfamiliar terms such as matcha latte, matcha cloud, jasmine matcha, salted cheese, ceremonial matcha, or culinary matcha. Official menus usually list drink names, ingredients, and prices, but they do not always explain what the drink tastes like, whether it is beginner-friendly, how strong the matcha flavor is, or how customers customize it. An unofficial guide can combine cafe menus, tea education articles, reviews, and community discussions to help beginners make better ordering decisions.

---

## Document Sources

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

Each source is saved as a plain `.txt` file in `data/raw/`, copied from the page above. Live scraping is intentionally avoided; the local-file approach keeps ingestion reproducible and easy to inspect.

---

## Architecture Summary

The system is a five-stage RAG pipeline:

1. **Document Ingestion** (`ingest_and_chunk.py`) loads every `.txt` file from `data/raw/` into a consistent in-memory structure.
2. **Cleaning & Chunking** strips HTML tags, unescapes entities (e.g. `&amp;`, `&#39;`, `&nbsp;`), removes navigation/footer/cookie boilerplate, then splits each document into ~500-character chunks with 100-character overlap, preferring paragraph and sentence boundaries so menu items and review comments stay intact. Chunks are written with metadata to `data/processed/chunks.json`.
3. **Embedding & Vector Store** (`embed_and_retrieve.py`) encodes each chunk with the `all-MiniLM-L6-v2` sentence-transformer and stores the vectors, text, and metadata in a persistent ChromaDB collection configured for cosine distance.
4. **Retrieval** embeds the user query with the same model and returns the top `k = 4` nearest chunks, each carrying its source filename, chunk index, and distance score for attribution.
5. **Grounded Generation** (`query.py`) formats the retrieved chunks as labeled context and sends them, with a strict system prompt, to the Groq `llama-3.3-70b-versatile` model. A Gradio interface (`app.py`) exposes the whole pipeline as a question box that returns an answer plus the source files used.

```
Document Ingestion → Cleaning & Chunking → Embedding + Vector Store → Retrieval → Grounded Generation → Gradio UI
```

---

## Chunking Strategy

**Chunk size:** ~500 characters.

**Overlap:** 100 characters.

**Why these choices fit the documents:** the corpus mixes very short text (menu items, single Reddit comments) with longer educational paragraphs. A 500-character target keeps each chunk focused on one drink, one opinion, or one matcha concept, so retrieval returns tight, on-topic context rather than several unrelated drinks at once. The 100-character overlap protects information that spans a boundary — for example, a sentence naming a drink's ingredients followed by a sentence on whether it is beginner-friendly — so a single retrieved chunk still carries enough context to be useful.

**Preprocessing before chunking:** HTML tags are removed with a regular expression; HTML entities are unescaped; non-breaking spaces are normalized; lines matching known navigation/footer/cookie/advertisement patterns are dropped; and runs of whitespace are collapsed. The chunker then prefers to end a chunk at a paragraph break, then a sentence end, then a newline, then a space, falling back to a hard 500-character cut only when no natural boundary is nearby.

**Final chunk count:** 7 chunks across the 3 starter documents currently ingested in `data/raw/`. This count will grow once the remaining sources listed in the table above are saved into `data/raw/` and `ingest_and_chunk.py` is re-run.

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`, producing 384-dimensional embeddings, with cosine distance configured in ChromaDB. It was chosen because it is small, fast, runs locally with no API cost, and performs well on short, informal English text — which fits a corpus of menu snippets and Reddit comments.

**Production tradeoff reflection:** If this were deployed for real users and cost were not a constraint, I would weigh a larger or API-hosted embedding model with higher accuracy and a longer context window, and — because the corpus includes informal language and non-English tea terms — better support for multilingual and domain-specific text. The tradeoff is latency and cost: a stronger model improves retrieval relevance but is slower and more expensive per query, which matters for an interactive interface.

---

## Grounded Generation

**System prompt grounding instruction:** the model is given a system prompt that states it may answer *only* from the provided context chunks, must not use outside or general matcha knowledge, and must reply with the exact sentence "I don't have enough information on that." when the context is insufficient. The generation call uses `temperature=0` to keep answers deterministic and discourage creative additions.

**How source attribution is surfaced in the response:** sources are appended programmatically from the retrieval metadata, not invented by the LLM. After generation, the system collects the `source` filename of each retrieved chunk (de-duplicated, best-match first) and returns it alongside the answer; the Gradio UI shows these under "Retrieved from." When the model returns the refusal, no sources are attached, because the answer is not grounded in any chunk.

---

## Evaluation Report

> **Scope note:** The results below were generated by running the live system against the documents currently in `data/raw/` (the 3 starter documents, 7 chunks). They will be regenerated once the full source set in the Document Sources table is ingested. Distances are cosine distance (lower = more similar).

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Best matcha drink for a beginner avoiding bitterness | Matcha latte / sweeter milk-based; milk and sweetness smooth it | Matcha Latte and Cloud Matcha; milk softens the grassy edge, foam balances bitterness | Relevant (0.34) | **Accurate** |
| 2 | Customizations for a sweeter/creamier drink | Sweetness, creamy milk (oat), latte-style, cream/foam toppings | Add milk, choose a sweetness level, oat milk, salted cheese foam | Relevant (0.30) | **Accurate** |
| 3 | Difference between ceremonial and culinary matcha | Quality/use difference, **and labels are inconsistent marketing terms not to over-trust** | Plain (ceremonial) vs latte/baking use (culinary); smoother vs stronger | Relevant (0.18) | **Partially accurate** |
| 4 | Difference between a Cloud Matcha and a regular matcha latte | Cloud = latte + salted cheese foam (softens flavor); latte = matcha shaken with milk | Cloud has a salted cheese foam layer balancing bitterness; classic is matcha shaken with fresh milk | Relevant (0.30) | **Accurate** |
| 5 | What to order for a stronger matcha flavor | Matcha-forward drink, less sugar, fewer toppings/fruit, avoid milk overpowering | Ask for less sugar and skip fruit toppings, which bury the flavor | Relevant (0.36) | **Partially accurate** |

**Robustness check (off-topic input):** asked "What parking situation is best near UCSC?", the system returned "I don't have enough information on that." with no sources, confirming the grounding layer refuses out-of-domain questions instead of hallucinating.

**Summary:** three accurate and two partially accurate answers, with no hallucinations. The two partial results are honest limitations rather than failures of the mechanism: in both cases the answer was complete relative to the *available context* but missed detail that the expected answer drew from sources not yet ingested (Q5) or that the model dropped during synthesis (Q3, analyzed below).

---

## Failure Case Analysis

**Question that failed:** Q3 — "What is the difference between ceremonial and culinary matcha?"

**What the system returned:** A correct description of the practical difference (ceremonial is smoother and meant to be drunk plain; culinary is stronger and used for lattes and baking), but it omitted the most beginner-relevant point in the expected answer: that "ceremonial" and "culinary" are unregulated marketing labels that beginners should not over-trust.

**Root cause (tied to a specific pipeline stage):** This is a **generation-stage** failure, not a retrieval failure — and the distance scores prove it. The chunk containing the "marketing terms / not officially regulated" caveat was retrieved as the *single best match* at cosine distance 0.18. Retrieval did its job. With four chunks of context and an instruction to be "clear and beginner-friendly," the model summarized toward the most concrete, drink-relevant content and discarded the more abstract caveat during synthesis. The information was present in the context window but lost in the answer.

**Why that stage caused the failure:** Language models compress multi-chunk context toward the most salient, concrete points when asked to be concise. The caveat was the most conceptually important part of the answer but the least concrete, so it was the first thing dropped. Because retrieval succeeded, no amount of retrieval tuning would fix this — the fix has to happen at generation.

**What I would change to fix it:** Tighten the system prompt to require preserving caveats and qualifications — for example, "If the context warns about a common misconception or says a term is unreliable, include that warning in your answer." This is a single, testable change isolated to the generation stage. A secondary option is to reduce `top_k` so the model has fewer competing points to compress, though that risks dropping useful context elsewhere.

---

## Spec Reflection

**One way the spec helped me during implementation:** Writing the Chunking Strategy and Retrieval Approach sections of `planning.md` *before* coding gave me concrete parameters — 500-character chunks, 100-character overlap, `all-MiniLM-L6-v2`, and top-k = 4 — and, more importantly, the *reasoning* behind them. Because I had already articulated that my corpus mixes short reviews with longer articles, I could justify a chunker that prefers paragraph and sentence boundaries instead of a naive fixed split, and I never had to stop mid-implementation to re-decide basic parameters. The spec acted as a contract I could implement against directly.

**One way my implementation diverged from the spec, and why:** My requirements file originally pinned `sentence-transformers==3.4.1`, but adding the Gradio interface in the final milestone forced a change: Gradio 6.x requires `huggingface-hub >= 1.2`, which in turn requires `transformers >= 5.0`, which requires `sentence-transformers >= 5.0`. I therefore upgraded the embedding stack to 5.x. I verified this was safe by re-running retrieval and confirming the cosine distances were unchanged (0.34 / 0.30 / 0.18 on the first three questions), since the underlying `all-MiniLM-L6-v2` model weights are identical across versions. A second, smaller divergence: `planning.md` did not specify a distance metric, and ChromaDB defaults to squared-L2; I configured cosine distance instead so my relevance thresholds were interpretable.

---

## AI Usage

**Instance 1 — implementing the chunker**
- *What I gave the AI:* my Chunking Strategy section from `planning.md` (500-character chunks, 100-character overlap, "preserve paragraphs, menu items, and review comments when possible") and my list of document types.
- *What it produced:* a `chunk_text()` function using a sliding character window that snaps each chunk's end to the nearest paragraph break, then sentence end, then newline, then space, plus an inspection step printing representative and random chunks and warnings for empty, short, or HTML-containing chunks.
- *What I changed, verified, or overrode:* I inspected the representative and random chunks myself and checked the short-chunk warnings before accepting the 500/100 parameters, rather than assuming they were correct. *(Edit this line to match what you actually adjusted — e.g. whether you tuned the boundary look-back distance, the short-chunk threshold, or the sample text.)*

**Instance 2 — keeping the evaluation honest**
- *What I gave the AI:* I asked Claude to act as a reviewer for my evaluation and README, with instructions to point out weaknesses rather than just generate text.
- *What it produced:* it flagged that my system was still running on starter sample files rather than the full set of sources listed in my README, warned that reporting the evaluation as-is would misrepresent the project and make "Accurate" results circular, and identified that one of my evaluation questions was a methodology question my content corpus could not answer.
- *What I changed, verified, or overrode:* I decided to revise that evaluation question (Q4) into a content question my documents could answer, and I combined the critique with my own judgment about which fix preserved the intent of my evaluation plan rather than accepting a rewrite wholesale.

---

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your GROQ_API_KEY to a .env file (see .env.example)

# 3. Ingest and chunk the documents in data/raw/
python ingest_and_chunk.py

# 4. Build the embeddings and vector store, and test retrieval
python embed_and_retrieve.py

# 5. Test grounded generation from the command line
python query.py

# 6. Launch the Gradio interface
python app.py   # then open http://localhost:7860
```
