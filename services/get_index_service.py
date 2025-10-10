from llama_index.core import StorageContext,load_index_from_storage
from llama_index.vector_stores.chroma import ChromaVectorStore
from db.chroma_client import get_vector_db_client

from core.settings import embed_model, CHROMA_PATH
import logging
def get_index(user_name:str):
    chroma_client = get_vector_db_client()
    try:
        collection = chroma_client.get_collection(user_name)
        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=CHROMA_PATH)
        index = load_index_from_storage(storage_context=storage_context)
        return index
    
    except Exception as e:
        logging.error(f"Failed to create index for {user_name}: {e}")
        raise
