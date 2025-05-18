import os
import uuid
from contextlib import contextmanager
from uuid import UUID

from sqlalchemy.orm import joinedload, Session
from fastapi import HTTPException, UploadFile

from config import API
from . import SessionLocal
from .models import UserTable, PasswordsTable, ProjectsTable
from sqlalchemy import or_, and_
from src.utils.crypt import PSW2HASH

from src.api.schemas import User, ProjectOut, ShareLinkSchema, Project


def create_user(data: User):
    session = SessionLocal()
    try:
        new_user = UserTable(
            username=data.username,
            email=data.email,
            password_rel=PasswordsTable(password=data.password)
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user
    except Exception as e:
        session.rollback()
        return e
    finally:
        session.close()


def get_user(data: str):
    session = SessionLocal()
    try:
        user_obj = session.query(UserTable).options(
            joinedload(UserTable.password_rel)
        ).filter(
            or_(UserTable.email == data, UserTable.username == data, UserTable.public_id == data)
        ).first()

        return user_obj

    except Exception as e:
        session.rollback()
        return e
    finally:
        session.close()


def get_logins():
    session = SessionLocal()
    return session.query(UserTable.username).all()


@contextmanager
def get_session():
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def update_user(identify: str, *, email: str | None = None, raw_password: str | None = None):
    with get_session() as session:
        user: UserTable | None = (
            session.query(UserTable)
            .options(joinedload(UserTable.password_rel))
            .filter(or_(UserTable.email == identify, UserTable.username == identify))
            .first()
        )
        if user is None:
            raise ValueError("User not found")

        if email is not None:
            user.email = email

        if raw_password is not None:
            user.password_rel.password = PSW2HASH.crypt_psw(raw_password)


def create_project_for_user(user_id: UUID,
                            name: str = 'None',
                            description: str = None,
                            blocks: list = None,
                            cover: str = None,
                            images: dict = None):
    with get_session() as session:
        if session.query(ProjectsTable).filter_by(user_id=user_id).count() >= 5:
            raise ValueError("Достигнут лимит проектов")

        new_project = ProjectsTable(
            user_id=user_id,
            name=name,
            description=description,
            blocks=blocks,
            cover=cover,
            images=images
        )
        session.add(new_project)
        session.commit()
        session.refresh(new_project)
        return new_project.id


def get_project_by_id(project_id: str):
    with get_session() as session:
        project = session.query(ProjectsTable).filter(ProjectsTable.id == project_id).first()
        if project:
            return ProjectsTable(
                id=project.id,
                name=project.name,
                description=project.description,
                images=project.images,
                blocks=project.blocks,
                cover=project.cover,
                user_id=project.user_id
            )
        return None


def get_user_projects(user_id: UUID):
    with get_session() as session:
        projects = session.query(ProjectsTable).filter(ProjectsTable.user_id == user_id).all()
        return [ProjectOut(id=project.id, title=project.name, description=project.description) for project in projects]


def get_project_by_name(project_name: str, username: str):
    with get_session() as session:
        user = session.query(UserTable).filter(UserTable.username == username).first()
        project = session.query(ProjectsTable).filter(and_(ProjectsTable.name == project_name,
                                                           ProjectsTable.user_id == user.id)).first()
        return Project(id=project.id,
                       name=project.name,
                       description=project.description,
                       cover=project.cover,
                       images=project.images,
                       blocks=project.blocks,
                       user_id=project.user_id)


def save_file(file: UploadFile, user_id: UUID, folder: str = API.media_dir) -> str:
    if not file or not file.filename:
        raise ValueError("Файл не был передан или пустой filename")

    os.makedirs(folder, exist_ok=True)
    file_name = f"{user_id}_{file.filename}"
    file_path = os.path.join(folder, file_name)
    file.file.seek(0)
    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)

    return "/" + file_path


def update_project_data(project_id, name, user_id, cover, images_files, description, blocks):
    with get_session() as session:
        project = session.query(ProjectsTable).filter(ProjectsTable.id == project_id).first()
        if not project:
            raise ValueError("Проект не найден")

        project.name = name
        project.user_id = user_id
        project.cover = cover
        project.images = images_files
        project.description = description
        project.blocks = blocks
        session.commit()



def delete_project_db(project_id: UUID):
    with get_session() as session:
        project = session.get(ProjectsTable, project_id)
        if project:
            session.delete(project)
            session.commit()


def generate_share_link(project_id: UUID):
    with get_session() as session:
        project = session.get(ProjectsTable, project_id)
        user = session.get(UserTable, project.user_id)
        if project:
            return ShareLinkSchema(slug=f'{user.username}/{project.name}')

