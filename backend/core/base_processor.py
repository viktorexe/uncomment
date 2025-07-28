from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
import re

class BaseProcessor(ABC):
    """Base class for language-specific comment processors"""
    
    def __init__(self):
        self.single_line_patterns: List[str] = []
        self.multi_line_patterns: List[Tuple[str, str]] = []
        self.string_delimiters: List[str] = []
    
    @abstractmethod
    def remove_comments(self, code: str) -> str:
        """Remove comments from source code"""
        pass
    
    def _is_in_string(self, code: str, position: int) -> bool:
        """Check if position is inside a string literal"""
        before = code[:position]
        in_string = False
        escape_next = False
        current_delimiter = None
        
        for char in before:
            if escape_next:
                escape_next = False
                continue
                
            if char == '\\':
                escape_next = True
                continue
                
            if not in_string:
                if char in self.string_delimiters:
                    in_string = True
                    current_delimiter = char
            else:
                if char == current_delimiter:
                    in_string = False
                    current_delimiter = None
                    
        return in_string
    
    def _remove_single_line_comments(self, code: str) -> str:
        """Remove single-line comments while preserving strings"""
        lines = code.split('\n')
        result = []
        
        for line in lines:
            cleaned_line = line
            for pattern in self.single_line_patterns:
                match = re.search(pattern, line)
                if match and not self._is_in_string(line, match.start()):
                    cleaned_line = line[:match.start()].rstrip()
                    break
            result.append(cleaned_line)
            
        return '\n'.join(result)
    
    def _remove_multi_line_comments(self, code: str) -> str:
        """Remove multi-line comments while preserving strings"""
        result = code
        
        for start_pattern, end_pattern in self.multi_line_patterns:
            while True:
                start_match = re.search(start_pattern, result)
                if not start_match or self._is_in_string(result, start_match.start()):
                    break
                    
                end_match = re.search(end_pattern, result[start_match.end():])
                if not end_match:
                    result = result[:start_match.start()]
                    break
                    
                end_pos = start_match.end() + end_match.end()
                result = result[:start_match.start()] + result[end_pos:]
                
        return result