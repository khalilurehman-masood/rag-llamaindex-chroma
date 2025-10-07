import os, chromadb
from pathlib import Path
from core.settings import CHROMA_PATH
db_path = os.path.abspath(CHROMA_PATH)
os.makedirs(CHROMA_PATH, exist_ok=True)

# create a persistent client

def get_vector_db_client():


    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client
