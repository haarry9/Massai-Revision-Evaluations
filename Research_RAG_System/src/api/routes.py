from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.models.schemas import CrawlRequest, CrawlResponse, QueryRequest, QueryResponse, Source
from src.crawler.beautifulsoup_crawler import BeautifulSoupCrawler
from src.vectorstore.chroma_store import ChromaVectorStore
from src.retrieval.hybrid_retriever import HybridRetriever
from src.generation.rag_chain import RAGChain
from src.processing.text_cleaner import TextCleaner
from src.processing.chunker import TextChunker
from src.api.dependencies import (
    get_crawler,
    get_vector_store,
    get_retriever,
    get_rag_chain,
    get_text_cleaner,
    get_text_chunker
)

router = APIRouter()


@router.post("/crawl", response_model=CrawlResponse)
async def crawl_urls(
    request: CrawlRequest,
    crawler: BeautifulSoupCrawler = Depends(get_crawler),
    vector_store: ChromaVectorStore = Depends(get_vector_store),
    text_cleaner: TextCleaner = Depends(get_text_cleaner),
    text_chunker: TextChunker = Depends(get_text_chunker)
):
    """
    Crawl product URLs and store in vector database
    
    This endpoint:
    1. Crawls each URL
    2. Extracts text and metadata
    3. Cleans and chunks the text
    4. Generates embeddings
    5. Stores in vector database
    """
    try:
        total_chunks = 0
        documents_processed = 0
        
        for url in request.urls:
            # Crawl the URL
            crawl_result = crawler.crawl(str(url))
            
            if not crawl_result['text']:
                print(f"No content extracted from {url}")
                continue
            
            # Clean the text
            clean_text = text_cleaner.clean(crawl_result['text'])
            
            # Chunk the text
            chunks = text_chunker.chunk_text(clean_text, crawl_result['metadata'])
            
            if not chunks:
                print(f"No chunks created from {url}")
                continue
            
            # Add to vector store
            vector_store.add_documents(chunks)
            
            total_chunks += len(chunks)
            documents_processed += 1
        
        return CrawlResponse(
            status="success",
            documents_processed=documents_processed,
            chunks_created=total_chunks,
            message=f"Successfully processed {documents_processed} documents into {total_chunks} chunks"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during crawl: {str(e)}")


@router.post("/query", response_model=QueryResponse)
async def query_products(
    request: QueryRequest,
    retriever: HybridRetriever = Depends(get_retriever),
    rag_chain: RAGChain = Depends(get_rag_chain)
):
    """
    Query the product database using natural language
    
    This endpoint:
    1. Processes the query
    2. Retrieves relevant documents
    3. Applies any filters
    4. Generates an answer using LLM
    """
    try:
        # Retrieve relevant documents
        retrieved_docs = retriever.retrieve(request.query, top_k=5)
        
        # Apply additional filters if provided
        if request.filters:
            retrieved_docs = retriever.filter_by_price(retrieved_docs, request.filters)
        
        if not retrieved_docs:
            return QueryResponse(
                answer="I couldn't find any products matching your query.",
                sources=[],
                query=request.query
            )
        
        # Generate answer
        answer = rag_chain.generate(request.query, retrieved_docs)
        
        # Format sources
        sources = [
            Source(
                content=doc['content'][:500] + "...",  # Truncate for response
                metadata=doc['metadata'],
                relevance_score=doc.get('score')
            )
            for doc in retrieved_docs
        ]
        
        return QueryResponse(
            answer=answer,
            sources=sources,
            query=request.query
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during query: {str(e)}")


@router.get("/health")
async def health_check(vector_store: ChromaVectorStore = Depends(get_vector_store)):
    """Health check endpoint"""
    try:
        count = vector_store.get_collection_count()
        return {
            "status": "healthy",
            "documents_in_db": count
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }