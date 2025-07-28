import re
from .base_processor import BaseProcessor

class CProcessor(BaseProcessor):
    """C/C++ comment processor"""
    
    def __init__(self):
        super().__init__()
        self.single_line_patterns = [r'//.*$']
        self.multi_line_patterns = [(r'/\*', r'\*/')]
        self.string_delimiters = ['"', "'"]
    
    def remove_comments(self, code: str) -> str:
        """Remove C/C++ comments while handling preprocessor directives"""
        # Handle preprocessor directives
        result = self._handle_preprocessor(code)
        
        # Remove multi-line comments
        result = self._remove_multi_line_comments(result)
        
        # Remove single-line comments
        result = self._remove_single_line_comments(result)
        
        return result
    
    def _handle_preprocessor(self, code: str) -> str:
        """Preserve preprocessor directives that might contain // or /*"""
        lines = code.split('\n')
        result = []
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#'):
                # Preprocessor directive - preserve as is
                result.append(line)
            else:
                result.append(line)
        
        return '\n'.join(result)

class CppProcessor(CProcessor):
    """C++ specific processor (inherits from C)"""
    pass