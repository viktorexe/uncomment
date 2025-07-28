import re
from .base_processor import BaseProcessor

class GoProcessor(BaseProcessor):
    """Go comment processor"""
    
    def __init__(self):
        super().__init__()
        self.single_line_patterns = [r'//.*$']
        self.multi_line_patterns = [(r'/\*', r'\*/')]
        self.string_delimiters = ['"', '`']
    
    def remove_comments(self, code: str) -> str:
        """Remove Go comments while handling raw strings"""
        # Handle raw string literals first
        result = self._handle_raw_strings(code)
        
        # Remove multi-line comments
        result = self._remove_multi_line_comments(result)
        
        # Remove single-line comments
        result = self._remove_single_line_comments(result)
        
        return result
    
    def _handle_raw_strings(self, code: str) -> str:
        """Handle Go raw string literals (backticks)"""
        result = []
        i = 0
        
        while i < len(code):
            if code[i] == '`':
                # Start of raw string
                raw_start = i
                i += 1
                
                while i < len(code) and code[i] != '`':
                    i += 1
                
                if i < len(code):
                    result.append(code[raw_start:i+1])
                    i += 1
            else:
                result.append(code[i])
                i += 1
        
        return ''.join(result)