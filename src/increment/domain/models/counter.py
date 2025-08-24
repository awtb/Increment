from pydantic import BaseModel, Field


class Counter(BaseModel):
    count: int = Field(description="Count of increments")
