from src.vector_store.main import get_vector_store
from src.document_loader.main import lazy_load_documents
import questionary
from loguru import logger


def query(env: dict[str, str]) -> None:
    question = questionary.text("What would you like to ask?").ask()
    logger.info(f"Question asked: {question}")
    logger.info("Performing similarity search...")
    vector_store = get_vector_store(env)
    sim_search_results = vector_store.similarity_search_with_score(question, k=2)



def index_documents_in_vector_store(env: dict[str, str]) -> None:
    logger.info("Indexing documents in vector store...")
    # Initialize Vector Store and Embeddings
    vector_store = get_vector_store(env)

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
