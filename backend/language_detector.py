import re
from typing import Dict, List
class LanguageDetector:
    def __init__(self):
        self.patterns = {
            'python': [
                r'def\s+\w+\s*\(',
                r'import\s+\w+',
                r'from\s+\w+\s+import',
                r'if\s+__name__\s*==\s*["\']__main__["\']',
                r'#.*',
                r'""".*?"""',
                r"'''.*?'''"
            ],
            'javascript': [
                r'function\s+\w+\s*\(',
                r'var\s+\w+\s*=',
                r'let\s+\w+\s*=',
                r'const\s+\w+\s*=',
                r'//.*',
                r'/\*.*?\*/',
                r'console\.log\s*\(',
                r'document\.\w+'
            ],
            'typescript': [
                r'interface\s+\w+',
                r'type\s+\w+\s*=',
                r':\s*(string|number|boolean)',
                r'export\s+(interface|type|class)',
                r'//.*',
                r'/\*.*?\*/'
            ],
            'java': [
                r'public\s+class\s+\w+',
                r'public\s+static\s+void\s+main',
                r'import\s+[\w.]+;',
                r'//.*',
                r'/\*.*?\*/',
                r'System\.out\.print'
            ],
            'cpp': [
                r'#include\s*<[\w.]+>',
                r'using\s+namespace\s+std',
                r'int\s+main\s*\(',
                r'std::\w+',
                r'//.*',
                r'/\*.*?\*/'
            ],
            'c': [
                r'#include\s*<[\w.]+\.h>',
                r'int\s+main\s*\(',
                r'printf\s*\(',
                r'//.*',
                r'/\*.*?\*/'
            ],
            'csharp': [
                r'using\s+System',
                r'namespace\s+\w+',
                r'public\s+class\s+\w+',
                r'Console\.WriteLine',
                r'//.*',
                r'/\*.*?\*/'
            ],
            'go': [
                r'package\s+\w+',
                r'import\s+\(',
                r'func\s+\w+\s*\(',
                r'fmt\.Print',
                r'//.*',
                r'/\*.*?\*/'
            ],
            'rust': [
                r'fn\s+\w+\s*\(',
                r'let\s+\w+\s*=',
                r'use\s+\w+',
                r'println!\s*\(',
                r'//.*',
                r'/\*.*?\*/'
            ],
            'php': [
                r'<\?php',
                r'\$\w+\s*=',
                r'function\s+\w+\s*\(',
                r'echo\s+',
                r'//.*',
                r'/\*.*?\*/',
                r'#.*'
            ],
            'ruby': [
                r'def\s+\w+',
                r'class\s+\w+',
                r'require\s+',
                r'puts\s+',
                r'#.*'
            ],
            'swift': [
                r'import\s+\w+',
                r'func\s+\w+\s*\(',
                r'var\s+\w+\s*=',
                r'let\s+\w+\s*=',
                r'print\s*\(',
                r'//.*',
                r'/\*.*?\*/'
            ],
            'html': [
                r'<!DOCTYPE\s+html>',
                r'<html.*?>',
                r'<head.*?>',
                r'<body.*?>',
                r'<!--.*?-->'
            ],
            'css': [
                r'\w+\s*\{',
                r'[\w-]+\s*:\s*[\w\s#.-]+;',
                r'/\*.*?\*/'
            ],
            'sql': [
                r'SELECT\s+',
                r'FROM\s+\w+',
                r'WHERE\s+',
                r'INSERT\s+INTO',
                r'--.*',
                r'/\*.*?\*/'
            ]
        }
    def detect(self, code: str) -> str:
        """Advanced language detection using pattern matching"""
        if not code:
            return 'unknown'
        scores = {}
        code_lower = code.lower()
        for language, patterns in self.patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, code, re.MULTILINE | re.DOTALL | re.IGNORECASE))
                score += matches
            scores[language] = score / len(patterns) if patterns else 0
        if scores:
            detected = max(scores, key=scores.get)
            return detected if scores[detected] > 0 else 'unknown' 
        return 'unknown'