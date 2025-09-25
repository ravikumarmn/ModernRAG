# ModernRAG

A modern Retrieval-Augmented Generation (RAG) system built with async operations and production-level code.

[![Deploy to GitHub Pages](https://github.com/ravikumarmn/ModernRAG/actions/workflows/deploy-gh-pages.yml/badge.svg)](https://github.com/ravikumarmn/ModernRAG/actions/workflows/deploy-gh-pages.yml)

**Documentation:** [https://ravikumarmn.github.io/ModernRAG](https://ravikumarmn.github.io/ModernRAG)

## Features

- **Asynchronous Operations**: Fully async-compatible API for improved performance
- **Production-Ready**: Error handling, logging, configuration management, and type annotations
- **Vector Store Integration**: Seamless integration with Pinecone for vector storage and retrieval
- **Document Processing**: Tools for document loading, chunking, and embedding
- **Efficient Retrieval**: Advanced similarity search with configurable parameters
- **Interactive RAG Demo**: Web-based interface for exploring RAG capabilities
- **Query Caching**: Comprehensive caching system with memory and disk options
- **Document Augmentation**: Reranking and synthesis of retrieved documents

## Installation

```bash
# Clone the repository
git clone https://github.com/ravikumarmn/ModernRAG.git
cd ModernRAG

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## Environment Variables

Create a `.env` file with the following variables:

```
PINECONE_API_KEY=your_pinecone_api_key
OPENAI_API_KEY=your_openai_api_key
PINECONE_INDEX_NAME=your_index_name  # Optional, defaults to "langchain-test-index"
```

## Usage

### Basic Usage

```python
import asyncio
from modernrag.vector_store import similarity_search

async def search_example():
    results = await similarity_search(
        query="What is RAG?",
        k=3,
        score_threshold=0.7
    )
    
    for doc, score in results:
        print(f"Score: {score:.4f}")
        print(doc.page_content)

# Run the example
asyncio.run(search_example())
```

### Running Examples

```bash
# Run the main example
python -m modernrag.main
```

## Documentation

- [Vector Store Usage](./docs/vector_store_usage.md): Detailed documentation on the vector store module

## Testing

The project includes a comprehensive test suite for the vector store module and main application logic.

### Running Tests

```bash
# Run all tests
python -m pytest

# Run tests with verbose output
python -m pytest -v

# Run a specific test file
python -m pytest tests/test_vector_store.py

# Run a specific test
python -m pytest tests/test_vector_store.py::TestVectorStoreConfig::test_config_from_env_vars
```

### Test Coverage

The tests cover:

- Configuration management
- Vector store operations
- Main application workflow
- Error handling

See the [tests README](./tests/README.md) for more details on the test suite.

## Project Structure

```
ModernRAG/
├── data/                  # Sample data files
├── docs/                  # Documentation files
│   ├── miscellaneous.md   # Miscellaneous notes
│   └── vector_store_usage.md # Vector store documentation
├── modernrag/             # Main package
│   ├── __init__.py
│   ├── main.py            # Entry point
│   ├── vector_store.py    # Vector store operations
│   └── examples/          # Example scripts
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── conftest.py        # Shared test fixtures
│   ├── test_main.py       # Tests for main module
│   └── test_vector_store.py # Tests for vector store module
├── .env                   # Environment variables
├── .env.example           # Example environment variables
├── pytest.ini             # Pytest configuration
├── requirements.txt       # Dependencies
├── setup.py               # Package setup
└── README.md              # This file
```

## Dependencies

### Runtime Dependencies
- Python 3.8+
- langchain
- pinecone-client
- langchain-pinecone
- langchain-openai
- python-dotenv
- pydantic

### Testing Dependencies
- pytest
- pytest-asyncio
- unittest.mock

## License

MIT

## GitHub Pages and CI/CD

This project uses GitHub Pages to host documentation and a project website. The website is automatically deployed using GitHub Actions whenever changes are pushed to the main branch.

### Website Structure

The website is located in the `frontend` directory and includes:

- Landing page with project overview
- Comprehensive documentation
- Code examples
- Installation instructions

### CI/CD Pipeline

The CI/CD pipeline is configured in `.github/workflows/deploy-gh-pages.yml` and performs the following steps:

1. Checkout the repository
2. Set up Python environment
3. Install dependencies
4. Clean up unnecessary files
5. Copy frontend files to deployment directory
6. Deploy to GitHub Pages

### Setting Up GitHub Pages

To set up GitHub Pages for this repository:

1. Go to your GitHub repository settings
2. Navigate to the "Pages" section in the left sidebar
3. Under "Source", select "GitHub Actions" from the dropdown menu
4. The site will be deployed automatically when you push to the main branch

### Local Development

To work on the website locally:

```bash
# Navigate to the frontend directory
cd frontend

# Start a local server
python -m http.server 8000
```

Then open your browser to `http://localhost:8000`

## Interactive RAG Demo

The project includes an interactive web-based RAG demo that allows users to experience the RAG system in action without setting up the backend infrastructure.

### Demo Features

- **Interactive Query Interface**: Ask questions and get AI-generated responses
- **Document Visualization**: See which documents were retrieved for each query
- **Performance Metrics**: View retrieval time, generation time, and total processing time
- **Sample Queries**: Try pre-defined sample queries to explore different aspects of the system

### Try the Demo

Visit the [ModernRAG Demo](https://ravikumarmn.github.io/ModernRAG/rag.html) to try it out!

## Netlify Deployment

In addition to GitHub Pages for static content, this project uses Netlify Functions to provide serverless backend functionality for the RAG demo.

### Deploying to Netlify

1. **Fork the repository** to your GitHub account

2. **Sign up for Netlify** and connect your GitHub account

3. **Create a new site** from your forked repository

4. **Configure environment variables** in the Netlify dashboard:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `PINECONE_API_KEY`: Your Pinecone API key
   - `PINECONE_INDEX_NAME`: Your Pinecone index name

5. **Deploy** your site

### Local Development with Netlify Functions

To develop and test Netlify Functions locally:

```bash
# Install Netlify CLI
npm install netlify-cli -g

# Start local development server
netlify dev
```

This will start a local server that simulates the Netlify environment, including Functions.
