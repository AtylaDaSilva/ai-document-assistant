from src.ui.procedures import query, index_documents_in_vector_store, purge_vector_store, quit_program
from typing import Final
from collections.abc import Callable
from questionary import Choice, select


MAIN_MENU_MSG: Final[str] = "Welcome to your document assistant. What would you like to do?"

MAIN_MENU_CHOICES: Final[list[Choice]] = [
    Choice(
        title="Query", value=query
    ),
    Choice(
        title="Index documents into vector store", value=index_documents_in_vector_store
    ),
    Choice(
        title="Purge vector store", value=purge_vector_store
    ),
    Choice(
        title="Quit", value=quit_program
    )
]

def main_menu(env: dict[str, str]):
    while True:
        fn_choice: Callable[[dict[str, str]], None] = select(MAIN_MENU_MSG, MAIN_MENU_CHOICES).ask()
        fn_choice(env)