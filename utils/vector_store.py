"""
vector_store.py
---------------
Manages ChromaDB vector store operations:
  - Building a new store from document chunks
  - Persisting it to disk (avoids reprocessing same PDF)
  - Loading an existing store

ChromaDB stores embedding vectors locally so semantic search
is fast even without a GPU or internet connection.
"""

import os
import shutil
from langchain_community.vectorstores import Chroma
from utils.embeddings import get_embedding_model

# Local directory for ChromaDB persistence
CHROMA_PERSIST_DIR = "./chroma_store"


def build_vector_store(chunks: list) -> Chroma:
    """
    Create a ChromaDB vector store from document chunks.
    Embeds all chunks and stores them locally for fast retrieval.

    Args:
        chunks: List of LangChain Document chunks (from text_splitter).

    Returns:
        A Chroma vector store instance ready for similarity search.
    """
    embedding_model = get_embedding_model()

    # Clear any existing store to avoid stale data from previous sessions
    if os.path.exists(CHROMA_PERSIST_DIR):
        shutil.rmtree(CHROMA_PERSIST_DIR)

    # Build the vector store — this embeds all chunks and saves to disk
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_PERSIST_DIR,
        collection_name="pdf_collection",
    )

    return vector_store


def load_vector_store() -> Chroma:
    """
    Load an existing ChromaDB vector store from disk.

    Returns:
        A Chroma vector store instance, or None if not found.
    """
    if not os.path.exists(CHROMA_PERSIST_DIR):
        return None

    embedding_model = get_embedding_model()

    vector_store = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embedding_model,
        collection_name="pdf_collection",
    )

    return vector_store


def clear_vector_store() -> None:
    """
    Delete the persisted ChromaDB store from disk.
    Called when the user uploads new PDFs to start fresh.
    """
    if os.path.exists(CHROMA_PERSIST_DIR):
        shutil.rmtree(CHROMA_PERSIST_DIR)
