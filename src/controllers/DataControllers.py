from .BaseControllers import BaseControllers
from fastapi import UploadFile
from models import ResponseStatus
class DataController(BaseControllers):
    def __init__(self):
        super().__init__()
        self.size_scaler=1024*1024 # Convert MB to Bytes
    
    def validate_uploaded_file(self,file:UploadFile):
        if file.content_type not in self.settings.FILE_UPLOAD_EXTNSIONS:
            return False,ResponseStatus.FILE_TYPE_NOT_SUPPORTED.value
        if file.size>self.settings.FILE_MAX_SIZE*self.size_scaler:
            return False,ResponseStatus.FILE_SIZE_EXCEEDED.value
        return True,ResponseStatus.FILE_UPLOAD_SUCCESS.value

        