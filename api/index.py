from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
import time

app = FastAPI(title="Uncomment API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProcessRequest(BaseModel):
    code: str
    language: str
    preserve_structure: bool = True

class BaseProcessor:
    def __init__(self):
        self.single_line_patterns = []
        self.multi_line_patterns = []
        self.string_delimiters = []
    
    def _is_in_string(self, code: str, position: int) -> bool:
        before = code[:position]
        in_string = False
        escape_next = False
        current_delimiter = None
        
        for char in before:
            if escape_next:
                escape_next = False
                continue
            if char == '\\':
                escape_next = True
                continue
            if not in_string:
                if char in self.string_delimiters:
                    in_string = True
                    current_delimiter = char
            else:
                if char == current_delimiter:
                    in_string = False
                    current_delimiter = None
        return in_string
    
    def remove_comments(self, code: str) -> str:
        result = code
        # Remove multi-line comments
        for start_pattern, end_pattern in self.multi_line_patterns:
            while True:
                start_match = re.search(start_pattern, result)
                if not start_match or self._is_in_string(result, start_match.start()):
                    break
                end_match = re.search(end_pattern, result[start_match.end():])
                if not end_match:
                    result = result[:start_match.start()]
                    break
                end_pos = start_match.end() + end_match.end()
                result = result[:start_match.start()] + result[end_pos:]
        
        # Remove single-line comments
        lines = result.split('\n')
        cleaned_lines = []
        for line in lines:
            cleaned_line = line
            for pattern in self.single_line_patterns:
                match = re.search(pattern, line)
                if match and not self._is_in_string(line, match.start()):
                    cleaned_line = line[:match.start()].rstrip()
                    break
            cleaned_lines.append(cleaned_line)
        
        return '\n'.join(cleaned_lines)

class PythonProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.single_line_patterns = [r'#.*$']
        self.string_delimiters = ['"', "'"]

class JavaScriptProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.single_line_patterns = [r'//.*$']
        self.multi_line_patterns = [(r'/\*', r'\*/')]
        self.string_delimiters = ['"', "'", '`']

class CProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.single_line_patterns = [r'//.*$']
        self.multi_line_patterns = [(r'/\*', r'\*/')]
        self.string_delimiters = ['"', "'"]

class JavaProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.single_line_patterns = [r'//.*$']
        self.multi_line_patterns = [(r'/\*\*?', r'\*/')]
        self.string_delimiters = ['"']

PROCESSORS = {
    'python': PythonProcessor,
    'javascript': JavaScriptProcessor,
    'typescript': JavaScriptProcessor,
    'c': CProcessor,
    'cpp': CProcessor,
    'c++': CProcessor,
    'java': JavaProcessor,
    'go': CProcessor,
    'php': CProcessor,
    'rust': CProcessor,
    'ruby': PythonProcessor,
}

@app.post("/api/process")
async def process_code(request: ProcessRequest):
    try:
        start_time = time.time()
        
        language = request.language.lower()
        if language not in PROCESSORS:
            raise HTTPException(status_code=400, detail=f"Unsupported language: {language}")
        
        processor = PROCESSORS[language]()
        original_lines = len(request.code.split('\n'))
        cleaned_code = processor.remove_comments(request.code)
        cleaned_lines = len(cleaned_code.split('\n'))
        processing_time = time.time() - start_time
        
        return {
            "cleaned_code": cleaned_code,
            "original_lines": original_lines,
            "cleaned_lines": cleaned_lines,
            "language": language,
            "processing_time": processing_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/supported-languages")
async def get_supported_languages():
    return {"languages": list(PROCESSORS.keys()), "count": len(PROCESSORS)}

@app.get("/")
async def root():
    return {"message": "Uncomment API", "status": "running"}