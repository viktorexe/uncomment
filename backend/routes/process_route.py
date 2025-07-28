from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from schemas.request_model import ProcessRequest, ProcessResponse
from services.stripper_service import StripperService
from utils.file_handler import FileHandler
import io

router = APIRouter()

@router.post("/process", response_model=ProcessResponse)
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
            original_lines=FileHandler.count_lines(request.code),
            processed_lines=FileHandler.count_lines(processed_code),
            language=request.language,
            success=True
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process-file")
async def process_file(file: UploadFile = File(...), language: str = None):
    try:
        content = await file.read()
        code = content.decode('utf-8')
        
        if not language:
            language = FileHandler.detect_language_from_extension(file.filename)
        
        processed_code, success = await StripperService.process_code(code, language)
        
        if not success:
            raise HTTPException(status_code=400, detail="Processing failed")
        
        # Return processed file
        processed_filename = f"processed_{file.filename}"
        return StreamingResponse(
            io.BytesIO(processed_code.encode('utf-8')),
            media_type='application/octet-stream',
            headers={"Content-Disposition": f"attachment; filename={processed_filename}"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/languages")
async def get_supported_languages():
    return {"languages": StripperService.get_supported_languages()}