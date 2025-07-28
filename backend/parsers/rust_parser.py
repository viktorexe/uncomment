from .base_parser import BaseParser
from typing import List, Tuple

class RustParser(BaseParser):
    def get_string_patterns(self) -> List[str]:
        return [
            r'"(?:[^"\\]|\\.)*"',  # Double quoted strings
            r"'(?:[^'\\]|\\.)*'",  # Single quoted chars
            r'r#*".*?"#*',         # Raw string literals
            r'b"(?:[^"\\]|\\.)*"', # Byte strings
            r"b'(?:[^'\\]|\\.)*'", # Byte chars
        ]
    
    def get_comment_patterns(self) -> List[str]:
        return [r'//.*$']
    
    def get_multiline_comment_patterns(self) -> List[Tuple[str, str]]:
        return [(r'/\*', r'\*/')]