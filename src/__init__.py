from .api.api_routes import api_router_api
from .api.auth.logic import auth_router
from .api.projects.logic import project_router
from .render_pages import pages_router


from fastapi import APIRouter

rout = APIRouter()
rout.include_router(project_router)
rout.include_router(auth_router)
rout.include_router(pages_router)
rout.include_router(api_router_api)
