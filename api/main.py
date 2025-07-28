from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Tuple
from abc import ABC, abstractmethod
import asyncio
import io
import re

# Inline all dependencies for Vercel
class ProcessRequest(BaseModel):
    code: str = Field(..., description="Source code to process")
    language: str = Field(..., description="Programming language")
    preserve_structure: Optional[bool] = Field(default=True, description="Preserve code structure")

class ProcessResponse(BaseModel):
    processed_code: str
    original_lines: int
    processed_lines: int
    language: str
    success: bool

class BaseProcessor(ABC):
    def __init__(self):
        self.single_line_patterns = []
        self.multi_line_patterns = []
        self.string_delimiters = []
    
    @abstractmethod
    def get_comment_patterns(self) -> Tuple[List[str], List[Tuple[str, str]]]:
        pass
    
    def remove_comments(self, code: str) -> str:
        single_patterns, multi_patterns = self.get_comment_patterns()
        
        for start, end in multi_patterns:
            code = self._remove_multiline_comments(code, start, end)
        
        for pattern in single_patterns:
            code = self._remove_single_line_comments(code, pattern)
        
        return self._clean_empty_lines(code)
    
    def _remove_multiline_comments(self, code: str, start: str, end: str) -> str:
        result = []
        i = 0
        in_string = False
        string_char = None
        
        while i < len(code):
            if not in_string:
                if code[i:i+len(start)] == start:
                    j = i + len(start)
                    while j < len(code) - len(end) + 1:
                        if code[j:j+len(end)] == end:
                            i = j + len(end)
                            break
                        j += 1
                    else:
                        break
                    continue
                elif code[i] in ['"', "'", '`']:
                    in_string = True
                    string_char = code[i]
            else:
                if code[i] == string_char and (i == 0 or code[i-1] != '\\'):
                    in_string = False
                    string_char = None
            
            result.append(code[i])
            i += 1
        
        return ''.join(result)
    
    def _remove_single_line_comments(self, code: str, pattern: str) -> str:
        lines = code.split('\n')
        result = []
        
        for line in lines:
            in_string = False
            string_char = None
            i = 0
            
            while i < len(line):
                if not in_string:
                    if line[i:i+len(pattern)] == pattern:
                        line = line[:i].rstrip()
                        break
                    elif line[i] in ['"', "'", '`']:
                        in_string = True
                        string_char = line[i]
                else:
                    if line[i] == string_char and (i == 0 or line[i-1] != '\\'):
                        in_string = False
                        string_char = None
                i += 1
            
            result.append(line)
        
        return '\n'.join(result)
    
    def _clean_empty_lines(self, code: str) -> str:
        lines = code.split('\n')
        result = []
        
        for line in lines:
            if line.strip():
                result.append(line)
            elif result and result[-1].strip():
                result.append('')
        
        return '\n'.join(result).strip()

class PythonProcessor(BaseProcessor):
    def get_comment_patterns(self) -> Tuple[List[str], List[Tuple[str, str]]]:
        return ['#'], [('"""', '"""'), ("'''", "'''")]

class JavaScriptProcessor(BaseProcessor):
    def get_comment_patterns(self) -> Tuple[List[str], List[Tuple[str, str]]]:
        return ['//'], [('/*', '*/')]

class JavaProcessor(BaseProcessor):
    def get_comment_patterns(self) -> Tuple[List[str], List[Tuple[str, str]]]:
        return ['//'], [('/*', '*/')]

class CppProcessor(BaseProcessor):
    def get_comment_patterns(self) -> Tuple[List[str], List[Tuple[str, str]]]:
        return ['//'], [('/*', '*/')]

class CProcessor(BaseProcessor):
    def get_comment_patterns(self) -> Tuple[List[str], List[Tuple[str, str]]]:
        return ['//'], [('/*', '*/')]

class GoProcessor(BaseProcessor):
    def get_comment_patterns(self) -> Tuple[List[str], List[Tuple[str, str]]]:
        return ['//'], [('/*', '*/')]

class PhpProcessor(BaseProcessor):
    def get_comment_patterns(self) -> Tuple[List[str], List[Tuple[str, str]]]:
        return ['//', '#'], [('/*', '*/')]

class RustProcessor(BaseProcessor):
    def get_comment_patterns(self) -> Tuple[List[str], List[Tuple[str, str]]]:
        return ['//'], [('/*', '*/')]

class RubyProcessor(BaseProcessor):
    def get_comment_patterns(self) -> Tuple[List[str], List[Tuple[str, str]]]:
        return ['#'], [('=begin', '=end')]

class TypeScriptProcessor(BaseProcessor):
    def get_comment_patterns(self) -> Tuple[List[str], List[Tuple[str, str]]]:
        return ['//'], [('/*', '*/')]

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

class StripperService:
    @staticmethod
    async def process_code(code: str, language: str) -> tuple[str, bool]:
        try:
            processor_class = PROCESSORS.get(language.lower())
            if not processor_class:
                return code, False
            
            processor: BaseProcessor = processor_class()
            processed = await asyncio.to_thread(processor.remove_comments, code)
            return processed, True
            
        except Exception as e:
            return code, False
    
    @staticmethod
    def get_supported_languages() -> list[str]:
        return list(PROCESSORS.keys())

def count_lines(code: str) -> int:
    return len([line for line in code.split('\n') if line.strip()])

app = FastAPI(
    title="Advanced Comment Remover API",
    description="Production-grade comment removal for 10+ programming languages",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/process", response_model=ProcessResponse)
async def process_code(request: ProcessRequest):
    try:
        processed_code, success = await StripperService.process_code(
            request.code, 
            request.language
        )
        
        if not success:
            raise HTTPException(status_code=400, detail="Unsupported language or processing error")
        
        return ProcessResponse(
            processed_code=processed_code,
            original_lines=count_lines(request.code),
            processed_lines=count_lines(processed_code),
            language=request.language,
            success=True
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/languages")
async def get_supported_languages():
    return {"languages": StripperService.get_supported_languages()}