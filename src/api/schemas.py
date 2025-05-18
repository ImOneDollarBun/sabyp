from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr

from src.database.models import UserTable


class User(BaseModel):
    username: str
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginAuth(BaseModel):
    username: EmailStr | str
    password: str


class Project(BaseModel):
    id: UUID
    name: str
    description: str
    images: dict
    cover: str
    blocks: list

    user_id: UUID


class ProjectOut(BaseModel):
    id: UUID
    title: str
    description: str | None

    class Config:
        from_attributes = True


class UserProfileOut(BaseModel):
    email: str
    username: str
    projects: List[ProjectOut]


class ShareLinkSchema(BaseModel):
    slug: str
