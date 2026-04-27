"""
pdf_loader.py
-------------
Handles loading and extracting text from uploaded PDF files.
Uses LangChain's PyPDFLoader for reliable multi-page extraction.
"""

import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader


def load_pdfs(uploaded_files: list) -> list:
    """
    Load and extract text from one or multiple uploaded PDF files.

    Args:
        uploaded_files: List of Streamlit UploadedFile objects.

    Returns:
        List of LangChain Document objects with page content and metadata.

    Raises:
        ValueError: If no valid documents could be extracted.
    """
    all_documents = []

    for uploaded_file in uploaded_files:
        # Save uploaded file to a temporary location so PyPDFLoader can read it
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".pdf"
        ) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        try:
            # Load the PDF using LangChain's PyPDFLoader
            loader = PyPDFLoader(tmp_path)
            documents = loader.load()

            # Attach the original filename to each document's metadata
            for doc in documents:
                doc.metadata["source_filename"] = uploaded_file.name

            all_documents.extend(documents)

        except Exception as e:
            raise ValueError(
                f"Failed to load PDF '{uploaded_file.name}': {str(e)}"
            )

        finally:
            # Always clean up the temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    if not all_documents:
        raise ValueError(
            "No text could be extracted from the uploaded PDF(s). "
            "Please check that the files are not scanned images."
        )

    return all_documents


def get_pdf_metadata(documents: list) -> dict:
    """
    Extract useful metadata from loaded documents.

    Args:
        documents: List of LangChain Document objects.

    Returns:
        Dictionary with file names, total pages, total characters.
    """
    filenames = list(
        set(doc.metadata.get("source_filename", "Unknown") for doc in documents)
    )
    total_pages = len(documents)
    total_chars = sum(len(doc.page_content) for doc in documents)

    return {
        "filenames": filenames,
        "total_pages": total_pages,
        "total_characters": total_chars,
    }
