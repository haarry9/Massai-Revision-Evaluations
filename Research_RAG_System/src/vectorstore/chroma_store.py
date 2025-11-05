from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from src.config.settings import settings


class ChromaVectorStore:
    """Manages the Chroma vector database"""
    
    def __init__(self):
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openai_api_key
        )
        
        # Initialize Chroma client with persistent storage
        self.client = chromadb.PersistentClient(
            path=settings.vector_db_path,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Initialize or get collection
        self.vectorstore = Chroma(
            client=self.client,
            collection_name=settings.collection_name,
            embedding_function=self.embeddings
        )
    
    def add_documents(self, chunks: List[Dict[str, Any]]) -> List[str]:
        """
        Add document chunks to the vector store
        
        Args:
            chunks: List of dictionaries with 'text' and 'metadata'
            
        Returns:
            List of document IDs
        """
        if not chunks:
            return []
        
        texts = [chunk['text'] for chunk in chunks]
        metadatas = [chunk['metadata'] for chunk in chunks]
        
        # Add to vector store
        ids = self.vectorstore.add_texts(
            texts=texts,
            metadatas=metadatas
        )
        
        return ids
    
    def similarity_search(
        self, 
        query: str, 
        k: int = None,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents
        
        Args:
            query: Search query
            k: Number of results to return
            filter: Optional metadata filters
            
        Returns:
            List of documents with content and metadata
        """
        if k is None:
            k = settings.top_k_results
        
        # Perform search
        if filter:
            results = self.vectorstore.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter
            )
        else:
            results = self.vectorstore.similarity_search_with_score(
                query=query,
                k=k
            )
        
        # Format results
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                'content': doc.page_content,
                'metadata': doc.metadata,
                'score': float(score)
            })
        
        return formatted_results
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection"""
        collection = self.client.get_collection(settings.collection_name)
        return collection.count()