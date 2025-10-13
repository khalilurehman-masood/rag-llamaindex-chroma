
from db.chroma_client import get_vector_db_client
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.llms import ChatMessage
from core.settings import llm,embed_model, CHROMA_PATH
from services.memory_service import get_memory
from services.get_index_service import get_index


async def query_user_file_with_memory(user_name:str, query:str):
    memory = get_memory(user_name, "abcd")

    index = get_index(user_name)
    
    chat_engine = index.as_chat_engine(llm=llm, chat_mode="condense_plus_context",memory = memory, system_prompt=("you are a helpful assistant that can answer general questions as well as quetions asked from the provided context. Please be concise."))

    response =await chat_engine.achat(query)
    return {
        "response":response
    }
