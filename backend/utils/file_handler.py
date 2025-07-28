import aiofiles
import asyncio
from typing import AsyncGenerator
import os

class FileHandler:
    """Async file handling for large files"""
    
    @staticmethod
    async def read_file_chunks(file_path: str, chunk_size: int = 8192) -> AsyncGenerator[str, None]:
        """Read file in chunks for memory efficiency"""
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    
    @staticmethod
    async def write_file_async(file_path: str, content: str) -> None:
        """Write file asynchronously"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as file:
            await file.write(content)
    
    @staticmethod
    def detect_language_from_extension(filename: str) -> str:
        """Detect programming language from file extension"""
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.c': 'c',
            '.cpp': 'cpp',
            '.cc': 'cpp',
            '.cxx': 'cpp',
            '.go': 'go',
            '.php': 'php',
            '.rs': 'rust',
            '.rb': 'ruby',
        }
        
        ext = os.path.splitext(filename)[1].lower()
        return ext_map.get(ext, 'unknown')
    
    @staticmethod
    async def process_large_file(file_path: str, processor, chunk_size: int = 1024*1024) -> str:
        """Process large files in chunks to avoid memory issues"""
        chunks = []
        async for chunk in FileHandler.read_file_chunks(file_path, chunk_size):
            chunks.append(chunk)
        
        full_content = ''.join(chunks)
        return processor.remove_comments(full_content)