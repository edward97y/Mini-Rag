from ..VectorDBinterface import VectorDBinterface
from qdrant_client import models,QdrantClient
from qdrant_client.models import VectorParams,PointStruct
from typing import List
from ..VectorDBenums import DistanceMethodenum
import logging

class QdrantDB(VectorDBinterface):
    def __init__(self,db_path:str,distance_method:str)->None:

        self.db_path=db_path
        self.distance_method=None

        self.client=None

        if distance_method==DistanceMethodenum.COSINE.value:

            self.distance_method=models.Distance.COSINE


        elif distance_method==DistanceMethodenum.DOT:
            self.distance_method=models.Distance.DOT

        self.logger=logging.getLogger(__name__)

    def connect(self):
        self.client=QdrantClient(path=self.db_path)

    def disconnect(self):
        self.client=None
    
    def is_collection_existed(self, collection_name)->bool:
        return self.client.collection_exists(collection_name=collection_name)
    
    def list_all_collections(self)->List:

        return self.client.get_collections()
       
    def list_collections_info(self, collection_name):
        return self.client.create_collection(collection_name=collection_name)
    
    def delete_collection(self, collection_name):
         if self.client.collection_exists(collection_name=collection_name):
            self.client.delete_collection(collection_name=collection_name)

    
    def create_collection(self, collection_name, embed_size, do_reset = False):
        if do_reset:

            _ = self.delete_collection(collection_name=collection_name)
        if not self.is_collection_existed(collection_name=collection_name):
            _ = self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=embed_size, distance=self.distance_method),
         )
            return True
        return False
    
    def insert_one(self, collection_name, text, vector, metadata = None, record_id = None):
        if not self.is_collection_existed(collection_name=collection_name):
            self.logger.error(f"cannot insert new record into non-existed collection{collection_name}")
            return False
        point=PointStruct(
        vector=vector,
        payload={"text":text,"metadata":metadata}
    )
        try:
            _ = self.client.upsert(
            collection_name=collection_name,points=point)
        except Exception as e:
            self.logger.error(f"error while insert one record :{e}")
            return False
        return True
        
    


    def insert_many(self, collection_name, text, vector, metadata = None, record_id = None, batch_size = 50):
        if metadata is None:
            metadata=[None]*len(text)
        if record_id is None:
            record_id=[record_id]*len(text)

        for i in range(0,len(text),batch_size):
            batch_end=i+batch_size

            batch_text=text[i:batch_end]
            batch_vector=vector[i:batch_end]
            batch_metadata=metadata[i:batch_end]

            batch_point=[
                PointStruct(vector=batch_vector[x],payload={"text":batch_text[x],"metadata":batch_metadata[x]})
                
                for x in range(len(batch_text))
                ]
            try:
                _ = self.client.upsert(
                collection_name=collection_name,points=batch_point)
            except Exception as e:
                self.logger.error(f"error while inserting batch :{e}")
                return False

        return True

    
    def search_by_vector(self, collection_name, vector, limit=5):
        return self.client.query_points(collection_name=collection_name,query=vector,limit=limit)
    
