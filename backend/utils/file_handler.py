import io
import zipfile
from typing import Dict, List

class FileHandler:
    @staticmethod
    def create_zip_response(files: Dict[str, str]) -> bytes:
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for filename, content in files.items():
                zip_file.writestr(filename, content)
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    
    @staticmethod
    def detect_language_from_extension(filename: str) -> str:
        extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.cc': 'cpp',
            '.cxx': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.php': 'php',
            '.rs': 'rust',
            '.rb': 'ruby',
        }
        
        ext = filename.lower().split('.')[-1]
        return extensions.get(f'.{ext}', 'javascript')
    
    @staticmethod
    def count_lines(code: str) -> int:
        return len([line for line in code.split('\n') if line.strip()])