
from db.chroma_client import get_vector_db_client
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex
from core.settings import llm

from core.temp_state import results
# def query_user_file(user_name:str, query:str):
#     vector_client = get_vector_db_client()
#     try:
#         collection = vector_client.get_collection(user_name)
#         print("Collection exists, I am from query_user_index function!")
#         vector_store = ChromaVectorStore(chroma_collection=collection)
#         print("after vectore store")
#         index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
#         print("after vector store . from vector store")
#         query_engine = index.as_query_engine()
#         print("after . as query engine")
#         print(query)
#         # result = query_engine.query(query)
#         print("afetr .query")
#         print("collection loaded!")
#         return "finished"
        
#     except Exception as e:
#         return "No user collection found, please upload a document!"

def run_query_task(user_name, query, query_id):
    vector_client = get_vector_db_client()
    collection = vector_client.get_collection(user_name)
    vector_store = ChromaVectorStore(chroma_collection=collection)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    print(index.__dict__)
    query_engine = index.as_query_engine(llm=llm)
    print("after query engine")
    print(query_engine.__dict__)
    result = query_engine.query(query).response
    # result = "not perfect"
    print("after .query()")
    results[query_id]  = str(result)
    return results