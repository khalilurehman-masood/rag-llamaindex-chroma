from pathlib import Path
from core.settings import llm, embed_model, ollama_ef
from core.settings import CHROMA_PATH, STORAGE_PATH
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, settings,StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from llama_index.core import load_index_from_storage
from db.chroma_client import get_vector_db_client
from services.ingest_service import build_ingestion_pipeline
from services.get_index_service import get_storage_context, get_index ,create_or_get_storage_context_path
from llama_index.core import Document
import json

            

async def index_user_file(user_name:str, department:str, roles:list[str], user_dir: str, file_path:str) -> dict:
    print(f"All roles recieved{roles}")
    def set_document_metadata(file_path:Path):
  
        meta_data = {}
        for role in roles:
            meta_data[role.lower()]="true"
        meta_data['department']=department.lower().strip()

        return meta_data
    Path(CHROMA_PATH).mkdir(parents=True, exist_ok=True)


    # user_dir = Path(user_dir)
    docs = SimpleDirectoryReader(input_files=[file_path], file_metadata=set_document_metadata, filename_as_id=True).load_data()


    vector_client = get_vector_db_client()
   

   


    try:
        # collection = vector_client.get_collection(department)
        # vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = get_storage_context(department = department)
        # storage_context = StorageContext.from_defaults(vector_store = vector_store,persist_dir=STORAGE_PATH)
        print("after storage context")
        # index = load_index_from_storage(storage_context=storage_context) 
        index = get_index(department=department)
        # index = VectorStoreIndex.from_vector_store(vector_store = vector_store , storage_context=storage_context, embed_model=embed_model)
        # index = get_index(department)
        doc_store = storage_context.docstore
        vectorstore = storage_context.vector_store
        vectorstore = index.storage_context.vector_store
    


    except Exception as e:
        print("Collection not found, creating new one.")
        # collection = vector_client.create_collection(department, embedding_function=ollama_ef)
        # vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = get_storage_context(department=department)
        print("storage context recieved")

        
        
        index = VectorStoreIndex(
            nodes=[],
            storage_context=storage_context,
            embed_model=embed_model
        )
        
        doc_store = storage_context.docstore
        vectorstore = storage_context.vector_store

    
        

    ingestion_pipeline = build_ingestion_pipeline(vectorstore, doc_store)
    
    print(".................before pipeline.run().....................")
    nodes = ingestion_pipeline.run(documents=docs)
    print(".................after pipeline.run().....................")
    print(len(nodes))
    index.insert_nodes(nodes)
    print("after index creation .................................")
    # index.storage_context.persist(persist_dir=CHROMA_PATH)
    print("after index persistance.")
    storage_path = create_or_get_storage_context_path(department=department)
    storage_context.persist(persist_dir=storage_path)
    print("storage persisted")

    return {
        "message":"File indexed successfully for user"     
        }




