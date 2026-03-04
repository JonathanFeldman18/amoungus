import datetime
from enum import Enum
import sqlalchemy as alc
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Session

class StatusType(Enum):
    CREATED = 1
    DELETED = 2

class Base(DeclarativeBase):
    pass

class Deployment(Base):
    __tablename__ = "deployments"
    id: Mapped[str] = mapped_column(primary_key=True)
    db_name: Mapped[str] = mapped_column(String(255))
    status: Mapped[Optional[StatusType]]
    username: Mapped[str] = mapped_column(String(255))
    creation_time: Mapped[datetime.datetime] = mapped_column()

    def __repr__(self) -> str:
        return (f"deployments(id={self.id!r}, db_name={self.db_name!r}, status={self.status!r},"
                f" username={self.username!r}, creation_time={self.creation_time!r})")

class PostgresConnection:
    def __init__(self):
        self.engine = alc.create_engine("postgresql://{}:{}@{}/{}".format("postgres", "postgres", "postgres:5432", "postgres"))
        """self.deployments = alc.Table(
            'deployments',
            self.metadata,
            alc.Column('id', alc.String, primary_key=True),
            alc.Column('db_name', alc.VARCHAR(255)),
            alc.Column('status', alc.Integer),
            alc.Column('username', alc.VARCHAR(255)),
            alc.Column('creation_time', alc.TIMESTAMP),
        )"""
        self.metadata = Base.metadata
        self.metadata.create_all(self.engine)

    def create_new_deployment(self):
        with Session(self.engine) as session:
            spongebob = Deployment(
                db_name="spongebob",
                status="CREATED",
                username="Spongebob Squarepants",
                creation_time=datetime.datetime.now()
            )
            session.add(spongebob)
            session.commit()

        """session = Session(self.engine)

        stmt = alc.select(Deployment).where(Deployment.db_name.in_(["spongebob"]))

        for user in session.scalars(stmt):
            print(user)"""
