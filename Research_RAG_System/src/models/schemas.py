from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any


class CrawlRequest(BaseModel):
    """Request model for crawling URLs"""
    urls: List[HttpUrl] = Field(..., description="List of product page URLs to crawl")
    
    class Config:
        json_schema_extra = {
            "example": {
                "urls": [
                    "https://www.amazon.com/product/example",
                    "https://www.ebay.com/product/example"
                ]
            }
        }


class CrawlResponse(BaseModel):
    """Response model after crawling"""
    status: str = Field(..., description="Status of the crawl operation")
    documents_processed: int = Field(..., description="Number of documents processed")
    chunks_created: int = Field(..., description="Number of text chunks created")
    message: str = Field(..., description="Human-readable message")


class QueryRequest(BaseModel):
    """Request model for querying the RAG system"""
    query: str = Field(..., description="Natural language query")
    filters: Optional[Dict[str, Any]] = Field(None, description="Optional metadata filters")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Find products under $50",
                "filters": {"price_max": 50}
            }
        }


class Source(BaseModel):
    """Model for a single source document"""
    content: str = Field(..., description="Text content of the source")
    metadata: Dict[str, Any] = Field(..., description="Metadata about the source")
    relevance_score: Optional[float] = Field(None, description="Similarity score")


class QueryResponse(BaseModel):
    """Response model for queries"""
    answer: str = Field(..., description="Generated answer from the RAG system")
    sources: List[Source] = Field(..., description="Source documents used to generate the answer")
    query: str = Field(..., description="Original query")


class ProductMetadata(BaseModel):
    """Metadata extracted from product pages"""
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[str] = None
    tags: Optional[List[str]] = None
    url: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values"""
        return {k: v for k, v in self.model_dump().items() if v is not None}