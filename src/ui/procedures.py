from src.vector_store.main import initialize_vector_store_embeddings, initialize_vector_store
from src.document_loader.main import lazy_load_documents
from loguru import logger


def query(env: dict[str, str]) -> None:
    print("Quering...")


def index_documents_in_vector_store(env: dict[str, str]) -> None:
    logger.info("Indexing documents in vector store...")
    # Initialize Vector Store Embeddings
    vector_store_embeddings = initialize_vector_store_embeddings(env)

    # Initialize Vector Store
    vector_store = initialize_vector_store(env, vector_store_embeddings)

    # Load documents into memory
    documents = lazy_load_documents(env["DOCUMENTS_PATH"])

    # Add documents to vector store
    logger.info("Adding documents to vector store...")
    vector_store.add_documents(documents)

    # Success
    logger.success("Successfully indexed documents in vector store.")


def purge_vector_store(env: dict[str, str]) -> None:
    print("Purging...")


def quit_program(env: dict[str, str]) -> None:
    print("Goodbye!")
    logger.info("PROCESS END")
    exit(0)
