import asyncio
from typing import Optional
from core import PROCESSORS
from core.base_processor import BaseProcessor

class StripperService:
    @staticmethod
    async def process_code(code: str, language: str) -> tuple[str, bool]:
        try:
            processor_class = PROCESSORS.get(language.lower())
            if not processor_class:
                return code, False
            
            processor: BaseProcessor = processor_class()
            
            # Process in chunks for large files
            if len(code) > 50000:
                return await StripperService._process_large_code(processor, code)
            
            processed = await asyncio.to_thread(processor.remove_comments, code)
            return processed, True
            
        except Exception as e:
            print(f"Error processing {language}: {e}")
            return code, False
    
    @staticmethod
    async def _process_large_code(processor: BaseProcessor, code: str) -> tuple[str, bool]:
        lines = code.split('\n')
        chunk_size = 1000
        processed_chunks = []
        
        for i in range(0, len(lines), chunk_size):
            chunk = '\n'.join(lines[i:i + chunk_size])
            processed_chunk = await asyncio.to_thread(processor.remove_comments, chunk)
            processed_chunks.append(processed_chunk)
        
        return '\n'.join(processed_chunks), True
    
    @staticmethod
    def get_supported_languages() -> list[str]:
        return list(PROCESSORS.keys())