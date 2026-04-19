from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
from src.exceptions.path import DirectoryDoesNotExistError, EmptyDirectoryError
from typing import Final, Any
from enum import Enum
import dotenv
import os


class EnumEmbeddingMethods(Enum):
    OLLAMA = OllamaEmbeddings

class EnumVectorStores(Enum):
    CHROMA = Chroma

def initialize_env_var() -> dict[str, str]:
    return dotenv.dotenv_values(".env")

def initialize_embeddings(embedding_method: str, embedding_func_args: dict[str, Any]):
    return EnumEmbeddingMethods[embedding_method].value(**embedding_func_args)

def initialize_vector_store(vector_store_name: str, vector_store_args: dict[str, Any]):
    return EnumVectorStores[vector_store_name].value(**vector_store_args)

def lazy_load_documents(documents_path: str) -> list[Document]:
    if not os.path.isdir(documents_path):
        raise DirectoryDoesNotExistError(documents_path)
    elif not os.listdir(documents_path):
        raise EmptyDirectoryError(documents_path)

    # TODO: iterate through each file in `documents_path` and:
    # TODO: determine file type and instantiate an appropriate loader for each specific file type

    # ! TO BE CONTINUED...

    # Lazy load for large documents
    doc_loader = PyPDFDirectoryLoader(documents_path, mode="page")
    return [doc for doc in doc_loader.lazy_load()]

def main():
    # Initialize environment variables
    ENV: Final[dict[str, str]] = initialize_env_var()
    try:
        # Create Vector Store Embeddings
        embedding_method_str = ENV["EMBEDDING_METHOD"].upper()
        embeddings = initialize_embeddings(
            embedding_method=embedding_method_str,
            embedding_func_args={"model": ENV["EMBEDDING_MODEL"]}
        )

        # Initialize Vector Store
        vector_store_str = ENV["VECTOR_STORE"].upper()

        class EnumVectorStoresArgs(Enum):  # Different vector stores may have different args
            CHROMA = {
                "collection_name": ENV["VECTOR_STORE_COLLECTION_NAME"],
                "persist_directory": f"{ENV["VECTOR_STORE_PERSIST_PATH"]}/{vector_store_str}",
                "embedding_function": embeddings
            }

        vector_store = initialize_vector_store(
            vector_store_name=vector_store_str,
            vector_store_args=EnumVectorStoresArgs[vector_store_str].value
        )

        # Load documents into memory
        documents = lazy_load_documents(ENV["DOCUMENTS_PATH"])
    except KeyError:
        # TODO: implement logging
        print("Oops, something went wrong.")
    except (DirectoryDoesNotExistError, EmptyDirectoryError) as dir_err:
        print(dir_err)

    # Add documents to Vector Store
    ## Check if document is already in Vector Store
    # To be continued...

if __name__ == '__main__':
    main()
