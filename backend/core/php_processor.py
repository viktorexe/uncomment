import re
from .base_processor import BaseProcessor

class PhpProcessor(BaseProcessor):
    """PHP comment processor"""
    
    def __init__(self):
        super().__init__()
        self.single_line_patterns = [r'//.*$', r'#.*$']
        self.multi_line_patterns = [(r'/\*', r'\*/')]
        self.string_delimiters = ['"', "'"]
    
    def remove_comments(self, code: str) -> str:
        """Remove PHP comments while handling heredoc/nowdoc"""
        # Handle heredoc/nowdoc first
        result = self._handle_heredoc(code)
        
        # Remove multi-line comments
        result = self._remove_multi_line_comments(result)
        
        # Remove single-line comments
        result = self._remove_single_line_comments(result)
        
        return result
    
    def _handle_heredoc(self, code: str) -> str:
        """Handle PHP heredoc and nowdoc syntax"""
        # Simplified heredoc handling
        heredoc_pattern = r'<<<\s*(["\']?)(\w+)\1\s*\n(.*?)\n\2;'
        
        def preserve_heredoc(match):
            return match.group(0)  # Return unchanged
        
        return re.sub(heredoc_pattern, preserve_heredoc, code, flags=re.DOTALL)