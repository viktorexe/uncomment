from abc import ABC, abstractmethod
import re
from typing import List, Tuple

class BaseProcessor(ABC):
    def __init__(self):
        self.single_line_patterns = []
        self.multi_line_patterns = []
        self.string_delimiters = []
    
    @abstractmethod
    def get_comment_patterns(self) -> Tuple[List[str], List[Tuple[str, str]]]:
        pass
    
    def remove_comments(self, code: str) -> str:
        single_patterns, multi_patterns = self.get_comment_patterns()
        
        # Handle multi-line comments first
        for start, end in multi_patterns:
            code = self._remove_multiline_comments(code, start, end)
        
        # Handle single-line comments
        for pattern in single_patterns:
            code = self._remove_single_line_comments(code, pattern)
        
        return self._clean_empty_lines(code)
    
    def _remove_multiline_comments(self, code: str, start: str, end: str) -> str:
        result = []
        i = 0
        in_string = False
        string_char = None
        
        while i < len(code):
            if not in_string:
                if code[i:i+len(start)] == start:
                    # Find end of comment
                    j = i + len(start)
                    while j < len(code) - len(end) + 1:
                        if code[j:j+len(end)] == end:
                            i = j + len(end)
                            break
                        j += 1
                    else:
                        break
                    continue
                elif code[i] in ['"', "'", '`']:
                    in_string = True
                    string_char = code[i]
            else:
                if code[i] == string_char and (i == 0 or code[i-1] != '\\'):
                    in_string = False
                    string_char = None
            
            result.append(code[i])
            i += 1
        
        return ''.join(result)
    
    def _remove_single_line_comments(self, code: str, pattern: str) -> str:
        lines = code.split('\n')
        result = []
        
        for line in lines:
            in_string = False
            string_char = None
            i = 0
            
            while i < len(line):
                if not in_string:
                    if line[i:i+len(pattern)] == pattern:
                        line = line[:i].rstrip()
                        break
                    elif line[i] in ['"', "'", '`']:
                        in_string = True
                        string_char = line[i]
                else:
                    if line[i] == string_char and (i == 0 or line[i-1] != '\\'):
                        in_string = False
                        string_char = None
                i += 1
            
            result.append(line)
        
        return '\n'.join(result)
    
    def _clean_empty_lines(self, code: str) -> str:
        lines = code.split('\n')
        result = []
        
        for line in lines:
            if line.strip():
                result.append(line)
            elif result and result[-1].strip():
                result.append('')
        
        return '\n'.join(result).strip()