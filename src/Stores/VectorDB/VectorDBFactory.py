from .VectorDBenums import VectorDB
from .Provider import QdrantDB
from controllers.BaseController import BaseController
class DataBaseFactory():
    def __init__(self,config):

        self.config=config

        
        
    def create_connection_with_db(self,DataBaseName:str):
        if VectorDB.QDRANT.value==DataBaseName:
            base_controller=BaseController()
            db_path=base_controller.get_database_path(db_name=self.config.DB_PATH)
            
            return QdrantDB(db_path=db_path,distance_method=self.config.DISTANCE_DataBase_Matrix)
        
        return None





