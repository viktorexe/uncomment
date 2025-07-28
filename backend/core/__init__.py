from .python_processor import PythonProcessor
from .javascript_processor import JavaScriptProcessor
from .java_processor import JavaProcessor
from .cpp_processor import CppProcessor
from .c_processor import CProcessor
from .go_processor import GoProcessor
from .php_processor import PhpProcessor
from .rust_processor import RustProcessor
from .ruby_processor import RubyProcessor
from .typescript_processor import TypeScriptProcessor

PROCESSORS = {
    'python': PythonProcessor,
    'javascript': JavaScriptProcessor,
    'typescript': TypeScriptProcessor,
    'java': JavaProcessor,
    'cpp': CppProcessor,
    'c': CProcessor,
    'go': GoProcessor,
    'php': PhpProcessor,
    'rust': RustProcessor,
    'ruby': RubyProcessor,
}