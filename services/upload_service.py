from fastapi import UploadFile
async def upload_user_file(user_name:str, upload_file:UploadFile)-> dict:
    import os
    from utils.path_utils import get_base_dir
    from fastapi import UploadFile
    # from services.index_service import index_user_file



    BASE_DIR = get_base_dir()
    user_dir= BASE_DIR/"data"/user_name

    user_dir.mkdir(exist_ok=True)

    file_path = user_dir/upload_file.filename

    with open(file_path, "wb") as f:
        f.write(await upload_file.read())

    # await index_user_file(user_name, str(file_path))

    return {
        "message":"File Uploaded Sucessfully!",
        "username":user_name,
        "file_path":str(file_path)
    }
