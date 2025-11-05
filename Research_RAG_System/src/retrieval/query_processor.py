import re
from typing import Dict, Any, Optional


class QueryProcessor:
    """Processes natural language queries and extracts filters"""
    
    @staticmethod
    def extract_price_filter(query: str) -> Optional[Dict[str, Any]]:
        """
        Extract price filters from query
        
        Examples:
            "under $50" -> {"price_max": 50}
            "less than $100" -> {"price_max": 100}
            "above $30" -> {"price_min": 30}
        """
        filters = {}
        
        # Pattern for "under", "less than", "below"
        under_pattern = r'(?:under|less than|below|cheaper than)\s*\$?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)'
        match = re.search(under_pattern, query.lower())
        if match:
            price = float(match.group(1).replace(',', ''))
            filters['price_max'] = price
        
        # Pattern for "above", "more than", "over"
        over_pattern = r'(?:above|more than|over|greater than)\s*\$?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)'
        match = re.search(over_pattern, query.lower())
        if match:
            price = float(match.group(1).replace(',', ''))
            filters['price_min'] = price
        
        return filters if filters else None
    
    @staticmethod
    def process_query(query: str) -> Dict[str, Any]:
        """
        Process query and extract all filters
        
        Args:
            query: Natural language query
            
        Returns:
            Dictionary with 'query' and optional 'filters'
        """
        result = {
            'query': query,
            'filters': {}
        }
        
        # Extract price filters
        price_filters = QueryProcessor.extract_price_filter(query)
        if price_filters:
            result['filters'].update(price_filters)
        
        return result