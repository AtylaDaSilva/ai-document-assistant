from src.environment.variables import initialize_env_var
from src.vector_store.main import get_vector_store
from langchain_core.documents import Document


def test_similarity_search():
    env = initialize_env_var()
    vector_store = get_vector_store(env)
    sim_search_results: list[Document] = vector_store.similarity_search("What is an Aboleth?", k=2)
    assert len(sim_search_results) > 0


def test_similarity_search_with_scores():
    env = initialize_env_var()
    vector_store = get_vector_store(env)
    sim_search_results: list[tuple[Document, float]] = vector_store.similarity_search_with_score("O que é Scrum?", k=2)
    scores: list[str] = []
    for doc, score in sim_search_results:
        scores.append(f"{score:3f}")
    assert len(scores) > 0


def test_similarity_search_with_relevance_scores():
    env = initialize_env_var()
    vector_store = get_vector_store(env)
    sim_search_results: list[tuple[Document, float]] = vector_store.similarity_search_with_relevance_scores("What is an Aboleth?", k=2)
    scores: list[str] = []
    for doc, score in sim_search_results:
        scores.append(f"{score:3f}")
    assert len(scores) > 0
