import langchain_community.document_loaders as lc_doc_loader
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
from src.exceptions.path import DirectoryDoesNotExistError, EmptyDirectoryError
from typing import Final, Any
from enum import Enum
import dotenv
import os
from pathlib import Path


class EnumFileLoaders(Enum):
    """Loaders for supported file types"""
    PDF = lc_doc_loader.PyPDFLoader
    CSV = lc_doc_loader.CSVLoader  # TODO: test loader
    JSON = lc_doc_loader.JSONLoader  # TODO: test loader
    HTML = lc_doc_loader.BSHTMLLoader  # TODO: test loader


def get_file_loader(file: Path) -> lc_doc_loader.BaseLoader:
    file_ext = file.suffix.replace(".", "").upper()
    return EnumFileLoaders[file_ext]


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
    """
    Lazy-loads documents into memory and returns a list of *Document* objects.
    See *EnumFileLoaders* for supported file types.
    :param documents_path: The directory to load documents from.
    :return: List of Document objects.
    """
    if not os.path.isdir(documents_path):
        raise DirectoryDoesNotExistError(documents_path)

    dir_items: list[str] = os.listdir(documents_path)

    if not dir_items:
        raise EmptyDirectoryError(documents_path)

    docs: list[Document] = []  # Each page of a file is treated as a document
    for file_name in dir_items:
        # Get file-appropriate loader
        file = Path(file_name)
        loader_enum = get_file_loader(file)
        doc_loader: lc_doc_loader.BaseLoader = loader_enum.value(f"{documents_path}/{file.name}")
        # Load docs
        for page in doc_loader.lazy_load():  # Lazy load works better for large documents
            docs.append(page)

    return docs

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
        # ! TO BE CONTINUED...
        # Index and add documents to vector store (check if already exists in storage)
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
