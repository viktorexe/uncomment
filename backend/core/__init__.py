from .python_processor import PythonProcessor
from .javascript_processor import JavaScriptProcessor
from .c_processor import CProcessor, CppProcessor
from .java_processor import JavaProcessor
from .go_processor import GoProcessor
from .php_processor import PhpProcessor
from .rust_processor import RustProcessor
from .ruby_processor import RubyProcessor

PROCESSORS = {
    'python': PythonProcessor,
    'javascript': JavaScriptProcessor,
    'typescript': JavaScriptProcessor,
    'c': CProcessor,
    'cpp': CppProcessor,
    'c++': CppProcessor,
    'java': JavaProcessor,
    'go': GoProcessor,
    'php': PhpProcessor,
    'rust': RustProcessor,
    'ruby': RubyProcessor,
}

def get_processor(language: str):
    """Get processor for specified language"""
    language = language.lower()
    if language in PROCESSORS:
        return PROCESSORS[language]()
    raise ValueError(f"Unsupported language: {language}")