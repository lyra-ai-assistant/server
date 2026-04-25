from pydantic import BaseModel
from typing import Optional


class TextRequest(BaseModel):
    text: str
    context: Optional[str] = None


class ChatRequest(BaseModel):
    text: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


class StreamRequest(BaseModel):
    text: str
    session_id: Optional[str] = None
