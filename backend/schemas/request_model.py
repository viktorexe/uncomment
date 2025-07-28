from pydantic import BaseModel, Field
from typing import Optional

class ProcessRequest(BaseModel):
    code: str = Field(..., description="Source code to process")
    language: str = Field(..., description="Programming language")
    preserve_structure: bool = Field(default=True, description="Preserve code structure")

class ProcessResponse(BaseModel):
    cleaned_code: str = Field(..., description="Code with comments removed")
    original_lines: int = Field(..., description="Original line count")
    cleaned_lines: int = Field(..., description="Cleaned line count")
    language: str = Field(..., description="Processed language")
    processing_time: float = Field(..., description="Processing time in seconds")