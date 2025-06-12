from langchain_openai.embeddings import AzureOpenAIEmbeddings
from langchain_chroma import Chroma
from src.utils.load_locations import DOCUMENTS, UUIDS
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

embeddings = AzureOpenAIEmbeddings(model="text-embedding-3-large",
                                  api_version="2024-02-01"
                                  )
# Verify if the data folder exist already
dir_name = "./data"

collection_name = "locations_collection"
chroma_vector_store = Chroma(
    collection_name=collection_name,
    embedding_function=embeddings,
    persist_directory=dir_name
)

# Get the path to data folder
persist_dir = Path(dir_name).resolve()

# Validate if the vector store already contains inside a UUID-named folder
has_uuid_named_folder = any(
    len(child.name) == 36 for child in persist_dir.iterdir() if child.is_dir() or child.is_file()
)

# depending the case generate it or skip the process
if not has_uuid_named_folder:
    logging.info("No folder containing the documents was found. Adding documents to a new vector store.")
    chroma_vector_store.add_documents(documents=DOCUMENTS, id=UUIDS)

# generate a retriever
retriever = chroma_vector_store.as_retriever(search_type="mmr")