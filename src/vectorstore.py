from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from langchain_chroma import Chroma
from src.utils.load_locations import DOCUMENTS
from langchain.indexes import SQLRecordManager, index
from typing import Optional

class ChromaDBVectorStore:
    """
    Utility class that initializes and manages a LangChain-compatible
    vector store using ChromaDB, and indexes documents into it using a specified embedding model.

    It supports the following features:
    - Initializes a persistent Chroma vector store with a specified collection name.
    - Uses AzureOpenAIEmbeddings by default, but allows other langchain embedding models.
    - Supports custom vector store injection for advanced use cases.
    - Tracks document indexing state using SQLRecordManager to avoid re-indexing unchanged documents.
    - Provides a retriever interface for querying the vector store using Maximal Marginal Relevance (MMR).

    Parameters:
        collection_name (str): The name of the Chroma collection (logical group of documents).
        namespace (str): The logical namespace used to separate indexes in the SQL record manager.
        persist_directory (Optional[str]): Directory where ChromaDB will persist data (default: './data').
        embedding_model (Optional[Embeddings]): A custom embedding model; defaults to AzureOpenAIEmbeddings.
        vectorstore (Optional[VectorStore]): An existing vector store instance to reuse instead of creating one.
        db_url (Optional[str]): URL of the SQL database used for tracking indexed documents.

    Methods:
        add_index():
            Indexes the documents defined in DOCUMENTS using the record manager and vector store.
            Returns a retriever object for querying the indexed content.
    """
    def __init__(self,
                 collection_name: str,
                 namespace: str,
                 persist_directory: Optional[str] = "./data",
                 embedding_model: Optional[Embeddings] = None,
                 vectorstore: Optional[VectorStore] = None,
                 db_url: Optional[str] = "sqlite:///record_manager_cache.sql"
                 ):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embedding_model = embedding_model or AzureOpenAIEmbeddings(
            model="text-embedding-3-large",
            api_version="2024-02-01"
        )
        self.vectorstore = vectorstore or Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embedding_model,
            persist_directory=self.persist_directory
        )
        self.namespace = f"{namespace}/{collection_name}" 
        self.db_url = db_url

    def add_index(self):
        record_manager = SQLRecordManager(
            namespace=self.namespace,
            db_url=self.db_url
        )
        record_manager.create_schema()
        print(index(
            DOCUMENTS,
            record_manager,
            self.vectorstore,
            cleanup="incremental",
            source_id_key="source"
        ))
        return self.vectorstore.as_retriever(search_type="mmr")