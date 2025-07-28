import re
from .base_processor import BaseProcessor

class RustProcessor(BaseProcessor):
    """Rust comment processor"""
    
    def __init__(self):
        super().__init__()
        self.single_line_patterns = [r'//.*$']
        self.multi_line_patterns = [(r'/\*', r'\*/')]
        self.string_delimiters = ['"']
    
    def remove_comments(self, code: str) -> str:
        """Remove Rust comments while handling raw strings"""
        # Handle raw string literals
        result = self._handle_raw_strings(code)
        
        # Remove multi-line comments
        result = self._remove_multi_line_comments(result)
        
        # Remove single-line comments
        result = self._remove_single_line_comments(result)
        
        return result
    
    def _handle_raw_strings(self, code: str) -> str:
        """Handle Rust raw string literals r#"..."#"""
        raw_string_pattern = r'r(#*)"(.*?)"\1'
        
        def preserve_raw_string(match):
            return match.group(0)  # Return unchanged
        
        return re.sub(raw_string_pattern, preserve_raw_string, code, flags=re.DOTALL)