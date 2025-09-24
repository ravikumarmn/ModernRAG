"""
Tests for the generation module of the ModernRAG application.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from langchain.docstore.document import Document

from modernrag.generation import (
    GenerationConfig,
    AugmentationManager,
    GenerationManager,
    rerank_documents,
    augment_documents,
    generate_response,
    retrieve_augment_generate
)


@pytest.fixture
def sample_documents():
    """Sample documents for testing."""
    return [
        (Document(
            page_content="This is a test document about RAG systems.",
            metadata={"source": "Test Source", "page": 1}
        ), 0.85),
        (Document(
            page_content="This document discusses retrieval-augmented generation.",
            metadata={"source": "Test Source", "page": 2}
        ), 0.75),
        (Document(
            page_content="This is an unrelated document about machine learning.",
            metadata={"source": "Test Source", "page": 3}
        ), 0.65),
    ]


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing."""
    mock_response = MagicMock()
    mock_response.content = "This is a mock response from the LLM."
    return mock_response


@pytest.mark.asyncio
async def test_rerank_documents(sample_documents, mock_llm_response):
    """Test the rerank_documents function."""
    with patch('modernrag.generation.get_llm') as mock_get_llm:
        # Setup the mock
        mock_llm = AsyncMock()
        mock_llm.invoke = AsyncMock(return_value=mock_llm_response)
        mock_get_llm.return_value = mock_llm
        
        # Set the mock response content to a comma-separated list of document indices
        mock_llm_response.content = "2,1,3"
        
        # Create an instance of AugmentationManager with the mocked LLM
        augmentation_manager = AugmentationManager()
        augmentation_manager.llm = mock_llm
        
        # Call the function
        result = await augmentation_manager.rerank_documents(
            query="test query",
            documents=sample_documents,
            top_k=2
        )
        
        # Assertions
        assert len(result) == 2
        # The first document should be the second one from the original list (index 1)
        assert "retrieval-augmented generation" in result[0].page_content


@pytest.mark.asyncio
async def test_augment_documents(sample_documents, mock_llm_response):
    """Test the augment_documents function."""
    with patch('modernrag.generation.get_llm') as mock_get_llm:
        # Setup the mock
        mock_llm = AsyncMock()
        mock_llm.invoke = AsyncMock(return_value=mock_llm_response)
        mock_get_llm.return_value = mock_llm
        
        # Set the mock response content
        mock_llm_response.content = "Synthesized information about RAG systems."
        
        # Create an instance of AugmentationManager with the mocked LLM
        augmentation_manager = AugmentationManager()
        augmentation_manager.llm = mock_llm
        
        # Extract just the documents from the tuples for this test
        docs = [doc for doc, _ in sample_documents]
        
        # Call the function
        result = await augmentation_manager.augment_documents(
            query="test query",
            documents=docs
        )
        
        # Assertions
        assert result == "Synthesized information about RAG systems."
        assert mock_llm.invoke.called


@pytest.mark.asyncio
async def test_generate_response(mock_llm_response):
    """Test the generate_response function."""
    with patch('modernrag.generation.get_llm') as mock_get_llm:
        # Setup the mock
        mock_llm = AsyncMock()
        mock_llm.invoke = AsyncMock(return_value=mock_llm_response)
        mock_get_llm.return_value = mock_llm
        
        # Set the mock response content
        mock_llm_response.content = "Generated response based on the context."
        
        # Create an instance of GenerationManager with the mocked LLM
        generation_manager = GenerationManager()
        generation_manager.llm = mock_llm
        
        # Call the function
        result = await generation_manager.generate_response(
            query="test query",
            context="test context"
        )
        
        # Assertions
        assert result == "Generated response based on the context."
        assert mock_llm.invoke.called


@pytest.mark.asyncio
async def test_retrieve_augment_generate(sample_documents, mock_llm_response):
    """Test the complete RAG pipeline."""
    with patch('modernrag.generation.similarity_search', new_callable=AsyncMock) as mock_search, \
         patch('modernrag.generation.GenerationManager.augmentation_manager') as mock_augmentation_manager, \
         patch('modernrag.generation.GenerationManager.generate_response', new_callable=AsyncMock) as mock_generate:
        
        # Setup the mocks
        mock_search.return_value = sample_documents
        
        # Mock the augmentation manager's rerank_documents method
        mock_augmentation_manager.rerank_documents = AsyncMock()
        mock_augmentation_manager.rerank_documents.return_value = [doc for doc, _ in sample_documents[:2]]
        
        # Mock the augmentation manager's augment_documents method
        mock_augmentation_manager.augment_documents = AsyncMock()
        mock_augmentation_manager.augment_documents.return_value = "Augmented context."
        
        # Mock the generate_response method
        mock_generate.return_value = "Final generated response."
        
        # Create an instance of GenerationManager
        generation_manager = GenerationManager()
        
        # Replace the augmentation_manager with our mock
        generation_manager.augmentation_manager = mock_augmentation_manager
        
        # Call the function
        result = await generation_manager.retrieve_augment_generate(
            query="test query",
            index_name="test-index",
            k=3,
            score_threshold=0.5,
            rerank_top_k=2
        )
        
        # Assertions
        assert result["query"] == "test query"
        assert len(result["retrieved_docs"]) == 3
        assert result["augmented_context"] == "Augmented context."
        assert result["response"] == "Final generated response."
        
        # Verify the mocks were called
        mock_search.assert_called_once()
        mock_augmentation_manager.rerank_documents.assert_called_once()
        mock_augmentation_manager.augment_documents.assert_called_once()
        mock_generate.assert_called_once()
