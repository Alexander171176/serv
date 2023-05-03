from sqlalchemy import Column, Integer, String, JSON
from app.model.base_model import BaseModel


class Role(BaseModel):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_role = Column(String, nullable=False, unique=True)
    description = Column(String, default="")
    permissions = Column(JSON, default=lambda: [])
