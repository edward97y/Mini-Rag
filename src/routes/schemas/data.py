from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    file_name:str
    chunk_size: Optional[int] = 100
    overlap: Optional[int] = 20
    do_reset: Optional[bool] = False
