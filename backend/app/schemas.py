from pydantic import BaseModel
from typing import List, Optional, Literal

class ValidationError(BaseModel):
    row_index: Optional[int] = None
    id: Optional[int] = None
    column: Optional[str] = None
    error_message: str

class ValidationResponse(BaseModel):
    status: Literal["pass", "fail"]
    errors: List[ValidationError]
