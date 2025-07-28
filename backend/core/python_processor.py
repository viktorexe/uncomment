from .base_processor import BaseProcessor
from typing import List, Tuple

class PythonProcessor(BaseProcessor):
    def get_comment_patterns(self) -> Tuple[List[str], List[Tuple[str, str]]]:
        single_patterns = ['#']
        multi_patterns = [('"""', '"""'), ("'''", "'''")]
        return single_patterns, multi_patterns
    
    def remove_comments(self, code: str) -> str:
        # Handle docstrings specially for Python
        code = self._remove_docstrings(code)
        return super().remove_comments(code)
    
    def _remove_docstrings(self, code: str) -> str:
        lines = code.split('\n')
        result = []
        in_docstring = False
        docstring_delimiter = None
        indent_level = 0
        
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            if not in_docstring:
                # Check for docstring start
                if (stripped.startswith('"""') or stripped.startswith("'''")) and \
                   (i == 0 or lines[i-1].strip().endswith(':') or 
                    any(keyword in lines[i-1] for keyword in ['def ', 'class ', 'async def '])):
                    
                    docstring_delimiter = stripped[:3]
                    in_docstring = True
                    indent_level = len(line) - len(line.lstrip())
                    
                    # Check if docstring ends on same line
                    if stripped.count(docstring_delimiter) >= 2:
                        in_docstring = False
                        docstring_delimiter = None
                    i += 1
                    continue
                
                result.append(line)
            else:
                # In docstring, look for end
                if docstring_delimiter in stripped:
                    in_docstring = False
                    docstring_delimiter = None
                i += 1
                continue
            
            i += 1
        
        return '\n'.join(result)