"""
Streamlit Web UI for ModernRAG

This module provides a web interface for interacting with the ModernRAG system.
"""

import os
import asyncio
import time
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
import streamlit as st
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv

# Import ModernRAG components
from modernrag.vector_store import (
    check_index_exists,
    similarity_search,
    split_and_upsert_documents
)
from modernrag.generation import (
    retrieve_augment_generate,
    rerank_documents,
    augment_documents,
    generate_response,
    generation_manager,
    augmentation_manager
)
from modernrag.caching import (
    get_cached_result,
    cache_result,
    clear_cache,
    clear_expired_cache
)
from langchain.docstore.document import Document

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="ModernRAG",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Modern color palette */
    :root {
        --primary: #1E88E5;       /* Blue */
        --primary-dark: #1565C0;  /* Darker Blue */
        --secondary: #43A047;     /* Green */
        --secondary-dark: #2E7D32; /* Darker Green */
        --accent: #7E57C2;        /* Purple */
        --text-primary: #212121;  /* Near Black */
        --text-secondary: #424242; /* Dark Gray */
        --text-tertiary: #616161; /* Medium Gray */
        --background-light: #FAFAFA; /* Off White */
        --background-card: #FFFFFF; /* White */
        --border-light: #E0E0E0;  /* Light Gray */
        --warning: #FB8C00;       /* Orange */
        --error: #E53935;         /* Red */
    }
    
    /* Base text styling */
    body {
        color: var(--text-primary);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Main header styling */
    .main-header {
        font-size: 2.8rem;
        color: var(--primary-dark) !important;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 600;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Sub header styling */
    .sub-header {
        font-size: 1.6rem;
        color: var(--secondary-dark) !important;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 500;
        border-bottom: 2px solid var(--border-light);
        padding-bottom: 0.5rem;
    }
    
    /* Info box styling */
    .info-box {
        background-color: var(--background-light);
        padding: 1.2rem;
        border-radius: 0.75rem;
        margin-bottom: 1.5rem;
        color: var(--text-secondary) !important;
        border: 1px solid var(--border-light);
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    
    /* Document box styling */
    .document-box {
        background-color: #EEF5FD;
        padding: 1.2rem;
        border-radius: 0.75rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid var(--primary);
        color: var(--text-secondary) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: transform 0.2s ease;
    }
    
    .document-box:hover {
        transform: translateY(-2px);
    }
    
    .document-box strong, .document-box b {
        color: var(--primary-dark) !important;
    }
    
    /* Response box styling */
    .response-box {
        background-color: #EEFAF0;
        padding: 1.2rem;
        border-radius: 0.75rem;
        margin-top: 1.5rem;
        border-left: 4px solid var(--secondary);
        color: var(--text-secondary) !important;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
    }
    
    /* Metric card styling */
    .metric-card {
        background-color: var(--background-card);
        padding: 1.2rem;
        border-radius: 0.75rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        color: var(--text-secondary) !important;
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .metric-card:hover {
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        transform: translateY(-3px);
    }
    
    /* Cache status styling */
    .cache-hit {
        color: var(--secondary) !important;
        font-weight: 600;
    }
    
    .cache-miss {
        color: var(--warning) !important;
        font-weight: 600;
    }
    
    /* Streamlit component overrides */
    .stTextInput > label, .stNumberInput > label, .stSelectbox > label,
    .stMultiselect > label, .stSlider > label {
        color: var(--text-secondary) !important;
        font-weight: 500;
    }
    
    .stButton > button {
        background-color: var(--primary);
        color: white !important;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: var(--primary-dark);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Fix expander styling */
    .streamlit-expanderHeader {
        color: var(--text-secondary) !important;
        font-weight: 500;
        background-color: var(--background-light);
        border-radius: 0.5rem;
    }
    
    /* Fix tabs styling */
    .stTabs [data-baseweb="tab"] {
        color: var(--text-secondary) !important;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--primary);
    }
    
    /* Fix metric styling */
    .stMetricValue {
        color: var(--primary-dark) !important;
        font-weight: 600;
    }
    
    .stMetricLabel {
        color: var(--text-tertiary) !important;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: var(--background-light);
    }
    
    /* Ensure all headings are styled consistently */
    h1, h2, h3 {
        color: var(--primary-dark) !important;
        font-weight: 600;
    }
    
    h4, h5, h6 {
        color: var(--text-secondary) !important;
        font-weight: 500;
    }
    
    /* Style links */
    a {
        color: var(--primary) !important;
        text-decoration: none;
        transition: color 0.2s ease;
    }
    
    a:hover {
        color: var(--primary-dark) !important;
        text-decoration: underline;
    }
    
    /* Style code blocks */
    code {
        background-color: #F5F5F5;
        padding: 0.2rem 0.4rem;
        border-radius: 0.25rem;
        color: var(--accent) !important;
        font-family: 'Consolas', 'Monaco', monospace;
    }
    
    /* Style tables */
    table {
        border-collapse: collapse;
        width: 100%;
    }
    
    th {
        background-color: var(--background-light);
        color: var(--text-secondary) !important;
        font-weight: 600;
        text-align: left;
        padding: 0.75rem;
        border-bottom: 2px solid var(--border-light);
    }
    
    td {
        padding: 0.75rem;
        border-bottom: 1px solid var(--border-light);
        color: var(--text-secondary) !important;
    }
    
    tr:nth-child(even) {
        background-color: var(--background-light);
    }

</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'metrics' not in st.session_state:
    st.session_state.metrics = {
        'total_queries': 0,
        'cache_hits': 0,
        'avg_response_time': 0,
        'total_response_time': 0,
    }

# Sidebar
with st.sidebar:
    st.markdown("## Configuration")
    
    # Index selection
    index_name = st.text_input("Index Name", value="langchain-test-index")
    
    # Search parameters
    st.markdown("### Search Parameters")
    k = st.slider("Number of documents to retrieve (k)", min_value=1, max_value=10, value=4)
    score_threshold = st.slider("Score threshold", min_value=0.0, max_value=1.0, value=0.4, step=0.05)
    rerank_top_k = st.slider("Number of documents to keep after reranking", min_value=1, max_value=5, value=3)
    
    # Cache settings
    st.markdown("### Cache Settings")
    use_cache = st.checkbox("Use query cache", value=True)
    
    if st.button("Clear Cache"):
        asyncio.run(clear_cache())
        st.success("Cache cleared successfully!")
    
    if st.button("Clear Expired Cache"):
        asyncio.run(clear_expired_cache())
        st.success("Expired cache entries cleared!")
    
    # Document upload
    st.markdown("### Document Upload")
    uploaded_file = st.file_uploader("Upload a text document", type=["txt", "md", "pdf"])
    
    if uploaded_file is not None:
        # Process the uploaded file
        if st.button("Index Document"):
            try:
                # Read the file content
                content = uploaded_file.read().decode("utf-8")
                
                # Create a document
                doc = Document(
                    page_content=content,
                    metadata={"source": uploaded_file.name, "page": 1}
                )
                
                # Add to session state
                st.session_state.documents.append(doc)
                
                # Index the document
                with st.spinner("Indexing document..."):
                    success = asyncio.run(split_and_upsert_documents(
                        documents=[doc],
                        index_name=index_name,
                        batch_size=50
                    ))
                
                if success:
                    st.success(f"Document '{uploaded_file.name}' indexed successfully!")
                else:
                    st.error(f"Failed to index document '{uploaded_file.name}'")
            
            except Exception as e:
                st.error(f"Error indexing document: {str(e)}")
    
    # Metrics
    st.markdown("### Metrics")
    st.metric("Total Queries", st.session_state.metrics['total_queries'])
    st.metric("Cache Hit Rate", f"{(st.session_state.metrics['cache_hits'] / max(1, st.session_state.metrics['total_queries'])) * 100:.1f}%")
    st.metric("Avg Response Time", f"{st.session_state.metrics['avg_response_time']:.2f}s")

# Main content
st.markdown("<h1 class='main-header'>ModernRAG</h1>", unsafe_allow_html=True)
st.markdown("<p class='info-box'>Ask questions and get answers based on the indexed documents.</p>", unsafe_allow_html=True)

# Query input
query = st.text_input("Enter your query:", placeholder="What is Retrieval-Augmented Generation?")

# Process query
if query:
    # Update metrics
    st.session_state.metrics['total_queries'] += 1
    
    # Process the query
    with st.spinner("Processing query..."):
        start_time = time.time()
        
        try:
            # Ensure index exists
            asyncio.run(check_index_exists(index_name))
            
            # Run the RAG pipeline
            result = asyncio.run(retrieve_augment_generate(
                query=query,
                index_name=index_name,
                k=k,
                score_threshold=score_threshold,
                rerank_top_k=rerank_top_k,
                use_cache=use_cache
            ))
            
            # Update metrics
            end_time = time.time()
            response_time = end_time - start_time
            
            if result.get('cached', False):
                st.session_state.metrics['cache_hits'] += 1
                cache_status = "<span class='cache-hit'>Cache Hit</span>"
            else:
                cache_status = "<span class='cache-miss'>Cache Miss</span>"
            
            # Update average response time
            total_time = st.session_state.metrics['total_response_time'] + response_time
            st.session_state.metrics['total_response_time'] = total_time
            st.session_state.metrics['avg_response_time'] = total_time / st.session_state.metrics['total_queries']
            
            # Add to history
            history_item = {
                'query': query,
                'response': result['response'],
                'retrieved_docs': result.get('retrieved_docs', []),
                'timestamp': time.time(),
                'response_time': response_time,
                'cached': result.get('cached', False)
            }
            st.session_state.history.insert(0, history_item)  # Add to the beginning
            
            # Display results
            st.markdown("<h2 class='sub-header'>Results</h2>", unsafe_allow_html=True)
            
            # Display response time and cache status
            st.markdown(f"<p>Response Time: {response_time:.2f}s | {cache_status}</p>", unsafe_allow_html=True)
            
            # Display retrieved documents
            if result.get('retrieved_docs'):
                with st.expander("Retrieved Documents", expanded=False):
                    for i, doc_tuple in enumerate(result['retrieved_docs']):
                        if isinstance(doc_tuple, tuple) and len(doc_tuple) == 2:
                            doc, score = doc_tuple
                            st.markdown(f"<div class='document-box'><strong>Document {i+1}</strong> (Score: {score:.4f})<br>"
                                      f"Source: {doc.metadata.get('source', 'Unknown')}<br>"
                                      f"Content: {doc.page_content[:200]}...</div>", 
                                      unsafe_allow_html=True)
            
            # Display augmented context
            if result.get('augmented_context'):
                with st.expander("Augmented Context", expanded=False):
                    st.markdown(result['augmented_context'])
            
            # Display response
            st.markdown("<h3>Response:</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='response-box'>{result['response']}</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")

# Display history
if st.session_state.history:
    st.markdown("<h2 class='sub-header'>Query History</h2>", unsafe_allow_html=True)
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["History", "Analytics"])
    
    with tab1:
        for i, item in enumerate(st.session_state.history[:10]):  # Show only the last 10 queries
            with st.expander(f"Query: {item['query']}", expanded=False):
                st.markdown(f"<p><strong>Time:</strong> {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['timestamp']))}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>Response Time:</strong> {item['response_time']:.2f}s | <strong>Cached:</strong> {'Yes' if item.get('cached', False) else 'No'}</p>", unsafe_allow_html=True)
                st.markdown("<strong>Response:</strong>")
                st.markdown(f"<div class='response-box'>{item['response']}</div>", unsafe_allow_html=True)
    
    with tab2:
        # Create analytics visualizations
        if len(st.session_state.history) > 1:
            # Response time chart
            response_times = [item['response_time'] for item in st.session_state.history]
            timestamps = [time.strftime('%H:%M:%S', time.localtime(item['timestamp'])) for item in st.session_state.history]
            cached = ["Cache Hit" if item.get('cached', False) else "Cache Miss" for item in st.session_state.history]
            
            df = pd.DataFrame({
                'Timestamp': timestamps,
                'Response Time (s)': response_times,
                'Cache Status': cached
            })
            
            fig = px.line(df, x='Timestamp', y='Response Time (s)', color='Cache Status', 
                         title='Response Time History', markers=True)
            st.plotly_chart(fig, use_container_width=True)
            
            # Cache hit rate
            cache_hits = sum(1 for item in st.session_state.history if item.get('cached', False))
            cache_misses = len(st.session_state.history) - cache_hits
            
            fig2 = px.pie(
                values=[cache_hits, cache_misses],
                names=['Cache Hits', 'Cache Misses'],
                title='Cache Performance',
                color_discrete_sequence=['#4CAF50', '#FF9800']
            )
            st.plotly_chart(fig2, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("ModernRAG - Retrieval-Augmented Generation System")
