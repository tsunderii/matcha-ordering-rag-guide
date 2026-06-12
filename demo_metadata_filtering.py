"""
Stretch feature demo: Metadata Filtering

Shows the same query run three ways against the ChromaDB collection:
  1. No filter (normal semantic search across all sources)
  2. Filtered to a single source document (where={"source": ...})
  3. Filtered by a numeric metadata field (where={"char_length": {"$gte": 400}})

The point is the *visible effect*: the filter changes which chunks come back,
because ChromaDB restricts the search to chunks whose metadata matches before
ranking them semantically.

Run it with:
    python demo_metadata_filtering.py
(Run `python embed_and_retrieve.py` first so the vector store exists.)
"""

import contextlib
import io

import chromadb
from sentence_transformers import SentenceTransformer

from embed_and_retrieve import (
    retrieve,
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
)


def show(title, results):
    """Print a compact summary of one retrieval result set."""
    print(f"\n{title}")
    if not results:
        print("  (no results)")
        return
    for r in results:
        print(f"  - {r['source']} (chunk {r['chunk_index']}, "
              f"{r['char_length']} chars, dist {r['distance']:.3f})")


def main():
    # Connect to the persistent collection and load the embedding model.
    collection = chromadb.PersistentClient(path=CHROMA_DIR).get_collection(COLLECTION_NAME)
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    query = "What makes a matcha drink taste less bitter?"
    print("=" * 70)
    print(f"QUERY: {query}")
    print("=" * 70)

    # retrieve() prints its own verbose output; silence it here and use the
    # returned data so this demo stays compact.
    def quiet_retrieve(**kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            return retrieve(query, collection, model, **kwargs)

    # 1. No filter — search everything.
    show("1) NO FILTER (all sources):", quiet_retrieve(top_k=4))

    # 2. Filter to a single source document.
    only_source = "01_mollytea_menu.txt"
    show(f"2) FILTER where source == '{only_source}':",
         quiet_retrieve(top_k=4, where={"source": only_source}))

    # 3. Filter by a numeric metadata field (only longer chunks).
    show("3) FILTER where char_length >= 400:",
         quiet_retrieve(top_k=4, where={"char_length": {"$gte": 400}}))

    print("\nNote how the filtered runs return a different set of chunks than the "
          "unfiltered run — the metadata filter changes the candidate pool before "
          "semantic ranking.")


if __name__ == "__main__":
    main()
