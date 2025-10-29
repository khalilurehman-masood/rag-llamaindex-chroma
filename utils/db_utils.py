import shutil
from pathlib import Path
from db.chroma_client import get_vector_db_client
from core.settings import CHROMA_PATH, STORAGE_PATH

def delete_collection_and_dir(department: str):
    """
    Deletes a Chroma collection and its corresponding directory.
    """
    vector_client = get_vector_db_client()
    try:
        # 1️⃣ Get the collection first (to extract ID before deletion)
        collection = vector_client.get_collection(department)
        collection_id = collection.id  # Chroma automatically assigns this
        
        # 2️⃣ Delete the collection itself
        vector_client.delete_collection(name=department)
        print(f"[INFO] Deleted Chroma collection: {department}")

        # 3️⃣ Delete its directory
        collection_dir = CHROMA_PATH / collection_id
        if collection_dir.exists() and collection_dir.is_dir():
            shutil.rmtree(collection_dir, ignore_errors=True)
            print(f"[INFO] Deleted collection directory: {collection_dir}")
        else:
            print(f"[WARN] Directory not found for collection ID: {collection_id}")


        #delete storage dir
        storage_dir = STORAGE_PATH / department
        if storage_dir.exists() and storage_dir.is_dir():
            shutil.rmtree(storage_dir, ignore_errors=True)
            print(f"[INFO] Deleted StorageContext directory: {storage_dir}")
        else:
            print(f"[WARN] No StorageContext directory found for department: {department}")

        print(f"[SUCCESS] Deleted all resources for department '{department}'.")
    except Exception as e:
        print(f"[ERROR] Failed to delete collection {department}: {e}")
