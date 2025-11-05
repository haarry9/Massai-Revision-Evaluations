from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict, Any
from src.config.settings import settings


class TextChunker:
    """Splits text into manageable chunks for embedding"""
    
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
    
    def chunk_text(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Split text into chunks with metadata
        
        Args:
            text: Text to split
            metadata: Metadata to attach to each chunk
            
        Returns:
            List of dictionaries containing 'text' and 'metadata'
        """
        if not text or len(text.strip()) == 0:
            return []
        
        # Split text into chunks
        chunks = self.splitter.split_text(text)
        
        # Attach metadata to each chunk
        result = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = metadata.copy()
            chunk_metadata['chunk_index'] = i
            chunk_metadata['total_chunks'] = len(chunks)
            
            result.append({
                'text': chunk,
                'metadata': chunk_metadata
            })
        
        return result