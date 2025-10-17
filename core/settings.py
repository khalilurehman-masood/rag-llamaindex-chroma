from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

from pathlib import Path

MODELS_BASE_URL = "http://192.168.2.62:11434"
LLM_MODEL = "llama3:latest"
EMBED_MODEL = "nomic-embed-text:latest"


llm = Ollama(
    model = LLM_MODEL,
    base_url = MODELS_BASE_URL,
    request_timeout=120
)

embed_model = OllamaEmbedding(
    model_name=EMBED_MODEL,
    base_url=MODELS_BASE_URL
)

ollama_ef= OllamaEmbeddingFunction(
     url="http://192.168.2.62:11434",
    model_name="nomic-embed-text:latest",
)

Settings.llm = llm
Settings.embed_model = embed_model


# embed_model = HuggingFaceEmbedding(
#     model_name = "BAAI/bge-base-en"
#     )






BASE_DIR =Path(__file__).resolve().parent.parent

CHROMA_PATH = BASE_DIR/"vector_stores"
CHATS_PATH = BASE_DIR/"chats"

SQLITE_STRING = "sqlite+aiosqlite:///"  #sqlite string

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

FETCH_K = 60
TOP_K = 6
MMR_LAMBDA = 0.6
USE_RERANKER = True