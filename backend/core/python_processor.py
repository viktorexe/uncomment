import re
from .base_processor import BaseProcessor

class PythonProcessor(BaseProcessor):
    """Python comment processor with docstring preservation"""
    
    def __init__(self):
        super().__init__()
        self.single_line_patterns = [r'#.*$']
        self.multi_line_patterns = []
        self.string_delimiters = ['"', "'"]
    
    def remove_comments(self, code: str) -> str:
        """Remove Python comments while preserving docstrings"""
        # Remove single-line comments
        result = self._remove_single_line_comments(code)
        
        # Handle triple-quoted strings (preserve docstrings at function/class level)
        result = self._handle_docstrings(result)
        
        return result
    
    def _handle_docstrings(self, code: str) -> str:
        """Preserve docstrings but remove standalone triple-quoted comments"""
        lines = code.split('\n')
        result = []
        in_triple_quote = False
        triple_quote_type = None
        quote_start_line = 0
        is_docstring = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            if not in_triple_quote:
                # Check for start of triple quote
                if '"""' in line or "'''" in line:
                    quote_pos_double = line.find('"""')
                    quote_pos_single = line.find("'''")
                    
                    if quote_pos_double != -1 and (quote_pos_single == -1 or quote_pos_double < quote_pos_single):
                        triple_quote_type = '"""'
                        quote_pos = quote_pos_double
                    elif quote_pos_single != -1:
                        triple_quote_type = "'''"
                        quote_pos = quote_pos_single
                    else:
                        result.append(line)
                        continue
                    
                    # Check if it's a docstring (follows def/class)
                    is_docstring = self._is_docstring_context(result)
                    
                    # Check if triple quote closes on same line
                    remaining = line[quote_pos + 3:]
                    if triple_quote_type in remaining:
                        if is_docstring:
                            result.append(line)
                        # else: skip standalone triple-quoted comment
                    else:
                        in_triple_quote = True
                        quote_start_line = i
                        if is_docstring:
                            result.append(line)
                else:
                    result.append(line)
            else:
                # In triple quote, look for end
                if triple_quote_type in line:
                    in_triple_quote = False
                    if is_docstring:
                        result.append(line)
                    triple_quote_type = None
                elif is_docstring:
                    result.append(line)
        
        return '\n'.join(result)
    
    def _is_docstring_context(self, previous_lines: list) -> bool:
        """Check if we're in a context where triple quotes would be a docstring"""
        for line in reversed(previous_lines[-10:]):  # Check last 10 lines
            stripped = line.strip()
            if stripped.startswith(('def ', 'class ', 'async def ')):
                return True
            if stripped and not stripped.startswith(('@', 'def ', 'class ', 'async def ')):
                break
        return False