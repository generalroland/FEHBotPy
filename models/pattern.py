from typing import Optional, Any
from pydantic import BaseModel


class Pattern(BaseModel):
    name: Optional[str]
    type: Optional[str]
    img: Any
