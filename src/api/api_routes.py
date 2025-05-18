from fastapi import APIRouter, Depends, HTTPException, status

from src.database.db_crud import update_user, get_user_projects
from src.utils.proceed_data import get_current_user
from .schemas import User

api_router_api = APIRouter()


@api_router_api.get("/api/me")
def get_my_profile(user: User = Depends(get_current_user)):
    projects = get_user_projects(user.id)
    return {
        "email": user.email,
        "username": user.username,
        "projects": projects
    }


@api_router_api.put('/api/me')
async def put_account(new_data: User, user=Depends(get_current_user)):
    if user:
        return update_user(new_data.username, email=new_data.email, raw_password=new_data.password)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
