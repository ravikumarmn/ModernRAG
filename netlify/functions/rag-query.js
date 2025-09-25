// Netlify Function for ModernRAG API
const { Configuration, OpenAIApi } = require('openai');
require('dotenv').config();

// Sample data for demo purposes (same as in frontend)
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

// Function to generate a response using OpenAI (for queries not in sample data)
async function generateResponse(query) {
  try {
    // Initialize OpenAI client
    const configuration = new Configuration({
      apiKey: process.env.OPENAI_API_KEY,
    });
    const openai = new OpenAIApi(configuration);
    
    // Generate a response
    const startTime = Date.now();
    const retrievalTime = (Math.random() * 0.5 + 0.2).toFixed(2);
    
    const completion = await openai.createChatCompletion({
      model: "gpt-3.5-turbo",
      messages: [
        { role: "system", content: "You are a helpful AI assistant that provides information about ModernRAG, a Retrieval-Augmented Generation system." },
        { role: "user", content: `Please provide information about: ${query}` }
      ],
      temperature: 0.7,
      max_tokens: 500,
    });
    
    const generationTime = ((Date.now() - startTime) / 1000).toFixed(2);
    const totalTime = (parseFloat(retrievalTime) + parseFloat(generationTime)).toFixed(2);
    
    return {
      documents: [
        {
          content: "This is a simulated document result for the query: " + query,
          source: "ModernRAG Documentation",
          score: 0.75
        }
      ],
      response: completion.data.choices[0].message.content,
      metrics: {
        retrievalTime: retrievalTime,
        generationTime: generationTime,
        totalTime: totalTime
      }
    };
  } catch (error) {
    console.error('Error generating response:', error);
    throw new Error('Failed to generate response');
  }
}

exports.handler = async function(event, context) {
  // Only allow POST requests
  if (event.httpMethod !== "POST") {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: "Method Not Allowed" }),
      headers: {
        "Allow": "POST",
        "Content-Type": "application/json"
      }
    };
  }
  
  try {
    // Parse the request body
    const body = JSON.parse(event.body);
    const { query } = body;
    
    if (!query) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: "Query parameter is required" }),
        headers: { "Content-Type": "application/json" }
      };
    }
    
    // Check if we have sample data for this query
    let result;
    if (sampleData[query]) {
      result = sampleData[query];
    } else {
      // For queries we don't have sample data for, generate a response
      result = await generateResponse(query);
    }
    
    // Return the result
    return {
      statusCode: 200,
      body: JSON.stringify(result),
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*" // Allow CORS for demo purposes
      }
    };
    
  } catch (error) {
    console.error('Error processing request:', error);
    
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Internal Server Error" }),
      headers: { "Content-Type": "application/json" }
    };
  }
};
