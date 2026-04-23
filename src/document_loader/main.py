from src.exceptions.path import DirectoryDoesNotExistError, EmptyDirectoryError
import langchain_community.document_loaders as lc_doc_loader
from langchain_core.documents import Document
from pathlib import Path
from enum import Enum
import os


class EnumDocLoader(Enum):
    """Loaders for supported file types"""
    PDF = lc_doc_loader.PyPDFLoader
    CSV = lc_doc_loader.CSVLoader  # TODO: test loader
    JSON = lc_doc_loader.JSONLoader  # TODO: test loader
    HTML = lc_doc_loader.BSHTMLLoader  # TODO: test loader


def get_document_loader(file: Path) -> lc_doc_loader.BaseLoader:
    file_ext = file.suffix.replace(".", "").upper()
    return EnumDocLoader[file_ext]


def lazy_load_documents(documents_path: str) -> list[Document]:
    """
    Lazy-loads documents into memory and returns a list of *Document* objects.
    See *EnumFileLoaders* for supported file types.
    :param documents_path: The directory to load documents from.
    :return: List of Document objects.
    """
    if not os.path.isdir(documents_path):
        raise DirectoryDoesNotExistError(documents_path)

    dir_items: list[str] = os.listdir(documents_path)

    if not dir_items:
        raise EmptyDirectoryError(documents_path)

    docs: list[Document] = []  # Each page of a file is treated as a document
    for file_name in dir_items:
        # Get file-appropriate loader
        file = Path(file_name)
        loader_enum = get_document_loader(file)
        doc_loader: lc_doc_loader.BaseLoader = loader_enum.value(f"{documents_path}/{file.name}")
        # Load docs
        for page in doc_loader.lazy_load():  # Lazy load works better for large documents
            docs.append(page)

    return docs