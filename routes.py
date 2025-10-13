import uuid
from fastapi import APIRouter, UploadFile,BackgroundTasks, Form
from services.upload_service import upload_user_file
# from services.query_service import query_user_file
from services.query_service import query_user_file_with_memory
# from services.query_service import run_query_task
from core.temp_state import results
router = APIRouter()

@router.post("/upload")
async def upload_file(
    user_name: str = Form(...),
    upload_file: UploadFile = None,
    background_tasks : BackgroundTasks = None

):
    result = await upload_user_file(user_name=user_name,upload_file=upload_file, background_tasks = background_tasks)
    return result

# @router.post("/query/start")
# def start_query(user_name: str = Form(...), query: str = Form(...), background_tasks:BackgroundTasks= None):
#     query_id = str(uuid.uuid4())
#     # results[query_id] = "processing...."
    
#     background_tasks.add_task(run_query_task, user_name, query, query_id)
#     return {"query_id": query_id, "status": "started"}

# @router.get("/query/status/{query_id}")
# def get_query_result(query_id:str):
#     print(results)
#     return {"query_id":query_id, "query_results":results.get(query_id,"processing....")}

@router.get("/query")
async def query_index(user_name:str, query:str):
    # result =query_user_file(user_name = user_name, query = query)
    result =await query_user_file_with_memory(user_name = user_name, query = query)

    return result