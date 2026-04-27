"""
embeddings.py
-------------
Creates sentence embeddings using the lightweight all-MiniLM-L6-v2 model.

Why all-MiniLM-L6-v2?
- Only 22MB model size
- Runs entirely on CPU — no GPU needed
- 384-dimensional embeddings (perfect balance of quality vs speed)
- Great semantic similarity for RAG pipelines
"""

from langchain_community.embeddings import HuggingFaceEmbeddings


# ── Singleton pattern: load the model only ONCE per session ─────────────────
_embedding_model = None


def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Load and return the sentence-transformer embedding model.
    Uses a module-level singleton so the model is only loaded once,
    saving ~2-3 seconds on repeated calls.

    Returns:
        HuggingFaceEmbeddings instance ready for use.
    """
    global _embedding_model

    if _embedding_model is None:
        # all-MiniLM-L6-v2 is a small, fast, CPU-friendly embedding model
        _embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},  # Force CPU — no GPU required
            encode_kwargs={
                "normalize_embeddings": True,  # Normalize for cosine similarity
                "batch_size": 32,              # Process 32 chunks at a time
            },
        )

    return _embedding_model
