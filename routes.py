import uuid
from fastapi import APIRouter, UploadFile,BackgroundTasks, Form
from services.upload_service import upload_user_file
# from services.query_service import query_user_file
from services.query_service import query_user_file
# from services.query_service import run_query_task
from services.documents_service import get_documents_list, delete_item,update_item,get_chunks_list
router = APIRouter()

@router.post("/upload")
async def upload_file(
    user_name: str = Form(...),
    department:str=Form(...),
    roles:str=Form(...),
    upload_file: UploadFile = None,
    background_tasks : BackgroundTasks = None

):
    result = await upload_user_file(user_name=user_name,department=department,roles = roles, upload_file=upload_file, background_tasks = background_tasks)
    return result


@router.post("/query")
async def query_index(user_name:str=Form(...),role:str=Form(...),department:str=Form(...), query:str=Form(...)):
    # result =query_user_file(user_name = user_name, query = query)
    result =await query_user_file(user_name = user_name,role=role,department=department, query = query)

    return result


@router.post("/list")
def list_documents(role:str=Form(...), department:str=Form(...)):
    result = get_documents_list(role=role, department= department)
    return result

@router.post("/getchunks")
def get_chunks(role:str=Form(...),department:str=Form(...),query:str=Form(...)):
    result = get_chunks_list(role=role, department=department, query=query)
    return result


@router.post("/delete")
def delete(role:str = Form(...), department:str= Form(...),type:str= Form(...), identifier:str= Form(...)):
    result = delete_item(role=role,department=department,type=type,identifier=identifier)
    return result


@router.post("/update")
def update(role:str = Form(...), department:str= Form(...),type:str= Form(...), identifier:str= Form(...), text:str=Form(...)):
    result = update_item(role=role,department=department,type=type,identifier=identifier, text=text)
    return result