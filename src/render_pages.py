from fastapi import APIRouter, Request, Cookie, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .utils.jwt_secure import decode_jwt

from .api.schemas import User

from .utils.proceed_data import get_current_user

pages_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@pages_router.get('/', response_class=HTMLResponse, description='Show main page')
async def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@pages_router.get('/signup', response_class=HTMLResponse, description='Show another page')
async def register(request: Request):
    return templates.TemplateResponse('signup.html', {'request': request})


@pages_router.get('/login', response_class=HTMLResponse, description='Show auth page')
async def log(request: Request, user: User = Depends(get_current_user)):
    if user:
        return templates.TemplateResponse('profile.html', {'request': request, 'user': user})
    return templates.TemplateResponse('auth.html', {'request': request})


@pages_router.get('/projects')
async def edit(request: Request):
    return templates.TemplateResponse('edit.html', {'request': request})


@pages_router.get('/profile')
async def profile(request: Request, user: User = Depends(get_current_user)):
    if user:
        return templates.TemplateResponse('profile.html', {'request': request, 'user': user})
    return RedirectResponse('/login', status_code=status.HTTP_307_TEMPORARY_REDIRECT)
