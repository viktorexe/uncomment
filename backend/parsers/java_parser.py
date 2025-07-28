from .base_parser import BaseParser
from typing import List, Tuple
class JavaParser(BaseParser):
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
                    if not in_string and char in ['"', "'"]:
                        in_string = True
                        string_char = char
                    elif in_string and char == string_char:
                        in_string = False
                        string_char = None
                    elif not in_string and line[i:i+2] == '//':
                        # Enhanced URL detection for Java
                        if i >= 4 and line[i-4:i+2] in ['http://', 'tps://']:
                            continue
                        if i > 0 and line[i-1] == ':' and i >= 5 and 'http' in line[i-5:i]:
                            continue
                        line = line[:i].rstrip()
                        comments_removed += 1
                        break
            while '/*' in line and not in_multiline:
                in_string = False
                found_comment = False
                for i in range(len(line) - 1):
                    char = line[i]
                    if char in ['"', "'"] and (i == 0 or line[i-1] != '\\'):
                        in_string = not in_string
                    elif not in_string and line[i:i+2] == '/*':
                        end = line.find('*/', i + 2)
                        if end != -1:
                            line = line[:i] + line[end + 2:]
                            comments_removed += 1
                            found_comment = True
                        else:
                            line = line[:i].rstrip()
                            in_multiline = True
                            comments_removed += 1
                        break
                if not found_comment:
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