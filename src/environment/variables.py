import dotenv


def initialize_env_var() -> dict[str, str]:
    return dotenv.dotenv_values(".env")
