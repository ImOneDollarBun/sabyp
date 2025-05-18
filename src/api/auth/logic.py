from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from src.api.schemas import User, LoginAuth
from src.database.db_crud import create_user, get_logins, get_user
from src.utils.jwt_secure import encode_jwt
from src.utils.proceed_data import hash_password_dependency, get_current_user

auth_router = APIRouter()
AUTH_TOKEN_TTL = 4800


#Логика
@auth_router.post('/register')
async def signup(reg_form: User = Depends(hash_password_dependency)):
    try:
        if reg_form.username in get_logins():
            raise HTTPException(401, 'Username is already used')
    except TypeError:
        raise TypeError
    create_user(reg_form)
    user = get_user(reg_form.username)

    jwt_payload = {
        'username': user.username,
        '_id': user.public_id
    }
    token = encode_jwt(jwt_payload)

    response = RedirectResponse(url='/profile', status_code=303)
    response.set_cookie('access_token', token, max_age=AUTH_TOKEN_TTL, httponly=True, secure=True)

    return response


@auth_router.post('/login-in')
async def login(form_data: LoginAuth, user: User = Depends(get_current_user)):
    if user:
        return RedirectResponse('/profile', 303)
    user = get_user(form_data.username)

    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')

    jwt_payload = {
         'username': form_data.username,
         '_id': user.public_id
    }
    token = encode_jwt(jwt_payload)
    response = RedirectResponse(url='/profile', status_code=303)
    response.set_cookie('access_token', token, max_age=AUTH_TOKEN_TTL, httponly=True, secure=True)
    return response
