# ModernRAG Test Suite

This directory contains unit tests for the ModernRAG project, focusing on testing the vector store functionality and main application logic.

## Test Structure

- **test_vector_store.py**: Tests for the vector store module
  - `TestVectorStoreConfig`: Tests for configuration management
  - `TestVectorStoreManager`: Tests for the vector store manager class
  - `TestAsyncAPI`: Tests for the async API functions

- **test_main.py**: Tests for the main application module
  - `TestMain`: Tests for the main function and error handling

## Fixtures

Shared fixtures are defined in `conftest.py`:

- `mock_env_vars`: Sets up environment variables for testing
- `sample_documents`: Creates sample documents for testing

## Running Tests

To run all tests:

```bash
python -m pytest
```

To run tests with verbose output:

```bash
python -m pytest -v
```

To run a specific test file:

```bash
python -m pytest tests/test_vector_store.py
```

To run a specific test:

```bash
python -m pytest tests/test_vector_store.py::TestVectorStoreConfig::test_config_from_env_vars
```

## Test Coverage

The tests cover the following functionality:

1. **Configuration Management**
   - Loading configuration from environment variables

2. **Vector Store Operations**
   - Initialization of the vector store manager
   - Creating and checking indexes
   - Vector store client management
   - Similarity search functionality

3. **Main Application**
   - End-to-end workflow
   - Error handling

## Mocking Strategy

The tests use mocking to avoid making actual API calls:

- Pinecone client operations are mocked
- OpenAI embeddings are mocked
- Async operations use AsyncMock for proper testing

This ensures tests can run quickly and without requiring external services.

## Adding New Tests

When adding new tests:

1. Follow the existing pattern for test classes and methods
2. Use appropriate fixtures from `conftest.py`
3. Mock external dependencies
4. Use descriptive test names that explain what is being tested
5. Add assertions that verify both the result and that the expected methods were called
