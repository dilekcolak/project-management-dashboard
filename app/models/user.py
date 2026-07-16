from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(50),
        unique=False,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(250),
        unique=False,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(250),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    owned_projects = relationship(
        "Project",
        back_populates="owner"
    )

    project_memberships = relationship(
        "ProjectMember",
        back_populates="user"
    )

    uploaded_documents = relationship(
        "Document",
        back_populates="uploader"
    )