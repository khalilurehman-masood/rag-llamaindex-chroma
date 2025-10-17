from llama_index.core.memory import Memory
from llama_index.core.llms import ChatMessage
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.memory import StaticMemoryBlock,FactExtractionMemoryBlock,VectorMemoryBlock
from core.settings import llm, embed_model, ollama_ef, CHATS_PATH,SQLITE_STRING
from db.chroma_client import get_vector_db_client
import os
from pathlib import Path


def get_memory(user_name: str, chat_id: str) -> Memory:
    chat_uri = get_chat_uri(user_name, chat_id)
    sqlite_uri = SQLITE_STRING + chat_uri

   

    blocks = get_memory_blocks(user_name,chat_id)
    memory = Memory.from_defaults(
        session_id=user_name,
        token_limit=30000,
        chat_history_token_ratio=0.7,
        token_flush_size=1000,
        memory_blocks=blocks,
        async_database_uri=sqlite_uri
    )
    return memory




def get_chat_uri(user_name:str, chat_id:str):
    # chat_dir = "chats"
    # os.makedirs(chat_dir, exist_ok=True)
    chat_dir = CHATS_PATH
    print("printing from get_chat_uri")
    print(chat_dir)
    # Create user folder
    user_chat_dir = os.path.join(chat_dir, user_name)
    os.makedirs(user_chat_dir, exist_ok=True)
    
    print(user_chat_dir)
    # File path for chat
    chat_uri = os.path.join(user_chat_dir, f"{chat_id}.sqlite3")
    chat_uri = Path(chat_uri).as_posix()

    
    return chat_uri


def get_memory_blocks(user_name:str, chat_id:str)->list:

    memory_blocks=[
        StaticMemoryBlock(
        name="core-info",
        static_content="My name is khalil, I line in Islamabad, I work with llamaindex.",
        priority=0
    ),

    FactExtractionMemoryBlock(
        name="extracted-info",
        llm=llm,
        max_facts=30,
        priority=1
    ),

    VectorMemoryBlock(
        name = "vector_memory",
        vector_store=get_chats_vector_store(user_name=user_name, chat_id = chat_id),
        priority=2,
        embed_model=embed_model,
        similarity_top_k=3,
        retrieval_context_window=5,
        

    ),
    ]
    return memory_blocks

def get_chats_vector_store(user_name:str, chat_id:str)->ChromaVectorStore:
    collection_name = f"{user_name}_{chat_id}_chat"
    try:
        vector_client = get_vector_db_client()
        chat_collection = vector_client.get_collection(collection_name)
        vector_store = ChromaVectorStore.from_collection(collection=chat_collection)
        return vector_store
      


    except:
        vector_client = get_vector_db_client()
        chat_collection = vector_client.create_collection(collection_name, embedding_function=ollama_ef)
        vector_store = ChromaVectorStore.from_collection(collection=chat_collection)
        return vector_store
        










