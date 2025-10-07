from fastapi import UploadFile, BackgroundTasks
async def upload_user_file(user_name:str, upload_file:UploadFile, background_tasks:BackgroundTasks)-> dict:
    import os
    from utils.path_utils import get_base_dir
    from services.index_service import index_user_file



    BASE_DIR = get_base_dir()
    user_dir= BASE_DIR/"data"/user_name

    user_dir.mkdir(exist_ok=True)

    file_path = user_dir/upload_file.filename

    with open(file_path, "wb") as f:
        f.write(await upload_file.read())
    print("before background tasks in upload_services")
    background_tasks.add_task(index_user_file,user_name, user_dir)
    print("after backround tasks in the index services")

    return {
        "message":"File Uploaded Sucessfully!",
        "file_path":str(file_path),
    }
