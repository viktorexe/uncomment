from .base_parser import BaseParser
from typing import List, Tuple

class ScalaParser(BaseParser):
    def get_string_patterns(self) -> List[str]:
        return [
            r'"(?:[^"\\]|\\.)*"',  # Double quoted strings
            r"'(?:[^'\\]|\\.)*'",  # Single quoted chars
            r'""".*?"""',          # Multi-line strings
        ]
    
    def get_comment_patterns(self) -> List[str]:
        return [r'//.*$']
    
    def get_multiline_comment_patterns(self) -> List[Tuple[str, str]]:
        return [(r'/\*', r'\*/')]