from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import uuid4, UUID


class User(BaseModel):
    username: str
    password: str


class Item(BaseModel):
    item_id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    created_at: datetime = Field(
        default_factory=datetime.now
    )  # Add Timezone if required


class UpdateModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
