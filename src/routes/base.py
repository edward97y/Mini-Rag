from fastapi import APIRouter
import os


base_router = APIRouter(prefix="/api/v1",tags=["api_v1"])
@base_router.get("/")
async def read_root():
    app_name=os.getenv("APP_NAME")
    app_ves =os.getenv("APP_VERSION")
    return {"message": f"Welcome to {app_name} version {app_ves}"}