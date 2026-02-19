from enum import Enum

class LLMenumeration(Enum):

    NVIDIA="NVIDIA"
    GOOGLE="GOOGLE"
class OpenAIEnum(Enum):
    SYSTEM="system"
    USER="user"
    ASSISTANT="assistant"
class GOOGLEAIEnum(Enum):
    SYSTEM="system"
    USER="user"
    MODEL="model"
class ProvidersName(Enum):
    NVIDIA="nvidia"
    GOOGLE="google"
    COHERE="cohere"

class DocumentTypeEnum(Enum):
    DOCUMENT="document"
    QUERY="query"
class CoHereEnums(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "CHATBOT"

    DOCUMENT = "search_document"
    QUERY = "search_query"


    