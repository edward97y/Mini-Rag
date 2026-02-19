from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "file_validate_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    PROCESSING_SUCCESS = "processing_success"
    FILE_ID_ERROR="file id error"
    NO_FILES_ERROR="not found files"
    PROCESSING_FAILED = "processing_failed"
    PROJECT_NOT_FOUND_ERROR="project not found"
    INSERT_INTO_VECTOR_DB_ERROR="failed to insert into vector db"
    INSERT_INTO_VECTOR_DB_SUCCESS="insert into vector db success"
    VECTOR_COLLECTION_RETRIVED="vector collection retrieved"
    VECTOR_DB_SEARCH_ERROR="vector search error"
    VECTOR_DB_SEARCH_SUCCESS="vector search SUCCESS"
    RAG_ANSWER_ERROR="rag answer failed"
    RAG_ANSWER_SUCCESS="rag answer SUCCESS"

