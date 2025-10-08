from pathlib import Path
from core.settings import llm, embed_model
from core.settings import CHROMA_PATH
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, settings,StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from db.chroma_client import get_vector_db_client
def index_user_file(user_name:str, user_dir: str) -> dict:
    
    
    Path(CHROMA_PATH).mkdir(parents=True, exist_ok=True)

    # user_dir = Path(user_dir)
    docs = SimpleDirectoryReader(user_dir).load_data()



    vector_client = get_vector_db_client()
    print(vector_client.list_collections())

    try:
        collection = vector_client.get_collection(user_name)
        vector_store = ChromaVectorStore(chroma_collection=collection)
        StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        engine = index.as_query_engine(llm  = llm)
        print(engine.query("hugging").response)
    except Exception:
        print("Collection not found, creating new one.")
        collection = vector_client.create_collection(user_name)
        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        VectorStoreIndex.from_documents(docs, storage_context=storage_context, embed_model = embed_model)
        storage_context.persist(persist_dir=CHROMA_PATH)
        print("collection created!")

    return {
        "message":"File indexed successfully for user"     
        }


