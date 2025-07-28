from .base_parser import BaseParser
from typing import List, Tuple

class PhpParser(BaseParser):
    def get_string_patterns(self) -> List[str]:
        return [
            r'"(?:[^"\\]|\\.)*"',  # Double quoted strings
            r"'(?:[^'\\]|\\.)*'",  # Single quoted strings
            r'<<<["\']?(\w+)["\']?.*?\n\1;', # Heredoc/Nowdoc
        ]
    
    def get_comment_patterns(self) -> List[str]:
        return [r'//.*$', r'#.*$']
    
    def get_multiline_comment_patterns(self) -> List[Tuple[str, str]]:
        return [(r'/\*', r'\*/')]