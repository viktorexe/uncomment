import re
from .base_processor import BaseProcessor

class JavaScriptProcessor(BaseProcessor):
    """JavaScript/TypeScript comment processor"""
    
    def __init__(self):
        super().__init__()
        self.single_line_patterns = [r'//.*$']
        self.multi_line_patterns = [(r'/\*', r'\*/')]
        self.string_delimiters = ['"', "'", '`']
    
    def remove_comments(self, code: str) -> str:
        """Remove JavaScript comments while handling template literals"""
        # Handle template literals first
        result = self._handle_template_literals(code)
        
        # Remove multi-line comments
        result = self._remove_multi_line_comments(result)
        
        # Remove single-line comments
        result = self._remove_single_line_comments(result)
        
        return result
    
    def _handle_template_literals(self, code: str) -> str:
        """Handle template literals with embedded expressions"""
        result = []
        i = 0
        
        while i < len(code):
            if code[i] == '`':
                # Start of template literal
                template_start = i
                i += 1
                brace_depth = 0
                
                while i < len(code):
                    if code[i] == '\\':
                        i += 2  # Skip escaped character
                        continue
                    elif code[i] == '`' and brace_depth == 0:
                        # End of template literal
                        result.append(code[template_start:i+1])
                        i += 1
                        break
                    elif code[i:i+2] == '${':
                        brace_depth += 1
                        i += 2
                    elif code[i] == '}' and brace_depth > 0:
                        brace_depth -= 1
                        i += 1
                    else:
                        i += 1
            else:
                result.append(code[i])
                i += 1
        
        return ''.join(result)