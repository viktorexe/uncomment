from .base_parser import BaseParser
from typing import List, Tuple

class JavaScriptParser(BaseParser):
    def process(self, code: str):
        if not code:
            return {'cleaned_code': '', 'comments_removed': 0}
        
        lines = code.split('\n')
        cleaned_lines = []
        comments_removed = 0
        in_multiline = False
        
        for line in lines:
            if in_multiline:
                if '*/' in line:
                    pos = line.find('*/')
                    line = line[pos + 2:]
                    in_multiline = False
                    comments_removed += 1
                else:
                    cleaned_lines.append('')
                    continue
            
            # Remove single line comments with error handling
            if '//' in line:
                in_string = False
                string_char = None
                escape_next = False
                
                for i, char in enumerate(line):
                    if escape_next:
                        escape_next = False
                        continue
                    
                    if char == '\\' and in_string:
                        escape_next = True
                        continue
                    
                    if not in_string and char in ['"', "'", '`']:
                        in_string = True
                        string_char = char
                    elif in_string and char == string_char:
                        in_string = False
                        string_char = None
                    elif not in_string and line[i:i+2] == '//':
                        # Check if it's a URL or protocol
                        if i > 0 and line[i-1] == ':':
                            continue
                        # Check if it's in a regex or similar
                        if i > 0 and line[i-1] in ['=', '(', '[', '{', ',', ' ']:
                            line = line[:i].rstrip()
                            comments_removed += 1
                            break
                        elif i == 0:
                            line = line[:i].rstrip()
                            comments_removed += 1
                            break
            
            # Handle multiline comments with error handling
            if '/*' in line and not in_multiline:
                in_string = False
                for i in range(len(line) - 1):
                    char = line[i]
                    if char in ['"', "'", '`'] and (i == 0 or line[i-1] != '\\'):
                        in_string = not in_string
                    elif not in_string and line[i:i+2] == '/*':
                        end = line.find('*/', i + 2)
                        if end != -1:
                            line = line[:i] + line[end + 2:]
                            comments_removed += 1
                        else:
                            line = line[:i].rstrip()
                            in_multiline = True
                            comments_removed += 1
                        break
            
            cleaned_lines.append(line)
        
        return {
            'cleaned_code': '\n'.join(cleaned_lines),
            'comments_removed': comments_removed
        }
    
    def get_string_patterns(self) -> List[str]:
        return []
    
    def get_comment_patterns(self) -> List[str]:
        return []
    
    def get_multiline_comment_patterns(self) -> List[Tuple[str, str]]:
        return []