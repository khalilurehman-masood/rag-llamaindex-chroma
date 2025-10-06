from fastapi import APIRouter, UploadFile, Form
from services.upload_service import upload_user_file

router = APIRouter()

@router.post("/upload")
async def upload_file(user_name:str = Form(...),upload_file : UploadFile = None):
    result = await upload_user_file(user_name, upload_file)
    return result