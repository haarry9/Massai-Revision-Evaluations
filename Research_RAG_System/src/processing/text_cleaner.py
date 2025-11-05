import re


class TextCleaner:
    """Cleans and normalizes text content"""
    
    @staticmethod
    def clean(text: str) -> str:
        """
        Clean text by removing extra whitespace and normalizing
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-$€₹£¥]', '', text)
        
        # Remove multiple periods
        text = re.sub(r'\.{2,}', '.', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text