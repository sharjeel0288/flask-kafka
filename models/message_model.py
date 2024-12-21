from pydantic import BaseModel
from typing import Optional

class MessageModel(BaseModel):
    """Message model to structure the Kafka message response."""
    value: str
    topic: str
    partition: int
    offset: int
    timestamp: Optional[str] = None

    class Config:
        """Pydantic config for data validation."""
        orm_mode = True
