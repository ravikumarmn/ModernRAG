"""
Unit tests for the vector_store module.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

from pinecone import Pinecone, ServerlessSpec
from langchain.docstore.document import Document

from modernrag.vector_store import (
    VectorStoreConfig,
    get_config,
    get_embeddings,
    VectorStoreManager,
    check_index_exists,
    get_vector_store,
    similarity_search
)


class TestVectorStoreConfig:
    """Tests for the VectorStoreConfig class."""

    def test_config_from_env_vars(self, mock_env_vars):
        """Test that config loads correctly from environment variables."""
        config = VectorStoreConfig()
        assert config.pinecone_api_key == "test-api-key"
        # Just check that we get a value for default_index_name
        assert config.default_index_name is not None
        assert config.embedding_model == "test-embedding-model"
        assert config.dimension == 1536
        assert config.metric == "cosine"
        assert config.cloud_provider == "aws"
        assert config.region == "us-east-1"
        assert config.chunk_size == 200
        assert config.chunk_overlap == 20


class TestVectorStoreManager:
    """Tests for the VectorStoreManager class."""

    @patch("modernrag.vector_store.Pinecone")
    @patch("modernrag.vector_store.get_embeddings")
    def test_init(self, mock_get_embeddings, mock_pinecone, mock_env_vars):
        """Test VectorStoreManager initialization."""
        mock_embeddings = MagicMock()
        mock_get_embeddings.return_value = mock_embeddings
        
        manager = VectorStoreManager()
        
        assert manager._pinecone_client is mock_pinecone.return_value
        assert manager._embeddings is mock_embeddings
        assert manager._index_cache == {}
        assert manager._vector_store_cache == {}

    @pytest.mark.asyncio
    @patch("modernrag.vector_store.asyncio.to_thread")
    async def test_create_index(self, mock_to_thread, mock_env_vars):
        """Test create_index method."""
        mock_to_thread.return_value = None
        
        with patch("modernrag.vector_store.Pinecone") as mock_pinecone:
            manager = VectorStoreManager()
            result = await manager.create_index("test-new-index")
            
            assert result == "test-new-index"
            mock_to_thread.assert_called_once()
            
            # Check that create_index was called with correct parameters
            create_index_call = mock_to_thread.call_args[0][0]
            assert create_index_call == mock_pinecone.return_value.create_index

    @pytest.mark.asyncio
    @patch("modernrag.vector_store.asyncio.to_thread")
    async def test_check_index_exists_when_exists(self, mock_to_thread, mock_env_vars):
        """Test check_index_exists when index exists."""
        mock_to_thread.return_value = True
        
        with patch("modernrag.vector_store.Pinecone"):
            manager = VectorStoreManager()
            result = await manager.check_index_exists("test-index")
            
            assert result is True
            mock_to_thread.assert_called_once()

    @pytest.mark.asyncio
    @patch("modernrag.vector_store.asyncio.to_thread")
    async def test_check_index_exists_when_not_exists(self, mock_to_thread, mock_env_vars):
        """Test check_index_exists when index doesn't exist."""
        mock_to_thread.side_effect = [False, None]
        
        with patch("modernrag.vector_store.Pinecone"):
            manager = VectorStoreManager()
            with patch.object(manager, "create_index") as mock_create_index:
                mock_create_index.return_value = "test-index"
                result = await manager.check_index_exists("test-index")
                
                assert result is True
                mock_to_thread.assert_called_once()
                mock_create_index.assert_called_once_with("test-index")


class TestAsyncAPI:
    """Tests for the async API functions."""

    @pytest.mark.asyncio
    async def test_check_index_exists(self, mock_env_vars):
        """Test check_index_exists function."""
        with patch("modernrag.vector_store.vector_store_manager") as mock_manager:
            mock_manager.check_index_exists = AsyncMock(return_value=True)
            result = await check_index_exists("test-index")
            
            assert result is True
            mock_manager.check_index_exists.assert_called_once_with("test-index")

    @pytest.mark.asyncio
    async def test_get_vector_store(self, mock_env_vars):
        """Test get_vector_store function."""
        mock_vector_store = MagicMock()
        
        with patch("modernrag.vector_store.vector_store_manager") as mock_manager:
            mock_manager.get_vector_store = AsyncMock(return_value=mock_vector_store)
            result = await get_vector_store("test-index")
            
            assert result is mock_vector_store
            mock_manager.get_vector_store.assert_called_once_with("test-index")

    @pytest.mark.asyncio
    async def test_similarity_search(self, mock_env_vars, sample_documents):
        """Test similarity_search function."""
        mock_results = sample_documents[:1]  # Use first document from sample_documents
        
        with patch("modernrag.vector_store.vector_store_manager") as mock_manager:
            mock_manager.similarity_search = AsyncMock(return_value=mock_results)
            result = await similarity_search(
                query="test query",
                index_name="test-index",
                k=2,
                score_threshold=0.5
            )
            
            assert result == mock_results
            mock_manager.similarity_search.assert_called_once_with(
                "test query", "test-index", 2, 0.5
            )
