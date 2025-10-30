from llama_index.core import StorageContext,load_index_from_storage, VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from db.chroma_client import get_vector_db_client
from core.settings import CHROMA_PATH, STORAGE_PATH, ollama_ef
import logging, os
def get_index(department:str):
    chroma_client = get_vector_db_client()
    try:
        collection = chroma_client.get_collection(department)
        vector_store = ChromaVectorStore(chroma_collection=collection)
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        return index
    
    except Exception as e:
        logging.error(f"Failed to get index for {department}: {e}")
        raise







def get_storage_context(department: str) -> StorageContext:
    """
    Creates or loads a StorageContext linked to a specific Chroma collection 
    and a unique local metadata directory.
    
    Args:
        department (str): The name of the Chroma collection (e.g., 'sales', 'hr').
        vector_client (chromadb.Client, optional): The persistent Chroma client. 
                                                   If None, it's initialized here.
                                                   
    Returns:
        StorageContext: The fully configured StorageContext object.
    """
    vector_client = get_vector_db_client()
    

    
   
    try:
        collection = vector_client.get_collection(department)
        print("got collection already created.")
    except Exception:
        print("before creating new collection")
        collection = vector_client.create_collection(department, embedding_function = ollama_ef) # Create if missing
        print("after creating new collection")
    vector_store = ChromaVectorStore(chroma_collection=collection)
    print("after initializing vector store")
    
    
    print('before storage_context initialization')
    try:
        print(create_or_get_storage_context_path(department=department))
        storage_context = StorageContext.from_defaults(
        persist_dir=create_or_get_storage_context_path(department=department),
       
        vector_store=vector_store,
        )
        print("storage_context from path")
    except:
        storage_context = StorageContext.from_defaults(
        vector_store=vector_store,
    )
    print("before returning storage_context......................")
    return storage_context







def create_or_get_storage_context_path(department:str):
    print(f"from withing the create or get storage path:{department}")
    storage_path = os.path.join(STORAGE_PATH, f"{department}")

    # storage_path = STORAGE_PATH/department
    os.makedirs(storage_path, exist_ok=True)
    return storage_path

    

# # --- Usage Example (How your get_index function would use it) ---

# def get_index(department: str, embed_model, vector_client):
#     """Loads or creates the VectorStoreIndex for a given department."""
    
#     # 1. Get the configured StorageContext
#     storage_context = get_storage_context(department, vector_client)
    
#     # 2. Check if the index structure (IndexStore) exists 
#     #    (to distinguish between loading and creating)
#     is_new_index = not os.path.exists(os.path.join(storage_context.persist_dir, "index_store.json"))

#     if is_new_index:
#         print(f"Index for {department} not found. Creating a new one.")
#         # Create a new index instance (empty, the data goes into Chroma/DocStore later)
#         index = VectorStoreIndex(
#             nodes=[],
#             storage_context=storage_context,
#             embed_model=embed_model
#         )
#         # Note: Must persist the initial empty structure!
#         storage_context.persist() 
#     else:
#         print(f"Loading existing index for {department}.")
#         # Load the index structure using the already-configured storage context
#         index = VectorStoreIndex.from_vector_store(
#             vector_store=storage_context.vector_store,
#             storage_context=storage_context,
#             embed_model=embed_model
#         )
        
#     return index