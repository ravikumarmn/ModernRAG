"""
Unit tests for the main module.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock

from modernrag.main import main


@pytest.fixture
def mock_search_results(sample_documents):
    """Create mock search results for testing."""
    return sample_documents[:2]  # Use first two documents from sample_documents fixture


class TestMain:
    """Tests for the main module."""

    @pytest.mark.asyncio
    @patch("modernrag.main.similarity_search")
    @patch("modernrag.main.check_index_exists")
    async def test_main_function(self, mock_check_index, mock_similarity_search, 
                                mock_env_vars, mock_search_results):
        """Test the main function."""
        # Set up mocks
        mock_check_index.return_value = True
        mock_similarity_search.return_value = mock_search_results
        
        # Call the main function
        with patch("builtins.print") as mock_print:
            with patch("modernrag.main.logger") as mock_logger:
                await main()
                
                # Verify that check_index_exists was called
                mock_check_index.assert_called_once_with("langchain-test-index")
                
                # Verify that similarity_search was called with correct parameters
                mock_similarity_search.assert_called_once()
                call_args = mock_similarity_search.call_args[1]
                assert call_args["query"] == "LM-generated results as supervisory signals to fine-tune the embedding model during the RAG process."
                assert call_args["index_name"] == "langchain-test-index"
                assert call_args["k"] == 2
                assert call_args["score_threshold"] == 0.4
                
                # Verify that results were printed
                assert mock_print.call_count >= 6  # At least 6 print calls for 2 results
                
                # Check log messages
                mock_logger.info.assert_any_call("Searching for: LM-generated results as supervisory signals to fine-tune the embedding model during the RAG process.")
                mock_logger.info.assert_any_call("Found 2 results")

    @pytest.mark.asyncio
    @patch("modernrag.main.similarity_search")
    @patch("modernrag.main.check_index_exists")
    async def test_main_function_error_handling(self, mock_check_index, 
                                              mock_similarity_search, 
                                              mock_env_vars):
        """Test error handling in the main function."""
        # Set up mock to raise an exception
        mock_check_index.side_effect = Exception("Test error")
        
        # Call the main function and expect it to raise the exception
        with patch("modernrag.main.logger") as mock_logger:
            with pytest.raises(Exception, match="Test error"):
                await main()
                
            # Verify that the error was logged
            mock_logger.error.assert_called_once_with("Error in main function: Test error")
