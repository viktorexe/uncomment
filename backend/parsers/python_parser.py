from .base_parser import BaseParser
from typing import List, Tuple
import re

class PythonParser(BaseParser):
    def process(self, code: str):
        """Optimized Python comment removal"""
        if not code:
            return {'cleaned_code': '', 'comments_removed': 0}
        
        lines = code.split('\n')
        cleaned_lines = []
        comments_removed = 0
        
        for line in lines:
            cleaned_line, removed = self._process_line(line)
            cleaned_lines.append(cleaned_line)
            comments_removed += removed
        
        return {
            'cleaned_code': '\n'.join(cleaned_lines),
            'comments_removed': comments_removed
        }
    
    def _process_line(self, line: str):
        """Process single line for Python comments with maximum error handling"""
        if not line.strip():
            return line, 0
        

        if '#' not in line:
            return line, 0
        

        in_string = False
        string_char = None
        escape_next = False
        i = 0
        
        while i < len(line):
            char = line[i]
            

            if escape_next:
                escape_next = False
                i += 1
                continue
            
            if char == '\\':
                escape_next = True
                i += 1
                continue
            

            if not in_string and char in ['"', "'"]:

                if i + 2 < len(line) and line[i:i+3] == char * 3:

                    end_pos = line.find(char * 3, i + 3)
                    if end_pos != -1:
                        i = end_pos + 3
                        continue
                    else:

                        in_string = True
                        string_char = char
                        i += 3
                        continue
                

                if i > 0 and line[i-1].lower() in ['r', 'f', 'b', 'u']:
                    in_string = True
                    string_char = char
                elif i > 1 and line[i-2:i].lower() in ['rf', 'fr', 'rb', 'br']:
                    in_string = True
                    string_char = char
                else:
                    in_string = True
                    string_char = char
            
            elif in_string and char == string_char:
                in_string = False
                string_char = None
            

            elif not in_string and char == '#':

                return line[:i].rstrip(), 1
            
            i += 1
        
        return line, 0
    
    def get_string_patterns(self) -> List[str]:
        return []
    
    def get_comment_patterns(self) -> List[str]:
        return []
    
    def get_multiline_comment_patterns(self) -> List[Tuple[str, str]]:
        return []