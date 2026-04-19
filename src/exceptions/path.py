class DirectoryDoesNotExistError(Exception):
    def __init__(self, dir_path: str):
        super().__init__(f"Directory '{dir_path}' does not exist")


class EmptyDirectoryError(Exception):
    def __init__(self, dir_path: str):
        super().__init__(f"Directory '{dir_path}' is empty")