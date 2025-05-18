from fastapi import APIRouter, Request, Depends, HTTPException, Cookie
from fastapi.responses import RedirectResponse

from src.database.db_crud import create_user, get_user, get_logins
from src.utils.crypt import PSW2HASH
from src.utils.jwt_secure import encode_jwt, decode_jwt
from src.utils.proceed_data import hash_password_dependency, get_current_user
from .schemas import User, LoginAuth

router = APIRouter()


#Логика
@router.post('/register')
async def signup(reg_form: User = Depends(hash_password_dependency)):
    try:
        if reg_form.username in get_logins():
            raise HTTPException(401, 'Username is already used')
    except TypeError:
        pass
    create_user(reg_form)

    jwt_payload = {
        'username': reg_form.username
    }
    token = encode_jwt(jwt_payload)

    response = RedirectResponse(url='/profile', status_code=303)
    response.set_cookie('access_token', token, max_age=1200, httponly=True, secure=True)

    return response


@router.post('/login-in')
async def login(form_data: LoginAuth, user: User = Depends(get_current_user)):
    if user:
        jwt_payload = {
             'username': form_data.username
        }
        token = encode_jwt(jwt_payload)

        response = RedirectResponse(url='/profile', status_code=303)
        response.set_cookie('access_token', token, max_age=1200, httponly=True, secure=True)

        return response
    else:
        raise HTTPException(401, 'Invalid credentials')


@router.get('/projects/{project_id}/edit')
async def edit_prj(request: Request, project_id, access_token: str = Cookie(...)):
    ...
    #if decode_jwt(access_token)['username']:
        #return templates.TemplateResponse('edit.html', {'request': request})