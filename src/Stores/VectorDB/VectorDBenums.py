from enum import Enum

class VectorDB(Enum):
    QDRANT="QDRANT"

class DistanceMethodenum(Enum):
    COSINE="cosine"
    DOT="dot"