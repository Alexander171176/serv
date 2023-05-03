import uuid

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.model.base_model import BaseModel


class User(SQLAlchemyBaseUserTableUUID, BaseModel):
    __tablename__ = "user"

    # Столбцы таблицы "user"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Внешний ключ на таблицу "roles"
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    role = relationship("Role", backref="user")
