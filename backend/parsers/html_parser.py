from .base_parser import BaseParser
from typing import List, Tuple

class HtmlParser(BaseParser):
    def get_string_patterns(self) -> List[str]:
        return [
            r'"[^"]*"',  # Double quoted attributes
            r"'[^']*'",  # Single quoted attributes
        ]
    
    def get_comment_patterns(self) -> List[str]:
        return []
    
    def get_multiline_comment_patterns(self) -> List[Tuple[str, str]]:
        return [(r'<!--', r'-->')]