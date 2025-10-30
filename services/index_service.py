from pathlib import Path
from core.settings import llm, embed_model, ollama_ef
from core.settings import CHROMA_PATH, STORAGE_PATH
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, settings,StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from llama_index.core import load_index_from_storage
from db.chroma_client import get_vector_db_client
from services.ingest_service import build_ingestion_pipeline
from services.get_index_service import get_storage_context, get_index ,create_or_get_storage_context_path
from llama_index.core import Document
from llama_index.core.schema import TextNode
import json, hashlib

def compute_node_hash(node:TextNode):
    text = node.text
    meta = json.dumps(node.metadata, sort_keys=True)
    node_hash = hashlib.sha256((text + meta).encode("utf-8")).hexdigest()
    node.metadata['hash'] = node_hash
    return node


def get_nodes_to_insert(new_nodes:list[TextNode], collection):
   
    file_name = new_nodes[0].metadata["file_name"]
    print(f":::::::::::::::::::::::::::::::::{file_name}")
    old_nodes_metadatas = collection.get(where={"file_name": file_name},include=["metadatas"]).get("metadatas")
    # print(old_nodes_metadatas[400])
   

    nodes_to_insert, nodes_ids_to_delete = diff_nodes_by_hash(new_nodes, old_nodes_metadatas)

    

   
    return (nodes_to_insert, nodes_ids_to_delete)





def diff_nodes_by_hash(new_nodes: list[TextNode], old_nodes_metadatas: list[dict]):
    """
    Determine which nodes to insert or delete based on hash differences.
    new_nodes: list of TextNodes (with .metadata["hash"])
    old_nodes: dict returned from Chroma collection.get(where={"file_name": ...}), the dicts contain metadata for each node.
    Logic from sets theory is used to determin insertion and deletion nodes.
    """
    print(f"len of olde nodes metadas: {len(old_nodes_metadatas)}")

    #creating two dicts as {"hash":"id"} one for old_nodes and one for new_nodes to be used after filtering for remaping hashes to ids  
    old_hash_to_id={metadata["hash"]:json.loads(metadata["_node_content"])["id_"] for metadata in old_nodes_metadatas if "hash" in metadata and "_node_content" in metadata}
    # print(f"len of olde nodes: {len(old_hash_to_id)}")
    # print(list(old_hash_to_id.items())[155])
    new_hash_to_id={node.metadata["hash"]:node.id_ for node in new_nodes}
    # print(list(new_hash_to_id.items())[65])

    #now we will create sets of hashes for both old and new nodes
    old_hash_set = set(old_hash_to_id.keys())
    new_hash_set = set(new_hash_to_id.keys())

    print(f"len of old_hash_set:{len(old_hash_set)}")
    print(f"len of new_hash_set:{len(new_hash_set)}")

    #now we will perform Set operations on the sets of hashes, to figureout the exact nodes for deletion and insersion.

    # union = old_hash_set.union(new_hash_set)  # this will return union of both the sets - all nodes in a single set
    intersection = old_hash_set.intersection(new_hash_set)  #this will return nodes that are in both the sets (old and new).
    nodes_hash_to_index = new_hash_set.difference(intersection)  #can't explain here but it works, hehe!
    nodes_hash_to_delete = old_hash_set.difference(new_hash_set)  

    #now we have the sets to be inseted and to be deleted we will get the ids for both.

    node_ids_to_insert = [id for hash,id in new_hash_to_id.items() if hash in nodes_hash_to_index]
    node_ids_to_delete = [id for hash,id in old_hash_to_id.items() if hash in nodes_hash_to_delete]

    #create a list of the nodes to be inserted from the using the ids
    nodes_to_insert = [node for node in new_nodes if node.id_ in node_ids_to_insert]

    print(f"length of nodes to be inserted{len(node_ids_to_insert)}  & lenght of nodes to be deleted: {len(node_ids_to_delete)}")

    



    return nodes_to_insert, node_ids_to_delete

            

async def index_user_file(user_name:str, department:str, roles:list[str], user_dir: str, file_path:str) -> dict:
    print(f"All roles recieved{roles}")
    def set_document_metadata(file_path:Path):
  
        meta_data = {}
        for role in roles:
            meta_data[role.lower()]="true"
        meta_data['department']=department.lower().strip()

        return meta_data
    Path(CHROMA_PATH).mkdir(parents=True, exist_ok=True)


    # user_dir = Path(user_dir)
    docs = SimpleDirectoryReader(input_files=[file_path], file_metadata=set_document_metadata, filename_as_id=True).load_data()

    vector_client = get_vector_db_client()

    try:
        collection = vector_client.get_collection(department)
        vector_store = ChromaVectorStore(chroma_collection=collection)       
        index = VectorStoreIndex.from_vector_store(vector_store = vector_store, embed_model=embed_model)
        
    


    except Exception as e:
        print("Collection not found, creating new one.")
        collection = vector_client.create_collection(department, embedding_function=ollama_ef)
        vector_store = ChromaVectorStore(chroma_collection=collection)
        print("storage context recieved")
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    
        

    ingestion_pipeline = build_ingestion_pipeline(vector_store)
    
    print(".................before pipeline.run().....................")
    nodes = ingestion_pipeline.run(documents=docs)
    nodes_with_hash = [compute_node_hash(node) for node in nodes]
    nodes_to_insert, nodes_ids_to_delete = get_nodes_to_insert(new_nodes=nodes_with_hash, collection = collection)
    print(".................after pipeline.run().....................")
    print(len(nodes_to_insert))
    print(len(nodes_ids_to_delete))
    index.insert_nodes(nodes_to_insert)
    if nodes_ids_to_delete:
        index.delete_nodes(nodes_ids_to_delete)


   

    return {
        "message":"File indexed successfully for user"     
        }




