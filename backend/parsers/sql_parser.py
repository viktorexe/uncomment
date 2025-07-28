from .base_parser import BaseParser
from typing import List, Tuple

class SqlParser(BaseParser):
    def get_string_patterns(self) -> List[str]:
        return [
            r"'(?:[^'\\]|\\.)*'",  # Single quoted strings
            r'"(?:[^"\\]|\\.)*"',  # Double quoted identifiers
        ]
    
    def get_comment_patterns(self) -> List[str]:
        return [r'--.*$']
    
    def get_multiline_comment_patterns(self) -> List[Tuple[str, str]]:
        return [(r'/\*', r'\*/')]