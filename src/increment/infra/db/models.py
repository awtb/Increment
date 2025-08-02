from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    """Base for all models"""


class Increment(BaseModel):
    """User's model"""

    __tablename__ = "increment"

    count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        primary_key=True,
    )
