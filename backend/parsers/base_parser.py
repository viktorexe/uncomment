import re
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any
class BaseParser(ABC):
    def __init__(self):
        self.string_patterns = []
        self.comment_patterns = []
        self.multiline_comment_patterns = []
    @abstractmethod
    def get_string_patterns(self) -> List[str]:
        pass
    @abstractmethod
    def get_comment_patterns(self) -> List[str]:
        pass
    @abstractmethod
    def get_multiline_comment_patterns(self) -> List[Tuple[str, str]]:
        pass
    def process(self, code: str) -> Dict[str, Any]:
        if not code:
            return {'cleaned_code': '', 'comments_removed': 0}
        self.string_patterns = self.get_string_patterns()
        self.comment_patterns = self.get_comment_patterns()
        self.multiline_comment_patterns = self.get_multiline_comment_patterns()
        string_positions = self._find_string_positions(code)
        code, ml_removed = self._remove_multiline_comments(code, string_positions)
        string_positions = self._find_string_positions(code)
        code, sl_removed = self._remove_single_line_comments(code, string_positions)
        code = self._clean_whitespace(code) 
        return {
            'cleaned_code': code,
            'comments_removed': ml_removed + sl_removed
        }
    def _find_string_positions(self, code: str) -> List[Tuple[int, int]]:
        """Find all string literal positions to avoid processing comments inside them"""
        positions = []
        for pattern in self.string_patterns:
            for match in re.finditer(pattern, code, re.DOTALL):
                positions.append((match.start(), match.end()))
        positions.sort()
        merged = []
        for start, end in positions:
            if merged and start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))
        return merged
    def _is_in_string(self, pos: int, string_positions: List[Tuple[int, int]]) -> bool:
        for start, end in string_positions:
            if start <= pos < end:
                return True
        return False
    def _remove_multiline_comments(self, code: str, string_positions: List[Tuple[int, int]]) -> Tuple[str, int]:
        removed_count = 0
        for start_pattern, end_pattern in self.multiline_comment_patterns:
            while True:
                start_match = re.search(start_pattern, code)
                if not start_match or self._is_in_string(start_match.start(), string_positions):
                    if start_match and self._is_in_string(start_match.start(), string_positions):
                        temp_code = code[:start_match.start()] + 'X' * len(start_match.group()) + code[start_match.end():]
                        next_match = re.search(start_pattern, temp_code[start_match.end():])
                        if next_match:
                            continue
                    break
                end_match = re.search(end_pattern, code[start_match.end():])
                if not end_match:
                    code = code[:start_match.start()]
                    removed_count += 1
                    break
                comment_start = start_match.start()
                comment_end = start_match.end() + end_match.end()
                comment_text = code[comment_start:comment_end]
                line_breaks = comment_text.count('\n')
                replacement = '\n' * line_breaks
                code = code[:comment_start] + replacement + code[comment_end:]
                removed_count += 1
                string_positions = self._find_string_positions(code)
        return code, removed_count
    def _remove_single_line_comments(self, code: str, string_positions: List[Tuple[int, int]]) -> Tuple[str, int]:
        lines = code.split('\n')
        removed_count = 0
        for i, line in enumerate(lines):
            for pattern in self.comment_patterns:
                for match in re.finditer(pattern, line):
                    if not self._is_in_string_line(match.start(), line, string_positions, i, code):
                        lines[i] = line[:match.start()].rstrip()
                        removed_count += 1
                        break
                if removed_count > len(lines) - len([l for l in lines if l.strip()]):
                    break
        return '\n'.join(lines), removed_count
    def _is_in_string_line(self, pos: int, line: str, string_positions: List[Tuple[int, int]], line_num: int, full_code: str) -> bool:
        lines_before = full_code.split('\n')[:line_num]
        abs_pos = sum(len(l) + 1 for l in lines_before) + pos
        return self._is_in_string(abs_pos, string_positions)
    def _clean_whitespace(self, code: str) -> str:
        lines = code.split('\n')
        cleaned_lines = []
        for line in lines:

            cleaned_line = line.rstrip()
            cleaned_lines.append(cleaned_line)
        result_lines = []
        empty_count = 0
        for line in cleaned_lines:
            if line.strip() == '':
                empty_count += 1
                if empty_count <= 2:
                    result_lines.append(line)
            else:
                empty_count = 0
                result_lines.append(line)
        return '\n'.join(result_lines)