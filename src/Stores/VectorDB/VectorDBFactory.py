from VectorDBenums import VectorDB
from .Provider import QdrantDB
from controllers.BaseController import BaseController
class DataBaseFactory():
    def __init__(self,config):

        self.config=config

        self.base_controller=BaseController
        
    def create_connection_with_db(self,DataBaseName:str):
        if VectorDB.QDRANT.value==DataBaseName:
            return QdrantDB(db_path=self.config.DB_PATH,distance_method=self.config.DISTANCE_DataBase_Matrix)
        
        return None





