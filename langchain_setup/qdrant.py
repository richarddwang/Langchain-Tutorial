from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import Qdrant

from . import pprint_documents


def create_inmemory_empty_qdrant(**from_texts_kwargs):
    return create_empty_qdrant(
        location=":memory:", embedding=OpenAIEmbeddings(), **from_texts_kwargs
    )


def create_empty_qdrant(**from_texts_kwargs):
    # Qdrant requires vector size, which can be only know after applying embedder
    vectorstore = Qdrant.from_texts(["dummy"], **from_texts_kwargs)
    dummy_document_id = vectorstore.client.scroll(vectorstore.collection_name)[0][0].id
    vectorstore.delete([dummy_document_id])
    return vectorstore


def pprint_qdrant_documents(vectorstore, limit: int = 100, **scroll_kwargs):
    document_ids, documents = [], []
    for record in vectorstore.client.scroll(
        vectorstore.collection_name, limit=100, **scroll_kwargs
    )[0]:
        document_ids.append(record.id)
        documents.append(
            Document(
                page_content=record.payload["page_content"],
                metadata=record.payload["metadata"] or {},
            )
        )
    pprint_documents(documents, document_ids=document_ids)
