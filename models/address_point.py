from typing import Optional
from pydantic import BaseModel


class AddressPoint(BaseModel):
    x: Optional[int]
    y: Optional[int]
