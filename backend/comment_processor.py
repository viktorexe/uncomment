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
        """Advanced comment removal"""
        if not code or not language:
            return {'code': code, 'stats': {'removed': 0}}
        language = language.lower()
        parser = self.parsers.get(language)
        if not parser:
            return {'code': code, 'stats': {'removed': 0}}
        result = parser.process(code)
        return {
            'code': result['cleaned_code'],
            'stats': {
                'removed': result['comments_removed']
            }
        }
    def get_supported_languages(self) -> List[str]:
        return list(self.parsers.keys())