from enum import Enum
from langchain_ollama import ChatOllama


class ChatModels(Enum):
    OLLAMA = ChatOllama
