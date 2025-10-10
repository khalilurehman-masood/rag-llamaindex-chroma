
from db.chroma_client import get_vector_db_client
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.llms import ChatMessage
from core.settings import llm,embed_model, CHROMA_PATH
from services.memory_service import get_memory
from services.get_index_service import get_index
# from core.temp_state import results
# def query_user_file(user_name:str, query:str):
#     vector_client = get_vector_db_client()
#     try:
#         vector_client = get_vector_db_client()
#         collection = vector_client.get_collection(user_name)
#         vector_store = ChromaVectorStore(chroma_collection=collection)
#         storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=CHROMA_PATH)
#         index = load_index_from_storage(storage_context=storage_context)        
#         query_engine = index.as_query_engine(llm=llm)
#         result = query_engine.query(query).response
#         return result
        
#     except Exception as e:
#         return "No user collection found, please upload a document!"

def query_user_file_with_memory(user_name:str, query:str):
    memory = get_memory(user_name, "abc")
    memory.put_messages([ChatMessage(role="user", content=query)])

    index = get_index(user_name)
    # retriever = index.as_retriever(embed_model=embed_model)
    # chat_engine = index.as_chat_engine(llm=llm, chat_mode="context",memory = memory, system_prompt=("you are a helpful assistant that can answer general questions as well as quetions asked from the provided context. Please be concise."))
    chat_engine = index.as_chat_engine(llm=llm, chat_mode="condense_plus_context",memory = memory, system_prompt=("you are a helpful assistant that can answer general questions as well as quetions asked from the provided context. Please be concise."))


    # retrieved_nodes = retriever.retrieve(query)

    # retrieved_texts = [node.get_content() for node in retrieved_nodes]

    # messages = []
    # for text in retrieved_texts:
    #     messages.append(ChatMessage(role="system", content=f"Context: {text}",additional_kwargs={"source_role":"RetrievedContext"}))
    
     
    # messages.extend(memory.get())
    print(memory.get_all())

    # response = llm.chat(messages)
    response = chat_engine.chat(query)
    return {
        "response":response
    }
# def run_query_task(user_name, query, query_id):
#     vector_client = get_vector_db_client()
#     collection = vector_client.get_collection(user_name)
#     print("chollection dictionary......................")
#     print(collection.__dict__)
#     vector_store = ChromaVectorStore(chroma_collection=collection)
#     storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=CHROMA_PATH)
#     index = load_index_from_storage(storage_context=storage_context)
#     print(index.__dict__)
#     query_engine = index.as_query_engine(llm=llm)
#     print("after query engine")
#     print(query_engine.__dict__)
#     result = query_engine.query(query).response
#     print("after .query()")
#     results[query_id]  = str(result)
#     return results