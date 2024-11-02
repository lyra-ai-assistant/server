from pydantic import BaseModel
from typing import Optional


class TextRequest(BaseModel):
    text: str
    context: Optional[str] = None
