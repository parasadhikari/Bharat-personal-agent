from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    user_id: str = "demo_user"


class PermissionRequest(BaseModel):
    permission_id: str
    allowed: bool


class ChatResponse(BaseModel):
    message: str
    intent: Optional[str] = None
    permission_required: bool = False
    permission_id: Optional[str] = None
    activity: list = []