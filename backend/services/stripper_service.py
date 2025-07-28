import asyncio
import time
from typing import Dict, Any
from ..core import get_processor
from ..utils.file_handler import FileHandler

class StripperService:
    """Main service for orchestrating comment removal"""
    
    def __init__(self):
        self.file_handler = FileHandler()
    
    async def process_code(self, code: str, language: str, preserve_structure: bool = True) -> Dict[str, Any]:
        """Process code and remove comments"""
        start_time = time.time()
        
        try:
            # Get appropriate processor
            processor = get_processor(language)
            
            # Count original lines
            original_lines = len(code.split('\n'))
            
            # Process code
            if len(code) > 100000:  # Large file handling
                cleaned_code = await self._process_large_code(code, processor)
            else:
                cleaned_code = processor.remove_comments(code)
            
            # Post-process if structure preservation is needed
            if preserve_structure:
                cleaned_code = self._preserve_structure(code, cleaned_code)
            
            # Count cleaned lines
            cleaned_lines = len(cleaned_code.split('\n'))
            
            processing_time = time.time() - start_time
            
            return {
                'cleaned_code': cleaned_code,
                'original_lines': original_lines,
                'cleaned_lines': cleaned_lines,
                'language': language,
                'processing_time': processing_time
            }
            
        except Exception as e:
            raise Exception(f"Processing failed: {str(e)}")
    
    async def _process_large_code(self, code: str, processor) -> str:
        """Process large code files with chunking"""
        # For very large files, we might need to process in chunks
        # but maintain context for comment boundaries
        return await asyncio.get_event_loop().run_in_executor(
            None, processor.remove_comments, code
        )
    
    def _preserve_structure(self, original: str, cleaned: str) -> str:
        """Preserve original structure by maintaining empty lines"""
        original_lines = original.split('\n')
        cleaned_lines = cleaned.split('\n')
        
        # Simple structure preservation - maintain empty lines
        result = []
        cleaned_idx = 0
        
        for orig_line in original_lines:
            if orig_line.strip() == '':
                result.append('')
            elif cleaned_idx < len(cleaned_lines):
                result.append(cleaned_lines[cleaned_idx])
                cleaned_idx += 1
            else:
                result.append('')
        
        return '\n'.join(result)
    
    async def process_multiple_files(self, files: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
        """Process multiple files concurrently"""
        tasks = []
        
        for filename, content in files.items():
            language = self.file_handler.detect_language_from_extension(filename)
            if language != 'unknown':
                task = self.process_code(content, language)
                tasks.append((filename, task))
        
        results = {}
        for filename, task in tasks:
            try:
                results[filename] = await task
            except Exception as e:
                results[filename] = {'error': str(e)}
        
        return results