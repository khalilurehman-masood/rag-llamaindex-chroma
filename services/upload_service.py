from fastapi import UploadFile, BackgroundTasks
async def upload_user_file(user_name:str,department:str, roles:str, upload_file:UploadFile, background_tasks:BackgroundTasks)-> dict:
    import os
    from utils.path_utils import get_base_dir
    from services.index_service import index_user_file



    BASE_DIR = get_base_dir()
    files_dir= BASE_DIR/"data"/department

    files_dir.mkdir(exist_ok=True)

    file_path = files_dir/upload_file.filename

    roles_list = [r.strip() for r in roles.split(",") if r.strip()]
    


    with open(file_path, "wb") as f:
        f.write(await upload_file.read())
    print("before background tasks in upload_services")
    background_tasks.add_task(index_user_file,user_name,department,roles_list, files_dir, file_path )
    print("after backround tasks in the index services")

    return {
        "message":"File Uploaded Sucessfully!",
        "file_path":str(file_path),
    }
