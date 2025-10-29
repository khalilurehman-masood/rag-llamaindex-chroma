from llama_index.core import StorageContext
from typing import List, Dict
from core.settings import STORAGE_PATH
from services.get_index_service import get_index, get_storage_context,create_or_get_storage_context_path
from llama_index.core.schema import TextNode
from db.chroma_client import get_vector_db_client
from utils.db_utils import delete_collection_and_dir
from llama_index.core import load_index_from_storage
PRIVILEGED_ROLES={
    # "ceo","admin"
    "xyz"
}

def get_documents_list(role:str,department:str):
    
    # storage_context = get_storage_context(department=department)
    # docstore = storage_context.docstore


    # documents = set()
    # for doc_id, doc in docstore.docs.items():
    #     metadata = doc.metadata or {}

    client = get_vector_db_client()
    collection = client.get_collection(name=department)
    metadatas  = collection.get(
         where={role: "true"},
        include=["metadatas"] 
        ).get("metadatas")
    
    documents = set()
    for metadata in metadatas:

        if (role.lower() in PRIVILEGED_ROLES) or ((metadata.get(role)=="true") and (metadata.get("department"))==department):
                documents.add(metadata["file_name"])
    return documents


def get_chunks_list(role:str, department:str,query:str):
    index = get_index(department=department)
    chunks = index.as_retriever().retrieve(query)
    return chunks


def delete_item(role:str, department:str ,type:str,identifier:str):
    #with role we can inforce that only admin can delete chunks.
    index = get_index(department=department)

    if type=="chunk":
       index.delete_nodes([identifier], delete_from_docstore=True)
       return ("chunks/chunk deleted successfully.")
    
    if type =="document":
        ref_doc_idx = get_ref_doc_idx(department=department,doc_name=identifier)
        doc_idx = get_doc_idx(department=department, doc_name=identifier)
        storage_context = get_storage_context(department=department)
        index = load_index_from_storage(storage_context=storage_context)

        # storage_context  = index.storage_context
        # for doc_id in doc_idx:
        #     index.storage_context.docstore.delete_document(doc_id=doc_id)
        print(f"entries in docstore befor deletion{len(index.storage_context.docstore.docs)}")
        for ref_doc_id in ref_doc_idx:
            index.delete_ref_doc(ref_doc_id, delete_from_docstore=True )

       
            
            
        print(create_or_get_storage_context_path(department=department))
        index.storage_context.persist(create_or_get_storage_context_path(department=department))
        # storage_path = create_or_get_storage_context_path(department=department)
        # storage_context.persist(persist_dir=storage_path)
        print(f"entries in docstore after deletion{len(index.storage_context.docstore.docs)}")

        print("Document Deleted succesfully!")

    if type =="collection":
        result = delete_collection_and_dir(department)
        return result

        




def update_item(role:str, department:str, type:str, identifier:str, text:str):
    # storage_context = StorageContext.from_defaults(persist_dir=STORAGE_PATH)
    # docstore = storage_context.docstore
    # node = TextNode(
    # id_=identifier,
    # text=text
    # )
    index = get_index(department=department)
    storage_context  = index.storage_context
    # index = load_index_from_storage(storage_context=storage_context)
    docstore =storage_context.docstore
    vectorestore =storage_context.vector_store

    

    if type=="chunk":
        node = vectorestore.get_nodes([identifier.strip()])[0]
        print(node.text)
        print(node.ref_doc_id)
        document = docstore.get_document(node.ref_doc_id)
        document.set_content(text)
        print(".....................................................")
        index.refresh_ref_docs([document])
        docstore.add_documents([document], allow_update=True)
        storage_context.persist()

        return ("updated the chunk content successfully")
    
    

      


def get_ref_doc_idx(department:str, doc_name:str):
    client = get_vector_db_client()
    collection = client.get_collection(department)
    metadatas = collection.get(
    where={"file_name": doc_name},
    include=["metadatas"] 
    ).get("metadatas")

    ref_doc_idx = {metadata.get("ref_doc_id") for metadata in metadatas}
    return ref_doc_idx



def get_doc_idx(department:str, doc_name:str):
    client = get_vector_db_client()
    collection = client.get_collection(department)
    metadatas = collection.get(
    where={"file_name": doc_name},
    include=["metadatas"] 
    ).get("metadatas")

    doc_idx = [metadata.get("doc_id") for metadata in metadatas]
    return doc_idx


    