from fastapi import APIRouter,Depends
from helpers.config import get_settings,Settings
base_router = APIRouter(prefix="/api/v1",tags=["api_v1"])
@base_router.get("/")
async def read_root(settings:Settings=Depends(get_settings)):
    
    app_name = settings.APP_NAME
    app_ves = settings.APP_VERSION
    return {"message": f"Welcome to {app_name} version {app_ves}"}