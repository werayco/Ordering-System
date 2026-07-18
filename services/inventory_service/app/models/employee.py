from typing import Optional
from uuid import UUID
from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7
from services.auth_service.app.db import Base

class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid7)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)