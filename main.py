from enum import Enum, StrEnum
import dotenv
from typing import Final, Any
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma


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

def load_documents():
    pass

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

        # Specific Args for different Vector Stores
        class EnumVectorStoresArgs(Enum):
            CHROMA = {
                "collection_name": ENV["VECTOR_STORE_COLLECTION_NAME"],
                "persist_directory": ENV["VECTOR_STORE_PERSIST_PATH"],
                "embedding_function": embeddings
            }

        # Initialize Vector Store
        vector_store_str = ENV["VECTOR_STORE"].upper()
        vector_store = initialize_vector_store(
            vector_store_name=vector_store_str,
            vector_store_args=EnumVectorStoresArgs[vector_store_str].value
        )

        # ! TO BE CONTINUED...
    except KeyError:
        # TODO: implement logging
        print("Oops, something went wrong.")
        return

    # Load documents into memory
    # Add documents to Vector Store
    ## Check if document is already in Vector Store
    # To be continued...

    pass

if __name__ == '__main__':
    main()
