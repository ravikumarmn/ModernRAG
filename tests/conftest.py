"""
Shared fixtures for ModernRAG tests.
"""

import os
import pytest
from langchain.docstore.document import Document


@pytest.fixture
def mock_env_vars():
    """Set up environment variables for testing."""
    os.environ["PINECONE_API_KEY"] = "test-api-key"
    os.environ["OPENAI_API_KEY"] = "test-openai-key"
    os.environ["PINECONE_INDEX_NAME"] = "test-index"
    os.environ["EMBEDDING_MODEL"] = "test-embedding-model"
    os.environ["VECTOR_DIMENSION"] = "1536"
    os.environ["SIMILARITY_METRIC"] = "cosine"
    os.environ["CLOUD_PROVIDER"] = "aws"
    os.environ["CLOUD_REGION"] = "us-east-1"
    os.environ["CHUNK_SIZE"] = "200"
    os.environ["CHUNK_OVERLAP"] = "20"
    yield
    # Clean up environment variables after tests
    for var in [
        "PINECONE_API_KEY", "OPENAI_API_KEY", "PINECONE_INDEX_NAME", 
        "EMBEDDING_MODEL", "VECTOR_DIMENSION", "SIMILARITY_METRIC", 
        "CLOUD_PROVIDER", "CLOUD_REGION", "CHUNK_SIZE", "CHUNK_OVERLAP"
    ]:
        if var in os.environ:
            del os.environ[var]


@pytest.fixture
def sample_documents():
    """Create sample documents for testing."""
    return [
        Document(
            page_content="This is a test document about vector databases.",
            metadata={"source": "test-source-1", "page": 1}
        ),
        Document(
            page_content="Embeddings are numerical representations of text.",
            metadata={"source": "test-source-2", "page": 2}
        ),
        Document(
            page_content="RAG combines retrieval with generation for better results.",
            metadata={"source": "test-source-3", "page": 3}
        )
    ]
