from .base_parser import BaseParser
from typing import List, Tuple

class PythonParser(BaseParser):
    def get_string_patterns(self) -> List[str]:
        return [
            r'""".*?"""',  # Triple double quotes
            r"'''.*?'''",  # Triple single quotes
            r'"(?:[^"\\]|\\.)*"',  # Double quoted strings
            r"'(?:[^'\\]|\\.)*'",  # Single quoted strings
            r'r"(?:[^"\\]|\\.)*"',  # Raw double quoted
            r"r'(?:[^'\\]|\\.)*'",  # Raw single quoted
            r'f"(?:[^"\\]|\\.)*"',  # F-string double
            r"f'(?:[^'\\]|\\.)*'",  # F-string single
        ]
    
    def get_comment_patterns(self) -> List[str]:
        return [r'#.*$']
    
    def get_multiline_comment_patterns(self) -> List[Tuple[str, str]]:
        return [
            (r'"""', r'"""'),
            (r"'''", r"'''")
        ]