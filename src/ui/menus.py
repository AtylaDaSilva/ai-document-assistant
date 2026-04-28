from src.ui.procedures import query, index_documents_in_vector_store, purge_vector_store, quit_program, test_log_sinks
from typing import Final
from collections.abc import Callable
from questionary import Choice, select, Separator


MAIN_MENU_MSG: Final[str] = "Welcome to your document assistant. What would you like to do?"

MAIN_MENU_CHOICES: list[Choice] = [
    Choice(
        title="Query", value=query
    ),
    Choice(
        title="Index Documents in Vector Store", value=index_documents_in_vector_store
    ),
    Choice(
        title="Purge Vector Store", value=purge_vector_store
    ),
    Choice(
        title="Quit", value=quit_program
    )
]

def main_menu(env: dict[str, str]):
    dev_mode = bool(int(env["DEVELOPER_MODE"]))
    # Dev mode menu options
    if dev_mode:
        MAIN_MENU_CHOICES.extend([
            Separator(line="============ Developer Options ============"),
            Choice(
                title="[DEV] Log Sink Test", value=test_log_sinks
            )
        ])
    # Main menu loop
    while True:
        fn_choice: Callable[[dict[str, str]], None] = select(MAIN_MENU_MSG, MAIN_MENU_CHOICES).ask()
        fn_choice(env)