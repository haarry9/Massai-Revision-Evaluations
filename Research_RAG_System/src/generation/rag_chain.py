from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.config.settings import settings


class RAGChain:
    """RAG pipeline for generating answers from retrieved documents"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            api_key=settings.openai_api_key,
            temperature=0.7
        )
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful product research assistant. 
            Use the following product information to answer the user's question.
            If you cannot find relevant information in the context, say so.
            Always be specific and cite the product details when available.
            
            Context:
            {context}
            """),
            ("human", "{question}")
        ])
    
    def generate(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
        """
        Generate answer using retrieved documents
        
        Args:
            query: User's question
            retrieved_docs: List of retrieved documents with metadata
            
        Returns:
            Generated answer
        """
        # Format context from retrieved documents
        context = self._format_context(retrieved_docs)
        
        # Create prompt
        messages = self.prompt_template.format_messages(
            context=context,
            question=query
        )
        
        # Generate response
        response = self.llm.invoke(messages)
        
        return response.content
    
    def _format_context(self, docs: List[Dict[str, Any]]) -> str:
        """Format retrieved documents into context string"""
        if not docs:
            return "No relevant information found."
        
        context_parts = []
        for i, doc in enumerate(docs, 1):
            metadata = doc.get('metadata', {})
            content = doc.get('content', '')
            
            # Build context entry
            entry = f"[Product {i}]\n"
            if metadata.get('title'):
                entry += f"Title: {metadata['title']}\n"
            if metadata.get('price'):
                entry += f"Price: {metadata['price']}\n"
            if metadata.get('url'):
                entry += f"URL: {metadata['url']}\n"
            entry += f"Description: {content[:500]}...\n"  # Limit content length
            
            context_parts.append(entry)
        
        return "\n\n".join(context_parts)