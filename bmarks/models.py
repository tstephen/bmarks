from datetime import UTC, datetime
from pydantic import BaseModel, Field


class Outline(BaseModel):
    """
    Represents an outline for a bookmark.
    """
    title: str
    category: str = None
    url: str 
    created: datetime = Field(default_factory=lambda: datetime.now(UTC))
    status: str = "archive"
