from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String, func,DateTime,Boolean,Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active = Column(Boolean,default=True)

    # NEW: Relationship to Goals
    goals = relationship("Goal", back_populates="owner")
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    target_date = Column(DateTime(timezone=True), nullable=True)

    # NEW: Foreign key to User
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # NEW: Relationship to User
    owner = relationship("User", back_populates="goals")