from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List, Optional
import asyncio

from ..schemas.request_model import ProcessRequest, ProcessResponse
from ..services.stripper_service import StripperService
from ..utils.file_handler import FileHandler

router = APIRouter(prefix="/api", tags=["process"])
stripper_service = StripperService()
file_handler = FileHandler()

@router.post("/process", response_model=ProcessResponse)
async def process_code(request: ProcessRequest):
    """Process code and remove comments"""
    try:
        result = await stripper_service.process_code(
            code=request.code,
            language=request.language,
            preserve_structure=request.preserve_structure
        )
        
        return ProcessResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@router.post("/process-file")
async def process_file(file: UploadFile = File(...), language: Optional[str] = None):
    """Process uploaded file and remove comments"""
    try:
        # Read file content
        content = await file.read()
        code = content.decode('utf-8')
        
        # Detect language if not provided
        if not language:
            language = file_handler.detect_language_from_extension(file.filename)
            if language == 'unknown':
                raise HTTPException(status_code=400, detail="Could not detect language from file extension")
        
        # Process code
        result = await stripper_service.process_code(code, language)
        
        return JSONResponse(content={
            "filename": file.filename,
            "language": language,
            **result
        })
        
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be valid UTF-8 text")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process-multiple")
async def process_multiple_files(files: List[UploadFile] = File(...)):
    """Process multiple files concurrently"""
    try:
        # Read all files
        file_contents = {}
        for file in files:
            content = await file.read()
            file_contents[file.filename] = content.decode('utf-8')
        
        # Process all files
        results = await stripper_service.process_multiple_files(file_contents)
        
        return JSONResponse(content=results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/supported-languages")
async def get_supported_languages():
    """Get list of supported programming languages"""
    from ..core import PROCESSORS
    return JSONResponse(content={
        "languages": list(PROCESSORS.keys()),
        "count": len(PROCESSORS)
    })