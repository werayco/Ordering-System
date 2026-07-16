from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlalchemy import String, Uuid, Integer, Numeric, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7
from src.db.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid7)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)