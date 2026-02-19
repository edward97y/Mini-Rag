from .BaseController import BaseController
from models.db_schemes import Project,DataChunk
from Stores.llm.LLMenums import DocumentTypeEnum

from typing import List
import json
class NLPController(BaseController):
    def __init__(self,vector_db_client,generation_client,embed_client,template_parser):
        super().__init__()
        self.vector_db_client=vector_db_client
        self.generation_client=generation_client
        self.embed_client=embed_client
        self.template_parser=template_parser
        

    def create_collection_name(self,project_id:str):
        return f"collection_{project_id}".strip()
    
    def reset_vector_db_collection(self,project:Project):
        
        collection_name=self.create_collection_name(project_id=project.project_id)

        return self.vector_db_client.delete_collection(collection_name=collection_name)
    
    def get_vector_db_collection(self,project:Project):
        collection_name=self.create_collection_name(project_id=project.project_id)
        collection_info= self.vector_db_client.list_collections_info(collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info,default=lambda x:x.__dict__)
        )
    
    def index_into_vector_db(self,project:Project,chunks:List[DataChunk],chunks_ids: List[int]
                             ,do_reset:bool=False):
        #get collection name
        collection_name=self.create_collection_name(project_id=project.project_id)

        #mange item
        texts=[
            c.chunk_text for c in chunks
        ]
        vector=[
           self.embed_client.embed_text(text=text,document_type=DocumentTypeEnum.DOCUMENT.value) for text in texts
        ]
        metadata=[
            c.chunk_metadata for c in chunks
        ]
      

        #create collection if not exist
        _=self.vector_db_client.create_collection(collection_name=collection_name,
                                                   embed_size=self.app_settings.EMBED_SIZE, do_reset = do_reset)

        #insert into vector db
        _=self.vector_db_client.insert_many(collection_name=collection_name,
                                            text=texts,vector=vector,metadata=metadata,record_id=chunks_ids)
        return True
    def search_vector_db_collection(self,project:Project,text:str,limit:int=5):
        #get collection name
        collection_name=self.create_collection_name(project_id=project.project_id)

        #get text embed
        embed_text=self.embed_client.embed_text(text=text,document_type=DocumentTypeEnum.DOCUMENT.value)

        # use semantic search
        result=self.vector_db_client.search_by_vector(collection_name=collection_name,vector=embed_text, limit=limit)

        return result
    
    def answer_rag_question(self,project:Project,query:str,limit:int=5):
        answer,full_prompt,chat_history=None,None,None
        #retrieve related docs
        retrieve_documents=self.search_vector_db_collection(project=project,text=query,limit=limit)
        retrieve_documents=retrieve_documents.points 
        if not retrieve_documents:
            return None,None,None
        
        #construct prompt
        system_prompt=self.template_parser.get("rag","system_prompt")
        
        document_prompts="\n".join([
            self.template_parser.get("rag","document_prompt",
                                     {"doc_num":idx+1,"chunk_text":doc.payload["text"],}) 
                                     for idx,doc in enumerate(retrieve_documents)
            ])
    
        footer_prompt=self.template_parser.get("rag","footer_prompt",{"query":query})

        chat_history=[
            self.generation_client.construct_prompt(prompt=system_prompt,role=self.generation_client.enums.SYSTEM.value)

        ]
        full_prompt="\n\n".join([document_prompts,footer_prompt])
        answer=self.generation_client.generate_text(prompt=full_prompt,chat_history=chat_history)
        return answer,full_prompt,chat_history

       