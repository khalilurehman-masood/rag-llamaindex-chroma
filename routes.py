from fastapi import APIRouter, UploadFile,BackgroundTasks, Form
from services.upload_service import upload_user_file

router = APIRouter()

@router.post("/upload")
async def upload_file(
    user_name: str = Form(...),
    upload_file: UploadFile = None,
    background_tasks : BackgroundTasks = None

):
    result = await upload_user_file(user_name=user_name,upload_file=upload_file, background_tasks = background_tasks)
    return result