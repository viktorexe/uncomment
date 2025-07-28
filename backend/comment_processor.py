import re
from typing import Dict, List, Tuple, Any
from .parsers import *

class CommentProcessor:
    def __init__(self):
        self.parsers = {
            'python': PythonParser(),
            'javascript': JavaScriptParser(),
            'typescript': TypeScriptParser(),
            'java': JavaParser(),
            'cpp': CppParser(),
            'c': CParser(),
            'csharp': CSharpParser(),
            'go': GoParser(),
            'rust': RustParser(),
            'php': PhpParser(),
            'ruby': RubyParser(),
            'swift': SwiftParser(),
            'kotlin': KotlinParser(),
            'scala': ScalaParser(),
            'html': HtmlParser(),
            'css': CssParser(),
            'sql': SqlParser()
        }
    
    def remove_comments(self, code: str, language: str) -> Dict[str, Any]:
        """Advanced comment removal with preservation of string literals and edge cases"""
        if not code or not language:
            return {'code': code, 'stats': {'removed': 0, 'lines_processed': 0}}
        
        language = language.lower()
        parser = self.parsers.get(language)
        
        if not parser:
            return {'code': code, 'stats': {'removed': 0, 'lines_processed': len(code.split('\n'))}}
        
        # Process with advanced parsing
        result = parser.process(code)
        
        return {
            'code': result['cleaned_code'],
            'stats': {
                'removed': result['comments_removed'],
                'lines_processed': len(code.split('\n')),
                'original_size': len(code),
                'cleaned_size': len(result['cleaned_code']),
                'compression_ratio': round((1 - len(result['cleaned_code']) / len(code)) * 100, 2) if code else 0
            }
        }
    
    def get_supported_languages(self) -> List[str]:
        return list(self.parsers.keys())