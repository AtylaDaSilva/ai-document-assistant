from src.exceptions.path import DirectoryDoesNotExistError, EmptyDirectoryError
from src.environment.variables import initialize_env_var
from src.logging.procedures import initialize_log_sinks
from typing import Final
from src.ui import menus
from loguru import logger


def main():
    try:
        # Environment variables
        env: Final[dict[str, str]] = initialize_env_var()
        # Log sinks
        initialize_log_sinks(env)
        logger.info("PROCESS START")
        # Main menu
        menus.main_menu(env)
    except Exception as err:
        logger.critical(f"Unhandled exception caught: {err}")
    except (DirectoryDoesNotExistError, EmptyDirectoryError) as dir_err:
        print(dir_err)

if __name__ == '__main__':
    main()
