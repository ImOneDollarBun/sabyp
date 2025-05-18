import os

from fastapi import UploadFile
from io import BytesIO

from config import API
from src.database.db_crud import save_file
from uuid import UUID

user_id = UUID('82465074-2394-466d-87f3-42b559c581bb')
project_id = 'b22a3568-113f-4d07-8bb7-7c43406ee155'
upload_dir = f"{API.media_dir}/{project_id}/images/"

# Пример содержимого файла
with open('static/default-cover.jpg', 'rb') as file:

    # Создание объекта UploadFile вручную
    fake_file = UploadFile(filename='default-cover.jpg', file=file)

    # Сохранение
    path = save_file(fake_file, user_id=user_id, folder=upload_dir)
    print(path)
