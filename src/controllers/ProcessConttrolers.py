import os
from .BaseControllers import BaseControllers
from .Projectcontrollers import ProjectController
from langchain_community.document_loaders import TextLoader,PyMuPDFLoader
from models import Processing_ext
from langchain_text_splitters import RecursiveCharacterTextSplitter
class ProcessController(BaseControllers):
    def __init__(self,project_id:str):
        super().__init__()
        self.project_id=project_id
        self.project_path=ProjectController().get_project_path(project_id=project_id)
    
    def get_file_extension(self,file_name:str):
        return file_name.split(".")[-1]
    
    def get_loader_for_file(self,file_name:str):
        ext=self.get_file_extension(file_name=file_name)
        file_path=os.path.join(self.project_path,file_name)
        if ext == Processing_ext.TXT.value:
            return TextLoader(file_path=file_path)
        elif ext == Processing_ext.PDF.value:
            return PyMuPDFLoader(file_path=file_path)
        else:
            return None
        
    def get_file_content(self,file_name:str):
        loader=self.get_loader_for_file(file_name=file_name)

        return loader.load()
    def process_file_content(self,file_content:list,file_name:str,chunk_size:int,overlap:int):
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=overlap)

        file_content_text=[rec.page_content for rec in file_content]

        file_content_metadata=[rec.metadata for rec in file_content]

        chunks=text_splitter.create_documents(file_content_text,metadatas=file_content_metadata)
        return chunks
    
