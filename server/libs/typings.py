from typing import Literal, Optional
from pydantic import BaseModel


class Message(BaseModel):
    role: Literal["user", "assistant","system"]
    content: Optional[str] = None
    file: Optional[bytes] = None