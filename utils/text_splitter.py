"""
text_splitter.py
----------------
Splits large document text into smaller, overlapping chunks.
Smaller chunks = more precise retrieval = better answers.

Settings:
- chunk_size=500   : Each chunk has max 500 characters
- chunk_overlap=50 : 50 chars overlap prevents context loss at boundaries
"""

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_documents(documents: list) -> list:
    """
    Split LangChain Documents into smaller overlapping text chunks.

    Args:
        documents: List of LangChain Document objects (from pdf_loader).

    Returns:
        List of smaller Document chunks ready for embedding.

    Raises:
        ValueError: If no chunks were produced.
    """
    # RecursiveCharacterTextSplitter tries to split on paragraphs → sentences
    # → words → characters, preserving semantic meaning as much as possible.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,       # Max characters per chunk (CPU-friendly)
        chunk_overlap=50,     # Overlap to prevent losing context at boundaries
        length_function=len,  # Use character count (not token count) for speed
        separators=["\n\n", "\n", " ", ""],  # Split order: paragraphs first
    )

    chunks = splitter.split_documents(documents)

    if not chunks:
        raise ValueError(
            "No text chunks were generated. "
            "The PDF may be empty or contain only images."
        )

    # Add a chunk index to metadata for reference in the UI
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i

    return chunks


def get_chunk_stats(chunks: list) -> dict:
    """
    Return basic statistics about the generated chunks.

    Args:
        chunks: List of Document chunks.

    Returns:
        Dictionary with count, average size, min/max sizes.
    """
    sizes = [len(c.page_content) for c in chunks]
    return {
        "total_chunks": len(chunks),
        "avg_chunk_size": int(sum(sizes) / len(sizes)) if sizes else 0,
        "min_chunk_size": min(sizes) if sizes else 0,
        "max_chunk_size": max(sizes) if sizes else 0,
    }
