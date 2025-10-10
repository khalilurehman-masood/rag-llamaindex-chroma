from llama_index.core.memory import Memory
from llama_index.core.llms import ChatMessage
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.memory import StaticMemoryBlock,FactExtractionMemoryBlock,VectorMemoryBlock
from core.settings import llm, embed_model, embed_fn, CHROMA_PATH
from db.chroma_client import get_vector_db_client
import os



def get_memory(user_name: str, chat_id: str) -> Memory:

    chat_store = get_chat_store(user_name, chat_id)
    blocks = get_memory_blocks(user_name,chat_id)
    memory = Memory.from_defaults(
        session_id=user_name,
        chat_history=chat_store,
        token_limit=30000,
        chat_history_token_ratio=0.7,
        token_flush_size=1000,
        memory_blocks=blocks
    )
    return memory


def get_chat_store(user_name:str, chat_id:str) -> SimpleChatStore:
    chat_dir = "chats"
    os.makedirs(chat_dir, exist_ok=True)

    # Create user folder
    user_chat_dir = os.path.join(chat_dir, user_name)
    os.makedirs(user_chat_dir, exist_ok=True)

    # File path for chat
    user_chat_path = os.path.join(user_chat_dir, f"{chat_id}.json")

    # Create persistent SimpleChatStore
    chat_store = SimpleChatStore.from_persist_path(persist_path=user_chat_path)
    if not os.path.exists(user_chat_path) or len(chat_store.store) == 0:
        chat_store.add_message(key="messages", message=ChatMessage(role="assistant", content="How can I help you today?"))

    chat_store.persist(persist_path=user_chat_path)
    return chat_store


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
        chat_collection = vector_client.create_collection(collection_name, embedding_function=embed_fn)
        vector_store = ChromaVectorStore.from_collection(collection=chat_collection)
        return vector_store


    except:
        vector_client = get_vector_db_client()
        chat_collection = vector_client.get_collection(collection_name)
        vector_store = ChromaVectorStore.from_collection(collection=chat_collection)
        return vector_store





# def get_memory(user_name: str) -> Memory:

#     memory = Memory.from_defaults(
#         session_id=user_name,
#         token_limit=30000,
#         chat_history_token_ratio=0.7,
#         token_flush_size=3000,
#     )
#     return memory











# def get_memory(user_name:str) -> Memory:
#     memory = Memory.from_defaults(
#         session_id=user_name,
#         token_limit=30000,
#         chat_history_token_ratio=0.7,
#         token_flush_size=3000,

#     )
#     return memory



