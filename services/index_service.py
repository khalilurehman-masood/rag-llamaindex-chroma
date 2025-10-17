from pathlib import Path
from core.settings import llm, embed_model, ollama_ef
from core.settings import CHROMA_PATH
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, settings,StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from llama_index.core import load_index_from_storage
from db.chroma_client import get_vector_db_client
from services.ingest_service import build_ingestion_pipeline



async def index_user_file(user_name:str, user_dir: str) -> dict:
    
    
    Path(CHROMA_PATH).mkdir(parents=True, exist_ok=True)

    # user_dir = Path(user_dir)
    docs = SimpleDirectoryReader(user_dir).load_data()



    vector_client = get_vector_db_client()
    print(vector_client.list_collections())

   

    ingestion_pipeline = build_ingestion_pipeline()

    try:
        collection = vector_client.get_collection(user_name)
        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        # index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        nodes = await ingestion_pipeline.arun(documents=docs, num_workers=4)
        index = VectorStoreIndex(nodes=[], storage_context=storage_context, embed_model=embed_model)
        index.insert_nodes(nodes=nodes)
        storage_context.persist(persist_dir=CHROMA_PATH)
        print("documents added to existing collection.")        
    except Exception:
        print("Collection not found, creating new one.")
        collection = vector_client.create_collection(user_name, embedding_function=ollama_ef)
        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        print(".................before pipeline.run().....................")
        nodes = await ingestion_pipeline.arun(documents=docs)
        print(".................after pipeline.run().....................")

        VectorStoreIndex(nodes=nodes, storage_context=storage_context, embed_model = embed_model)
        print("after index creation .................................")
        storage_context.persist(persist_dir=CHROMA_PATH)
        print("collection created!")

    return {
        "message":"File indexed successfully for user"     
        }


