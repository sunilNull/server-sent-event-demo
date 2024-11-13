from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskStatus(BaseModel):
    status: str


class TaskStatusResponse(BaseModel):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    version: int

    class Config:
        from_attributes = True
