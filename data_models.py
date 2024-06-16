from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class User(BaseModel):
    username: str
    password: str


class Item(BaseModel):
    item_id: int = None
    name: str
    description: str
    created_at: datetime = None


class UpdateModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
