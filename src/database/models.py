from sqlalchemy import Column, String, LargeBinary, Table, ForeignKey, JSON, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from uuid import uuid4

from src.database import Base, engine


class UserTable(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    public_id = Column(String, default=uuid4)

    password_rel = relationship("PasswordsTable", back_populates="user", uselist=False)
    projects = relationship('ProjectsTable', back_populates='user', uselist=True)


class PasswordsTable(Base):
    __tablename__ = 'passwords'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    password = Column(LargeBinary, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    user = relationship("UserTable", back_populates="password_rel")


class ProjectsTable(Base):
    __tablename__ = 'projects'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    images = Column(JSONB, default=dict)
    blocks = Column(ARRAY(item_type=String))
    cover = Column(String, nullable=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    user = relationship("UserTable", back_populates="projects")


class ShareProjectTable(Base):
    __tablename__ = 'shared_projects'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    slug = Column(String, unique=True, nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False)

    project = relationship('ProjectsTable')


Base.metadata.create_all(engine)
