from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

from pathlib import Path

MODELS_BASE_URL = "http://192.168.2.62:11434"
LLM_MODEL = "llama3.1:latest"
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
    


Settings.llm = llm
Settings.embed_model = embed_model

# embed_model = HuggingFaceEmbedding(
#     model_name = "BAAI/bge-base-en"
#     )






BASE_DIR =Path(__file__).resolve().parent.parent

CHROMA_PATH = (BASE_DIR/"vector_stores").as_posix()

