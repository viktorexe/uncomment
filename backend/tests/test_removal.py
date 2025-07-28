import pytest
import asyncio
from backend.core import get_processor
from backend.services.stripper_service import StripperService

class TestCommentRemoval:
    """Test suite for comment removal functionality"""
    
    def test_python_comments(self):
        """Test Python comment removal"""
        processor = get_processor('python')
        
        code = '''
def hello():  # This is a comment
    """This is a docstring"""
    print("Hello")  # Another comment
    # Full line comment
    return True
'''
        
        result = processor.remove_comments(code)
        assert '# This is a comment' not in result
        assert '# Another comment' not in result
        assert '# Full line comment' not in result
        assert '"""This is a docstring"""' in result  # Docstrings preserved
    
    def test_javascript_comments(self):
        """Test JavaScript comment removal"""
        processor = get_processor('javascript')
        
        code = '''
function hello() {  // Single line comment
    /* Multi-line
       comment */
    console.log("Hello"); // Another comment
    return true;
}
'''
        
        result = processor.remove_comments(code)
        assert '// Single line comment' not in result
        assert '/* Multi-line' not in result
        assert 'comment */' not in result
        assert '// Another comment' not in result
        assert 'console.log("Hello");' in result
    
    def test_c_comments(self):
        """Test C/C++ comment removal"""
        processor = get_processor('c')
        
        code = '''
#include <stdio.h>  // Include header
/* Main function
   implementation */
int main() {
    printf("Hello"); // Print statement
    return 0;
}
'''
        
        result = processor.remove_comments(code)
        assert '// Include header' not in result
        assert '/* Main function' not in result
        assert '// Print statement' not in result
        assert '#include <stdio.h>' in result  # Preprocessor preserved
    
    def test_java_comments(self):
        """Test Java comment removal"""
        processor = get_processor('java')
        
        code = '''
/**
 * JavaDoc comment
 */
public class Test {  // Class comment
    /* Block comment */
    public void method() {
        System.out.println("Hello"); // Method comment
    }
}
'''
        
        result = processor.remove_comments(code)
        assert '/**' not in result
        assert 'JavaDoc comment' not in result
        assert '// Class comment' not in result
        assert '/* Block comment */' not in result
        assert '// Method comment' not in result
        assert 'System.out.println("Hello");' in result
    
    def test_string_preservation(self):
        """Test that comments in strings are preserved"""
        processor = get_processor('python')
        
        code = '''
text = "This is a // comment in string"
url = "https://example.com"  # Real comment
'''
        
        result = processor.remove_comments(code)
        assert 'This is a // comment in string' in result
        assert '# Real comment' not in result
    
    @pytest.mark.asyncio
    async def test_service_processing(self):
        """Test the stripper service"""
        service = StripperService()
        
        code = '''
def test():  # Comment
    return True
'''
        
        result = await service.process_code(code, 'python')
        
        assert result['language'] == 'python'
        assert result['original_lines'] == 3
        assert '# Comment' not in result['cleaned_code']
        assert 'processing_time' in result
    
    def test_large_file_handling(self):
        """Test handling of large files"""
        processor = get_processor('python')
        
        # Generate large code with comments
        lines = []
        for i in range(1000):
            lines.append(f'def func_{i}():  # Comment {i}')
            lines.append(f'    return {i}')
            lines.append('')
        
        large_code = '\n'.join(lines)
        result = processor.remove_comments(large_code)
        
        # Verify comments are removed but code structure remains
        assert '# Comment' not in result
        assert 'def func_0():' in result
        assert 'return 0' in result
    
    def test_edge_cases(self):
        """Test edge cases and malformed input"""
        processor = get_processor('python')
        
        # Empty string
        assert processor.remove_comments('') == ''
        
        # Only comments
        result = processor.remove_comments('# Just a comment\n# Another comment')
        assert result.strip() == ''
        
        # Mixed line endings
        code = 'print("hello")  # Comment\r\nprint("world")  # Another\n'
        result = processor.remove_comments(code)
        assert '# Comment' not in result
        assert '# Another' not in result
    
    def test_unsupported_language(self):
        """Test handling of unsupported languages"""
        with pytest.raises(ValueError, match="Unsupported language"):
            get_processor('cobol')

if __name__ == '__main__':
    pytest.main([__file__])