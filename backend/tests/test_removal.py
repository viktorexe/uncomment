import pytest
from core.python_processor import PythonProcessor
from core.javascript_processor import JavaScriptProcessor
from services.stripper_service import StripperService

class TestCommentRemoval:
    def test_python_single_line_comments(self):
        processor = PythonProcessor()
        code = """
def hello():  # This is a comment
    print("Hello")  # Another comment
    return True
"""
        result = processor.remove_comments(code)
        assert "# This is a comment" not in result
        assert "# Another comment" not in result
        assert 'print("Hello")' in result

    def test_python_docstrings(self):
        processor = PythonProcessor()
        code = '''
def hello():
    """This is a docstring"""
    print("Hello")
    return True
'''
        result = processor.remove_comments(code)
        assert '"""This is a docstring"""' not in result
        assert 'print("Hello")' in result

    def test_javascript_comments(self):
        processor = JavaScriptProcessor()
        code = """
function hello() {  // Single line comment
    /* Multi-line
       comment */
    console.log("Hello");
    return true;
}
"""
        result = processor.remove_comments(code)
        assert "// Single line comment" not in result
        assert "/* Multi-line" not in result
        assert 'console.log("Hello");' in result

    @pytest.mark.asyncio
    async def test_service_processing(self):
        code = "def test(): # comment\n    pass"
        result, success = await StripperService.process_code(code, "python")
        assert success
        assert "# comment" not in result
        assert "def test():" in result