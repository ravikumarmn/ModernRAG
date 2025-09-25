// RAG Demo JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const queryInput = document.getElementById('query-input');
    const submitButton = document.getElementById('submit-query');
    const loadingSpinner = document.getElementById('loading-spinner');
    const errorMessage = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    const resultContainer = document.getElementById('result-container');
    const documentsContainer = document.getElementById('documents-container');
    const responseContent = document.getElementById('response-content');
    const retrievalTimeEl = document.getElementById('retrieval-time');
    const generationTimeEl = document.getElementById('generation-time');
    const totalTimeEl = document.getElementById('total-time');
    const sampleQueryButtons = document.querySelectorAll('.sample-query-btn');
    
    // Sample data for demo purposes
    const sampleData = {
        "What is Retrieval-Augmented Generation?": {
            documents: [
                {
                    content: "Retrieval-Augmented Generation (RAG) is a technique that enhances large language models by retrieving relevant information from external knowledge sources before generating responses. This approach combines the strengths of retrieval-based and generation-based methods.",
                    source: "RAG Paper",
                    score: 0.92
                },
                {
                    content: "RAG systems typically involve a retrieval component that searches for relevant documents or passages from a knowledge base, and a generation component that uses the retrieved information to produce more accurate and informed responses.",
                    source: "ModernRAG Documentation",
                    score: 0.87
                },
                {
                    content: "Unlike traditional language models that rely solely on their parametric knowledge, RAG models can access up-to-date information and specialized knowledge, making them more accurate and less prone to hallucination.",
                    source: "AI Research Blog",
                    score: 0.81
                }
            ],
            response: "Retrieval-Augmented Generation (RAG) is an AI technique that enhances language models by incorporating external knowledge retrieval into the generation process. Instead of relying solely on the knowledge encoded in the model's parameters, RAG systems first retrieve relevant information from a knowledge base and then use this information to generate more accurate, factual, and contextually appropriate responses.\n\nThe key components of RAG include:\n\n1. **Retrieval Component**: Searches through a database or vector store to find documents, passages, or information relevant to the user's query.\n\n2. **Augmentation Component**: Processes and refines the retrieved information to make it more useful for the generation step.\n\n3. **Generation Component**: Uses the retrieved and augmented information along with the original query to produce a comprehensive response.\n\nRAG offers several advantages over traditional language models:\n- Reduced hallucinations and factual errors\n- Access to up-to-date information beyond the model's training data\n- Ability to cite sources for generated information\n- More transparent reasoning process\n\nModernRAG implements this approach with asynchronous operations, efficient vector storage, and production-level code practices to create a robust and scalable RAG system.",
            metrics: {
                retrievalTime: 0.32,
                generationTime: 1.45,
                totalTime: 1.77
            }
        },
        "How does the vector store work in ModernRAG?": {
            documents: [
                {
                    content: "The vector store in ModernRAG is built on top of Pinecone, providing asynchronous operations for efficient vector storage and retrieval. It uses a singleton pattern to manage connections and implements LRU caching for improved performance.",
                    source: "vector_store.py",
                    score: 0.95
                },
                {
                    content: "VectorStoreManager handles index creation, document embedding, and similarity search operations. All operations are wrapped in asyncio.to_thread to provide non-blocking asynchronous interfaces while maintaining compatibility with synchronous libraries.",
                    source: "ModernRAG Documentation",
                    score: 0.89
                },
                {
                    content: "Documents are split into chunks using RecursiveCharacterTextSplitter before being embedded and stored in the vector database. The system supports batch processing for efficient handling of large document collections.",
                    source: "vector_store.py",
                    score: 0.84
                }
            ],
            response: "The vector store in ModernRAG is a sophisticated component that handles the storage and retrieval of document embeddings. Here's how it works:\n\n1. **Architecture**: The vector store is implemented using a `VectorStoreManager` class that follows the singleton pattern, ensuring efficient resource usage by maintaining a single instance throughout the application lifecycle.\n\n2. **Asynchronous API**: All vector store operations are fully asynchronous, using `asyncio.to_thread` to wrap synchronous Pinecone operations, allowing non-blocking I/O while maintaining compatibility with synchronous libraries.\n\n3. **Document Processing**: When documents are added to the system, they are:\n   - Split into smaller chunks using `RecursiveCharacterTextSplitter`\n   - Converted to vector embeddings using OpenAI's embedding models\n   - Stored in Pinecone with unique IDs and metadata\n\n4. **Batch Processing**: The system supports processing documents in configurable batches, with progress tracking and error handling for robust operation at scale.\n\n5. **Caching**: The implementation includes LRU caching for configurations, embeddings, and vector store instances to minimize redundant operations and improve performance.\n\n6. **Similarity Search**: When a query is received, it's converted to an embedding and used to find similar documents in the vector store based on cosine similarity, with configurable parameters like `k` (number of results) and `score_threshold`.\n\n7. **Error Handling**: Comprehensive try/except blocks with proper logging ensure robust operation even when external services experience issues.\n\nThis implementation follows best practices for production Python applications, with full type annotations, comprehensive documentation, and a clean public API that delegates to the manager instance.",
            metrics: {
                retrievalTime: 0.28,
                generationTime: 1.62,
                totalTime: 1.90
            }
        },
        "Explain the caching system in ModernRAG": {
            documents: [
                {
                    content: "ModernRAG implements a comprehensive caching system with both memory and disk caching options. The caching module provides functions for storing and retrieving query results, with configurable TTL (Time-To-Live) settings.",
                    source: "caching.py",
                    score: 0.93
                },
                {
                    content: "The memory cache uses an LRU (Least Recently Used) strategy to manage cache size, automatically evicting older entries when the cache reaches its configured maximum size. This prevents memory usage from growing unbounded.",
                    source: "ModernRAG Documentation",
                    score: 0.88
                },
                {
                    content: "For persistence across application restarts, the disk cache stores serialized results in a configurable directory. Cache invalidation happens automatically based on TTL or can be triggered manually through the clear_cache and clear_expired_cache functions.",
                    source: "caching.py",
                    score: 0.85
                }
            ],
            response: "The caching system in ModernRAG is a sophisticated component designed to improve performance and reduce redundant operations. Here's a detailed explanation:\n\n### Core Components\n\n1. **Dual-Layer Caching**: The system implements both memory caching (for speed) and disk caching (for persistence):\n   - Memory cache: Fast in-memory storage using LRU (Least Recently Used) eviction policy\n   - Disk cache: Persistent storage that survives application restarts\n\n2. **Cache Configuration**: The caching behavior is highly configurable through the `CacheConfig` class, which includes settings for:\n   - TTL (Time-To-Live): How long cached items remain valid\n   - Maximum cache size: Limits memory usage\n   - Cache directory: Where disk cache files are stored\n   - Enabled/disabled flags for each cache type\n\n3. **Asynchronous Operations**: All caching operations are implemented with async/await support for non-blocking performance\n\n### Key Functions\n\n- `get_cached_result()`: Attempts to retrieve a cached response for a given query\n- `cache_result()`: Stores a query result in both memory and disk caches\n- `clear_cache()`: Manually empties all caches\n- `clear_expired_cache()`: Removes only expired entries\n\n### Integration with RAG Pipeline\n\nThe caching system is integrated with the RAG pipeline in the `retrieve_augment_generate()` function, which:\n1. First checks if a cached result exists for the query\n2. If found and valid, returns the cached result immediately\n3. If not found, executes the full RAG pipeline\n4. Stores the new result in cache for future use\n\nThis approach significantly improves performance for repeated queries while maintaining result freshness through configurable expiration policies.",
            metrics: {
                retrievalTime: 0.25,
                generationTime: 1.38,
                totalTime: 1.63
            }
        }
    };
    
    // Function to process query
    async function processQuery(query) {
        // Show loading spinner, hide error and results
        loadingSpinner.style.display = 'block';
        errorMessage.style.display = 'none';
        resultContainer.style.display = 'none';
        
        try {
            // Call the serverless API
            let result;
            
            // First try to use the serverless API
            try {
                const response = await fetch('/api/rag-query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query })
                });
                
                if (!response.ok) {
                    throw new Error(`API responded with status: ${response.status}`);
                }
                
                result = await response.json();
                
            } catch (apiError) {
                console.warn('API call failed, falling back to sample data:', apiError);
                
                // Fallback to sample data if API call fails
                if (sampleData[query]) {
                    result = sampleData[query];
                } else {
                    // For queries we don't have sample data for, use a mock response
                    result = {
                        documents: [
                            {
                                content: "This is a simulated document result for the query: " + query,
                                source: "Simulated Source",
                                score: 0.75
                            }
                        ],
                        response: "This is a simulated response for the query: " + query + "\n\nIn a real implementation, this would be generated by calling your backend API that implements the ModernRAG system. The API would retrieve relevant documents, augment them, and generate a response based on the query.",
                        metrics: {
                            retrievalTime: (Math.random() * 0.5 + 0.2).toFixed(2),
                            generationTime: (Math.random() * 1.5 + 1.0).toFixed(2),
                            totalTime: 0 // Will be calculated
                        }
                    };
                    
                    // Calculate total time
                    result.metrics.totalTime = (parseFloat(result.metrics.retrievalTime) + parseFloat(result.metrics.generationTime)).toFixed(2);
                }
            }
            
            // Display results
            displayResults(result);
            
        } catch (error) {
            console.error('Error processing query:', error);
            errorText.textContent = error.message || 'An error occurred while processing your query.';
            errorMessage.style.display = 'block';
        } finally {
            loadingSpinner.style.display = 'none';
        }
    }
    
    // Function to display results
    function displayResults(result) {
        // Clear previous results
        documentsContainer.innerHTML = '';
        
        // Display documents
        result.documents.forEach((doc, index) => {
            const docElement = document.createElement('div');
            docElement.className = 'document-card';
            docElement.innerHTML = `
                <h5>Document ${index + 1} <small class="text-muted">(Score: ${doc.score.toFixed(2)})</small></h5>
                <p><strong>Source:</strong> ${doc.source}</p>
                <p>${doc.content}</p>
            `;
            documentsContainer.appendChild(docElement);
        });
        
        // Display response
        responseContent.innerHTML = result.response.replace(/\n/g, '<br>');
        
        // Update metrics
        retrievalTimeEl.textContent = result.metrics.retrievalTime + 's';
        generationTimeEl.textContent = result.metrics.generationTime + 's';
        totalTimeEl.textContent = result.metrics.totalTime + 's';
        
        // Show results container
        resultContainer.style.display = 'block';
        
        // Scroll to results
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    // Event listeners
    submitButton.addEventListener('click', () => {
        const query = queryInput.value.trim();
        if (query) {
            processQuery(query);
        }
    });
    
    queryInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const query = queryInput.value.trim();
            if (query) {
                processQuery(query);
            }
        }
    });
    
    // Sample query buttons
    sampleQueryButtons.forEach(button => {
        button.addEventListener('click', () => {
            const query = button.getAttribute('data-query');
            queryInput.value = query;
            processQuery(query);
        });
    });
    
    // Initialize highlight.js for code syntax highlighting
    document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightBlock(block);
    });
});

// Function to create a serverless API connection (placeholder for future implementation)
async function createServerlessApiClient() {
    // This would be implemented to connect to your serverless backend
    // For example, using AWS Lambda, Vercel Functions, or similar
    return {
        query: async (queryText, options = {}) => {
            // This would make an actual API call in a real implementation
            throw new Error('API not implemented yet');
        }
    };
}
