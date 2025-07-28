import re
from .base_processor import BaseProcessor

class RubyProcessor(BaseProcessor):
    """Ruby comment processor"""
    
    def __init__(self):
        super().__init__()
        self.single_line_patterns = [r'#.*$']
        self.multi_line_patterns = [(r'=begin', r'=end')]
        self.string_delimiters = ['"', "'"]
    
    def remove_comments(self, code: str) -> str:
        """Remove Ruby comments including =begin/=end blocks"""
        # Remove multi-line comments (=begin/=end)
        result = self._remove_ruby_multiline(code)
        
        # Remove single-line comments
        result = self._remove_single_line_comments(result)
        
        return result
    
    def _remove_ruby_multiline(self, code: str) -> str:
        """Remove Ruby =begin/=end comment blocks"""
        lines = code.split('\n')
        result = []
        in_comment_block = False
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('=begin'):
                in_comment_block = True
                continue
            elif stripped.startswith('=end'):
                in_comment_block = False
                continue
            elif not in_comment_block:
                result.append(line)
        
        return '\n'.join(result)