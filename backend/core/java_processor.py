import re
from .base_processor import BaseProcessor

class JavaProcessor(BaseProcessor):
    """Java comment processor"""
    
    def __init__(self):
        super().__init__()
        self.single_line_patterns = [r'//.*$']
        self.multi_line_patterns = [(r'/\*\*?', r'\*/')]
        self.string_delimiters = ['"']
    
    def remove_comments(self, code: str) -> str:
        """Remove Java comments including JavaDoc"""
        # Remove multi-line comments (including JavaDoc)
        result = self._remove_multi_line_comments(code)
        
        # Remove single-line comments
        result = self._remove_single_line_comments(result)
        
        return result