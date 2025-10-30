from pathlib import Path
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor, QuestionsAnsweredExtractor
from llama_index.core.storage.docstore import SimpleDocumentStore
from MetaDataExclusionSetter import MetadataExclusionSetter
from core import settings


def build_ingestion_pipeline(vector_store)->IngestionPipeline:

    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP),
            MetadataExclusionSetter(exclude_llm=["ceo","manager","developer","department"],exclude_embed=["ceo","manager","developer","department"])
        ],
        vector_store=vector_store,
    )

    return pipeline



