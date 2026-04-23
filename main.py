from src.exceptions.path import DirectoryDoesNotExistError, EmptyDirectoryError
from src.environment.variables import initialize_env_var
from typing import Final
from src.ui import menus
from loguru import logger


def main():
    logger.info("PROCESS START")
    # Initialize environment variables
    env: Final[dict[str, str]] = initialize_env_var()
    try:
        menus.main_menu(env)
    except Exception as err:
        # TODO: implement logging
        print("Unhandled exception caught: ", err)
    except (DirectoryDoesNotExistError, EmptyDirectoryError) as dir_err:
        print(dir_err)

if __name__ == '__main__':
    main()
