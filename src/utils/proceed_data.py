import os
import uuid

from fastapi import Cookie, UploadFile, status

from src.api.schemas import User
from src.database.db_crud import get_user
from src.utils.crypt import PSW2HASH
from .jwt_secure import decode_jwt
from config import API


async def hash_password_dependency(user: User) -> User:
    user.password = PSW2HASH.crypt_psw(user.password)
    return user


async def get_current_user(access_token: str | None = Cookie(None)) -> User | None:
    if not access_token:
        return None
    try:
        payload = decode_jwt(access_token)
        return get_user(payload["username"])
    except Exception:
        return None


async def auth(access_token: str | None = Cookie(None)) -> User:
    try:
        if not access_token:
            raise status.HTTP_401_UNAUTHORIZED
        return get_user(decode_jwt(access_token)['username'])
    except Exception as e:
        raise e
