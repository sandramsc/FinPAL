from typing import Any, Literal, Optional
from pydantic import BaseModel


class Message(BaseModel):
    role: Literal["user", "assistant", "system", "tool"]
    content: Optional[str] = None
    photo: Optional[bytes] = None
    tool_calls: list[Any] =None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None