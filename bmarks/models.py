from datetime import datetime
from pydantic import BaseModel, Field


class Outline(BaseModel):
    """
    Represents an outline for a bookmark.
    """
    title: str
    category: str = None
    url: str 
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "archive"
