from .base_parser import BaseParser
from typing import List, Tuple

class CSharpParser(BaseParser):
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
                verbatim = False

                i = 0
                while i < len(line):
                    char = line[i]

                    if not in_string and char == '@' and i + 1 < len(line) and line[i + 1] == '"':
                        verbatim = True
                        in_string = True
                        string_char = '"'
                        i += 2
                        continue
                    elif not in_string and char in ['"', "'"]:
                        in_string = True
                        string_char = char
                    elif in_string and char == string_char:
                        if verbatim and i + 1 < len(line) and line[i + 1] == '"':
                            i += 1  
                        else:
                            in_string = False
                            string_char = None
                            verbatim = False
                    elif not in_string and line[i:i+2] == '//':
                        if i > 0 and line[i-1] == ':':
                            i += 1
                            continue
                        line = line[:i].rstrip()
                        comments_removed += 1
                        break

                    i += 1

            if '/*' in line and not in_multiline:
                in_string = False
                for i in range(len(line) - 1):
                    char = line[i]
                    if char in ['"', "'"] and (i == 0 or line[i-1] != '\\'):
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