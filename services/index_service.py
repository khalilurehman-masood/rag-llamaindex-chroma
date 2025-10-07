from pathlib import Path
from core.settings import CHROMA_PATH
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, settings,StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from db.chroma_client import get_vector_db_client
async def index_user_file(user_name:str, user_dir: str) -> dict:
    Path(CHROMA_PATH).mkdir(parents=True, exist_ok=True)

    # user_dir = Path(user_dir)
    docs = SimpleDirectoryReader(user_dir).load_data()



    vector_client = get_vector_db_client()
    # collection = vector_client.get_or_create_collection(user_name)
    # print(collection.name)
    # vector_store = ChromaVectorStore(chroma_collection=collection)
    # print(type(vector_store))
    # storage_context = StorageContext.from_defaults(vector_store=vector_store)
    # print(type(storage_context))

    try:
        collection = vector_client.get_collection(user_name)
        print("Collection exists, loading from vector store.")
        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        VectorStoreIndex.from_vector_store(vector_store=vector_store)
        print("collection loaded!")
    except Exception:
        print("Collection not found, creating new one.")
        collection = vector_client.create_collection(user_name)
        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        VectorStoreIndex.from_documents(docs, storage_context=storage_context)
        storage_context.persist(persist_dir=CHROMA_PATH)
        print("collection created!")

    # if collection.count()==0:
    #     print("after collection.count()")
    #     print(docs)
    #     # Embed documents if collection is empty
    #     VectorStoreIndex.from_documents(docs, storage_context=storage_context)
    #     print("after vector store index . from documents")
    #     storage_context.persist(persist_dir=CHROMA_PATH)
    #     print("created from documents")
    # else:
    #     # Load existing embeddings from vector store
    #     print("before creating from vector store")
    #     VectorStoreIndex.from_vector_store(vector_store=vector_store)
    #     print("created from vector store")

    return {
        "message":"File indexed successfully for user"     
        }