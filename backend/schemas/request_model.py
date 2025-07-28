from pydantic import BaseModel, Field
from typing import Optional

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