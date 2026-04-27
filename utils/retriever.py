"""
retriever.py
------------
Handles semantic search over the ChromaDB vector store.

Retrieval strategy:
- MMR (Maximal Marginal Relevance): Balances relevance AND diversity.
  Prevents retrieving 3 nearly-identical chunks when documents repeat text.
- top_k=3: Fetch top 3 relevant chunks (keeps context tight & tokens low)
"""

from langchain_community.vectorstores import Chroma

# Number of chunks to retrieve per query
TOP_K = 3


def retrieve_relevant_chunks(
    vector_store: Chroma,
    query: str,
    top_k: int = TOP_K,
) -> list:
    """
    Retrieve the most semantically relevant document chunks for a query.

    Uses MMR (Maximal Marginal Relevance) to balance:
      - Relevance: How similar the chunk is to the query
      - Diversity: Avoid returning near-duplicate chunks

    Args:
        vector_store: The Chroma vector store to search.
        query: User's question string.
        top_k: Number of chunks to return (default 3).

    Returns:
        List of LangChain Document objects (most relevant chunks).

    Raises:
        ValueError: If the vector store is empty or query fails.
    """
    if vector_store is None:
        raise ValueError(
            "Vector store is not initialized. Please upload a PDF first."
        )

    try:
        # MMR retrieval — diversity-aware similarity search
        retrieved_docs = vector_store.max_marginal_relevance_search(
            query=query,
            k=top_k,
            fetch_k=top_k * 3,  # Fetch 3x then re-rank for diversity
            lambda_mult=0.7,    # 0.7 = 70% relevance, 30% diversity
        )
        return retrieved_docs

    except Exception as e:
        raise ValueError(f"Retrieval failed: {str(e)}")


def format_context(retrieved_docs: list, max_chars: int = 3000) -> str:
    """
    Format retrieved document chunks into a single context string.
    Truncates to max_chars to prevent exceeding Groq's token limit.

    Args:
        retrieved_docs: List of Document objects from retriever.
        max_chars: Maximum total characters for context (default 3000).

    Returns:
        Formatted context string with source info per chunk.
    """
    context_parts = []
    total_chars = 0

    for i, doc in enumerate(retrieved_docs):
        # Pull metadata for source attribution
        filename = doc.metadata.get("source_filename", "Unknown File")
        page = doc.metadata.get("page", "?")
        chunk_text = doc.page_content.strip()

        # Build a clearly labeled context block
        block = (
            f"[Source {i+1}: {filename}, Page {page}]\n"
            f"{chunk_text}"
        )

        # Stay within token-safe character limit
        if total_chars + len(block) > max_chars:
            remaining = max_chars - total_chars
            if remaining > 100:  # Only add if there's meaningful space left
                context_parts.append(block[:remaining] + "...")
            break

        context_parts.append(block)
        total_chars += len(block)

    return "\n\n---\n\n".join(context_parts)
