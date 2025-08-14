from pydantic import BaseModel, Field


class IncrementsCount(BaseModel):
    count: int = Field(description="Count of increments")
