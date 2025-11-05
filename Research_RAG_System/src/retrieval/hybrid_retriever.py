from typing import List, Dict, Any
from src.vectorstore.chroma_store import ChromaVectorStore
from src.retrieval.query_processor import QueryProcessor


class HybridRetriever:
    """Performs hybrid retrieval combining semantic search and metadata filtering"""
    
    def __init__(self, vector_store: ChromaVectorStore):
        self.vector_store = vector_store
        self.query_processor = QueryProcessor()
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents using hybrid search
        
        Args:
            query: Natural language query
            top_k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        # Process query to extract filters
        processed = self.query_processor.process_query(query)
        
        # Build Chroma filter if price constraints exist
        chroma_filter = None
        if processed['filters']:
            chroma_filter = self._build_chroma_filter(processed['filters'])
        
        # Perform similarity search
        results = self.vector_store.similarity_search(
            query=processed['query'],
            k=top_k,
            filter=chroma_filter
        )
        
        return results
    
    def _build_chroma_filter(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert our filter format to Chroma's filter format
        
        Note: This is a simplified version. Chroma filtering works with
        exact metadata matches. For numeric comparisons, we'd need to
        store price as a numeric field and use Chroma's where clause.
        """
        # For now, we'll return None and handle filtering post-retrieval
        # In production, you'd want to store numeric price and use Chroma's $gt, $lt operators
        return None
    
    def filter_by_price(self, results: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filter results by price after retrieval (fallback method)
        
        Args:
            results: Retrieved documents
            filters: Price filters to apply
            
        Returns:
            Filtered results
        """
        filtered_results = []
        
        for result in results:
            price_str = result.get('metadata', {}).get('price')
            if not price_str:
                # Include items without price
                filtered_results.append(result)
                continue
            
            # Extract numeric price
            try:
                import re
                price_match = re.search(r'(\d+(?:,\d{3})*(?:\.\d{2})?)', price_str)
                if price_match:
                    price = float(price_match.group(1).replace(',', ''))
                    
                    # Apply filters
                    if 'price_max' in filters and price > filters['price_max']:
                        continue
                    if 'price_min' in filters and price < filters['price_min']:
                        continue
                    
                    filtered_results.append(result)
            except:
                # If price parsing fails, include the item
                filtered_results.append(result)
        
        return filtered_results