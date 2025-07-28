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
        """Return regex patterns for string literals"""
        pass
    
    @abstractmethod
    def get_comment_patterns(self) -> List[str]:
        """Return regex patterns for single-line comments"""
        pass
    
    @abstractmethod
    def get_multiline_comment_patterns(self) -> List[Tuple[str, str]]:
        """Return start/end patterns for multi-line comments"""
        pass
    
    def process(self, code: str) -> Dict[str, Any]:
        """Advanced comment removal with string literal preservation"""
        if not code:
            return {'cleaned_code': '', 'comments_removed': 0}
        
        # Initialize patterns
        self.string_patterns = self.get_string_patterns()
        self.comment_patterns = self.get_comment_patterns()
        self.multiline_comment_patterns = self.get_multiline_comment_patterns()
        
        # Track string positions to avoid removing comments inside strings
        string_positions = self._find_string_positions(code)
        
        # Remove multi-line comments first
        code, ml_removed = self._remove_multiline_comments(code, string_positions)
        
        # Update string positions after multiline removal
        string_positions = self._find_string_positions(code)
        
        # Remove single-line comments
        code, sl_removed = self._remove_single_line_comments(code, string_positions)
        
        # Clean up excessive whitespace while preserving intentional formatting
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
        
        # Sort and merge overlapping positions
        positions.sort()
        merged = []
        for start, end in positions:
            if merged and start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))
        
        return merged
    
    def _is_in_string(self, pos: int, string_positions: List[Tuple[int, int]]) -> bool:
        """Check if position is inside a string literal"""
        for start, end in string_positions:
            if start <= pos < end:
                return True
        return False
    
    def _remove_multiline_comments(self, code: str, string_positions: List[Tuple[int, int]]) -> Tuple[str, int]:
        """Remove multi-line comments while preserving strings"""
        removed_count = 0
        
        for start_pattern, end_pattern in self.multiline_comment_patterns:
            while True:
                start_match = re.search(start_pattern, code)
                if not start_match or self._is_in_string(start_match.start(), string_positions):
                    if start_match and self._is_in_string(start_match.start(), string_positions):
                        # Skip this match and look for next
                        temp_code = code[:start_match.start()] + 'X' * len(start_match.group()) + code[start_match.end():]
                        next_match = re.search(start_pattern, temp_code[start_match.end():])
                        if next_match:
                            continue
                    break
                
                end_match = re.search(end_pattern, code[start_match.end():])
                if not end_match:
                    # Unclosed comment, remove to end
                    code = code[:start_match.start()]
                    removed_count += 1
                    break
                
                # Remove the comment block
                comment_start = start_match.start()
                comment_end = start_match.end() + end_match.end()
                
                # Preserve line breaks to maintain line numbers
                comment_text = code[comment_start:comment_end]
                line_breaks = comment_text.count('\n')
                replacement = '\n' * line_breaks
                
                code = code[:comment_start] + replacement + code[comment_end:]
                removed_count += 1
                
                # Update string positions
                string_positions = self._find_string_positions(code)
        
        return code, removed_count
    
    def _remove_single_line_comments(self, code: str, string_positions: List[Tuple[int, int]]) -> Tuple[str, int]:
        """Remove single-line comments while preserving strings"""
        lines = code.split('\n')
        removed_count = 0
        
        for i, line in enumerate(lines):
            for pattern in self.comment_patterns:
                match = re.search(pattern, line)
                if match and not self._is_in_string_line(match.start(), line, string_positions, i, code):
                    lines[i] = line[:match.start()].rstrip()
                    removed_count += 1
                    break
        
        return '\n'.join(lines), removed_count
    
    def _is_in_string_line(self, pos: int, line: str, string_positions: List[Tuple[int, int]], line_num: int, full_code: str) -> bool:
        """Check if position in line is inside a string literal"""
        # Calculate absolute position in full code
        lines_before = full_code.split('\n')[:line_num]
        abs_pos = sum(len(l) + 1 for l in lines_before) + pos
        
        return self._is_in_string(abs_pos, string_positions)
    
    def _clean_whitespace(self, code: str) -> str:
        """Clean excessive whitespace while preserving intentional formatting"""
        lines = code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove trailing whitespace but preserve leading indentation
            cleaned_line = line.rstrip()
            cleaned_lines.append(cleaned_line)
        
        # Remove excessive empty lines (more than 2 consecutive)
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