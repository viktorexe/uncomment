from .base_processor import BaseProcessor
from typing import List, Tuple

class RubyProcessor(BaseProcessor):
    def get_comment_patterns(self) -> Tuple[List[str], List[Tuple[str, str]]]:
        single_patterns = ['#']
        multi_patterns = [('=begin', '=end')]
        return single_patterns, multi_patterns