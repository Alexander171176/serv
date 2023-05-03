import datetime
from sqlalchemy import Column, DateTime
from app.model.base import Base


class BaseModel(Base):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
