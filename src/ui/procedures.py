from src.vector_store.main import get_vector_store, filter_sim_search_by_relevance_score
from src.document_loader.main import lazy_load_documents
from langchain_core.documents import Document
from src.utils import yaml
import questionary
from loguru import logger


def query(env: dict[str, str]) -> None:
    question = questionary.text("What would you like to ask?").ask()
    logger.info(f"Question asked: {question}")

    results_count = int(env["SIMILARITY_SEARCH_RESULTS_COUNT"])
    relevance_score_cutoff = float(env["SIMILARITY_SEARCH_RELEVANCE_CUTOFF"])
    logger.info(f"Performing similarity search (K={results_count}, Relevance cutoff={relevance_score_cutoff})...")

    # Search vector store for relevant results
    vector_store = get_vector_store(env)
    sim_search_results: list[tuple[Document, float]] = filter_sim_search_by_relevance_score(
        vector_store.similarity_search_with_relevance_scores(question, k=results_count),
        relevance_score=relevance_score_cutoff,
    )

    # Create LLM message template
    query_context = "\n\n---\n\n".join([doc.page_content for doc, score in sim_search_results])
    directives = yaml.parse_yaml("./directives.yaml")
    # ! TO BE CONTINUED...



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
