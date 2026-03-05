import datetime
from uuid import UUID, uuid7

from sqlalchemy import String, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.postgres_files.base_class import Base
from src.postgres_files.status_type import StatusType


class DeploymentTable(Base):
    __tablename__ = "deployments"
    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False, default=uuid7)
    db_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[StatusType] = mapped_column(Enum(StatusType), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    creation_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
