from uuid import UUID, uuid7

from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.postgres_files.base_class import Base
from src.postgres_files.permission_level import PermissionLevel


class UsersTable(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False, default=uuid7)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    deployment_id: Mapped[str] = mapped_column(ForeignKey("deployments.id"), nullable=False)
    permission_level: Mapped[PermissionLevel] = mapped_column(Enum(PermissionLevel), nullable=False)
