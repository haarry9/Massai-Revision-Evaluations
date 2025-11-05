from bs4 import BeautifulSoup
import re
from typing import Optional, List


class MetadataExtractor:
    """Extracts product metadata from HTML content"""
    
    @staticmethod
    def extract_title(soup: BeautifulSoup) -> Optional[str]:
        """Extract product title from various sources"""
        # Try meta og:title first
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            return og_title.get("content").strip()
        
        # Try regular title tag
        if soup.title and soup.title.string:
            return soup.title.string.strip()
        
        # Try h1 tag
        h1 = soup.find("h1")
        if h1:
            return h1.get_text().strip()
        
        return None
    
    @staticmethod
    def extract_description(soup: BeautifulSoup) -> Optional[str]:
        """Extract product description"""
        # Try meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            return meta_desc.get("content").strip()
        
        # Try og:description
        og_desc = soup.find("meta", property="og:description")
        if og_desc and og_desc.get("content"):
            return og_desc.get("content").strip()
        
        # Try first paragraph
        p = soup.find("p")
        if p:
            return p.get_text().strip()
        
        return None
    
    @staticmethod
    def extract_price(soup: BeautifulSoup, html_text: str) -> Optional[str]:
        """Extract price using regex patterns"""
        # Common price patterns
        price_patterns = [
            r'\$\s*\d+(?:,\d{3})*(?:\.\d{2})?',  # $1,234.56
            r'USD\s*\d+(?:,\d{3})*(?:\.\d{2})?',  # USD 1234.56
            r'₹\s*\d+(?:,\d{3})*(?:\.\d{2})?',    # ₹1,234.56
            r'€\s*\d+(?:,\d{3})*(?:\.\d{2})?',    # €1,234.56
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, html_text)
            if match:
                return match.group(0).strip()
        
        return None
    
    @staticmethod
    def extract_tags(soup: BeautifulSoup) -> Optional[List[str]]:
        """Extract keywords/tags"""
        meta_keywords = soup.find("meta", attrs={"name": "keywords"})
        if meta_keywords and meta_keywords.get("content"):
            keywords = meta_keywords.get("content")
            return [k.strip() for k in keywords.split(",") if k.strip()]
        
        return None