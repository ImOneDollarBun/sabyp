import os

from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# FastApi
APP_PORT = os.getenv('APP_PORT')


class API:
    media_dir = 'media/projects'


# Postgres
class Database:
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    url = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


class auth_jwt:
    algorithm = 'RS256'
    public_key_path = os.path.join(BASE_DIR, 'keys', 'public_key.pem')
    private_key_path = os.path.join(BASE_DIR, 'keys', 'private_key.pem')


class Redis:
    HOST = 'localhost'
    PORT = 6379
