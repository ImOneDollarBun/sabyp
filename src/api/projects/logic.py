import json
import logging
import os

from fastapi import APIRouter, Depends
from fastapi import Request, UploadFile, Form, HTTPException, File
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from config import API
from src.api.schemas import User, ShareLinkSchema
from src.database.db_crud import (get_project_by_id, update_project_data, create_project_for_user,
                                  delete_project_db, generate_share_link, get_project_by_name, save_file)
from src.utils.proceed_data import get_current_user, auth

project_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@project_router.post('/api/projects')
async def add_project_id(user: User = Depends(get_current_user)):
    project_id = create_project_for_user(user.id)
    return RedirectResponse(f'/projects/{project_id}/edit')


@project_router.get('/projects/{project_id}')
async def redir(project_id):
    return RedirectResponse('/profile', 303)


@project_router.get('/projects/{project_id}/edit')
async def edit_prj(request: Request, user: User = Depends(get_current_user)):
    if user:
        return templates.TemplateResponse('edit.html', {'request': request, 'user': user})
    return RedirectResponse('/login', 303)


@project_router.get('/project/share/{project_id}')
async def share_link(project_id):
    slug = generate_share_link(project_id)
    return ShareLinkSchema(slug=f'https://geoto.site/projects/{slug.slug}')
    # return ShareLinkSchema(slug=f'http://127.0.0.1:5000/projects/{slug.slug}')


@project_router.get('/projects/{username}/{project_name}')
async def read_project(request: Request, username: str, project_name: str, user: User = Depends(get_current_user)):
    #project = get_project_by_name(project_name, username)
    #if user.username == username:
    #    return RedirectResponse(f'/projects/{project.id}/edit')

    return templates.TemplateResponse('see_project.html', {'request': request})


@project_router.get('/api/get_project_data/{author}/{project_name}')
async def get_project_data(author, project_name):
    project = get_project_by_name(project_name, author)
    return project


@project_router.get('/api/projects/{project_id}')
async def get_project(project_id: str, request: Request, authorization=Depends(auth)):
    project = get_project_by_id(project_id)
    if not project:
        raise HTTPException(404, detail="Проект не найден")

    return {
        'title': project.name,
        'description': project.description,
        'blocks': project.blocks,
        'cover': project.cover,
        'images': [p for p in project.images.values()] if project.images else []
    }


@project_router.put('/api/projects/{project_id}')
async def update_project(
    request: Request,
    project_id: str,
    cover: UploadFile | None = File(None),
    title: str = Form(...),
    blocks: str = Form(...),
    description: str = Form(...),
    user: User = Depends(get_current_user),
):
    project = get_project_by_id(project_id)
    if not project:
        raise HTTPException(404, detail="Проект не найден")

    upload_dir = f"{API.media_dir}/{project_id}/"

    # Обработка обложки
    cover_path = save_file(cover, folder=upload_dir, user_id=user.id) if cover else project.cover

    # Получение form-data
    form_data = await request.form()

    # Извлекаем images словарь из form-data
    images_dict = json.loads(form_data.get("images", "{}"))
    upload_images = upload_dir + 'images/'

    for key in list(images_dict):
        file = form_data.get(key)

        if file:
            image_path = save_file(file, folder=upload_images, user_id=user.id)
            images_dict[key] = image_path
        else:
            pass

    update_project_data(
        project_id=project_id,
        name=title,
        user_id=user.id,
        cover=cover_path,
        images_files=images_dict,
        description=description,
        blocks=json.loads(blocks)
    )

    return JSONResponse({"status": "ok"})


@project_router.delete('/api/projects/{project_id}')
async def delete_project(project_id, user: User = Depends(get_current_user)):
    if user:
        delete_project_db(project_id)
