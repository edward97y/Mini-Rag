from pydantic import BaseModel, Field
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):

    _id: Optional[ObjectId] 
    file_name:str=Field(...,min_length=1)
    chunk_project_id:str=Field(...,min_length=1)
    chunk_index:int=Field(...,ge=0)
    chunk_text:str=Field(...,min_length=1)
    chunk_metadata:dict

    class Config:
        arbitrary_types_allowed = True