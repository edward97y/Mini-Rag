from helpers.config import get_settings
import os
class BaseControllers:
    def __init__(self):
        self.settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.file_dir=os.path.join(self.base_dir,"asserts/files")
        
