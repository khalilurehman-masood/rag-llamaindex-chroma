
from db.chroma_client import get_vector_db_client
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.llms import ChatMessage
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.chat_engine import ContextChatEngine, CondensePlusContextChatEngine,SimpleChatEngine
from llama_index.core import get_response_synthesizer
from core.settings import llm,embed_model, CHROMA_PATH, FETCH_K
from services.memory_service import get_memory
from services.get_index_service import get_index
from llama_index.core.retrievers import VectorIndexRetriever, RecursiveRetriever
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.vector_stores import (MetadataFilter, MetadataFilters, FilterOperator)
async def query_user_file(user_name:str, query:str):
    memory = get_memory(user_name, "abcd")

    index = get_index(user_name)
    
    # chat_engine = index.as_chat_engine(llm=llm, chat_mode="condense_plus_context",memory = memory, system_prompt=("you are a helpful assistant that can answer general questions as well as quetions asked from the provided context. Please be concise."))
    chat_engine = build_chat_engine(index,llm=llm,memory= memory)
    print("befor invoking..........")
    # response =await chat_engine.achat(query)
    response = await chat_engine.achat(query)

    print("after invoking engine")
    return {
        "response":response.response,
        "number of retrieved nodes":len(response.sources[0].raw_output),
        "scores of retrieved nodes":[node.score for node in response.sources[0].raw_output],
        "page labels for retrieved nodes":[node.node.extra_info['page_label'] for node in response.sources[0].raw_output],
        "File names for the retrieved nodes":[node.node.extra_info['file_name'] for node in response.sources[0].raw_output],
        "Text of the node":[node.text for node in response.sources[0].raw_output],
        "just a seperator":"_"*100,
        "sources":response
        # "sources":[n.metadata for n in response.source_nodes],
    }


def build_chat_engine(index:VectorStoreIndex, llm, memory=None)-> ContextChatEngine:
    

    filters = MetadataFilters(
        filters=[
            MetadataFilter(
                key="file_name",value="ICD-10-CM FY25 Guidelines October 1, 2024 (1).pdf",operator=FilterOperator.EQ
            )
        ]
    )


    retriever = VectorIndexRetriever(index=index, similarity_top_k=10)

    #define node postprocessors here
    node_postprocessors = [SimilarityPostprocessor(similarity_cutoff=0.3)]

  

    engine =CondensePlusContextChatEngine(
        llm= llm,
        memory = memory,
        retriever=retriever,
        # node_postprocessors = node_postprocessors,
        system_prompt=(
            "You are a helpful assistant that answers both general and context-based "
            "questions from the provided documents. Please be concise."
        ),
        

    )

    return engine

