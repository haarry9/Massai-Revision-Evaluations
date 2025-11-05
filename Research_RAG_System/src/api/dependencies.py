from functools import lru_cache
from src.crawler.beautifulsoup_crawler import BeautifulSoupCrawler
from src.vectorstore.chroma_store import ChromaVectorStore
from src.retrieval.hybrid_retriever import HybridRetriever
from src.generation.rag_chain import RAGChain
from src.processing.text_cleaner import TextCleaner
from src.processing.chunker import TextChunker


@lru_cache()
def get_crawler() -> BeautifulSoupCrawler:
    """Get or create crawler instance"""
    return BeautifulSoupCrawler()


@lru_cache()
def get_vector_store() -> ChromaVectorStore:
    """Get or create vector store instance"""
    return ChromaVectorStore()


@lru_cache()
def get_retriever() -> HybridRetriever:
    """Get or create retriever instance"""
    vector_store = get_vector_store()
    return HybridRetriever(vector_store)


@lru_cache()
def get_rag_chain() -> RAGChain:
    """Get or create RAG chain instance"""
    return RAGChain()


@lru_cache()
def get_text_cleaner() -> TextCleaner:
    """Get or create text cleaner instance"""
    return TextCleaner()


@lru_cache()
def get_text_chunker() -> TextChunker:
    """Get or create text chunker instance"""
    return TextChunker()