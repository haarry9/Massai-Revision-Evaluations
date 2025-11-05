import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
from src.models.schemas import ProductMetadata
from src.crawler.metadata_extractor import MetadataExtractor


class BeautifulSoupCrawler:
    """Crawls web pages and extracts content using BeautifulSoup"""
    
    def __init__(self):
        self.extractor = MetadataExtractor()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def crawl(self, url: str) -> Dict[str, Any]:
        """
        Crawl a single URL and extract content and metadata
        
        Args:
            url: The URL to crawl
            
        Returns:
            Dictionary containing 'text' and 'metadata'
        """
        try:
            # Fetch the page
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract text content
            text_content = self._extract_text(soup)
            
            # Extract metadata
            metadata = self._extract_metadata(soup, response.text, url)
            
            return {
                'text': text_content,
                'metadata': metadata
            }
            
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")
            return {
                'text': '',
                'metadata': ProductMetadata(url=url).to_dict()
            }
    
    def _extract_text(self, soup: BeautifulSoup) -> str:
        """Extract clean text from HTML"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def _extract_metadata(self, soup: BeautifulSoup, html_text: str, url: str) -> Dict[str, Any]:
        """Extract metadata from the page"""
        metadata = ProductMetadata(
            title=self.extractor.extract_title(soup),
            description=self.extractor.extract_description(soup),
            price=self.extractor.extract_price(soup, html_text),
            tags=self.extractor.extract_tags(soup),
            url=url
        )
        
        return metadata.to_dict()