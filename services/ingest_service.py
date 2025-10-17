from pathlib import Path
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor, QuestionsAnsweredExtractor
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from core import settings
import chromadb


def build_ingestion_pipeline()->IngestionPipeline:

    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP),
            # TitleExtractor(),
            # QuestionsAnsweredExtractor(),
        ]
    )

    return pipeline



