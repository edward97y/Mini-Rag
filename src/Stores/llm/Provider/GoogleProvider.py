from ..LLMinterface import LLMinterface
from google import genai
from ..LLMenums import GOOGLEAIEnum
from google.genai import types
import logging
class GoogleProvider(LLMinterface):
    def __init__(self,api_key:str,stream:bool=False,model:str=None
                 ,default_input_max_characters:int=1000
                 ,default_output_max_characters:int=1000,default_temperature:float=0.1,embed_model:str=None):
        

        self.api_key=api_key
        self.stream=stream
        
 
        self.model=model
        self.embed_model=embed_model

        self.default_input_max_characters=default_input_max_characters
        self.default_output_max_characters=default_output_max_characters
        self.default_temperature=default_temperature
        
        self.generation_model_id=None

        self.embedding_model_id=None
        self.embedding_size=None

        self.client=genai.Client(api_key=self.api_key)
        self.generate_model=None
        self.embed_client=None
        
        self.enums=GOOGLEAIEnum
        self.logger=logging.getLogger(__name__)
    
    def set_generation_model(self, model_id):
        self.generation_model_id=model_id
        self.generate_model= self.client.chats.create(model=self.model)


    def set_embedding_model(self, model_id, embed_size):
        self.embedding_model_id=model_id
        self.embedding_size=embed_size

        

    

    def process_text(self,text:str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt,chat_history, max_output_token=1000, temperature = None):
      
       if not self.generate_model:
            self.logger.error("Google Client was not set")
            return None
       if not self.generation_model_id:
            self.logger.error("Google model was not set")
            return None
       max_output_token=max_output_token if max_output_token else self.default_output_max_characters
       temperature=temperature if temperature else self.default_temperature
       chat_history.append(self.construct_prompt(prompt=prompt,role=GOOGLEAIEnum.USER.value))
       

       
       config = types.GenerateContentConfig(
                max_output_tokens=max_output_token,
                temperature=temperature
            )
            
       response=self.generate_model.send_message(
           message=str(chat_history),
           config = config
            
           
           

       )

       if not response or not response.text or len(response.text)==0 :
           self.logger.error("Error while generate text to user message")
           return None
       
       response = response.text

       chat_history.append(self.construct_prompt(prompt=response,role=GOOGLEAIEnum.MODEL.value))
       return response

    
    def embed_text(self, text, document_type=None):
        self.embed_client=self.client.models
       
        if not self.embed_client:
            self.logger.error("Google embed Client was not set")
            return None
        if not self.embedding_model_id:
            self.logger.error("Google Embedding model was not set")
            return None
        response = self.embed_client.embed_content(
                model=self.embed_model,
                contents=text,
                config=types.EmbedContentConfig(output_dimensionality=self.embedding_size) if self.embedding_size else None
            )

        if not response or not response.embeddings or len(response.embeddings)==0:
            self.logger.error("Error while embedding the text")
            return None
        
        return response.embeddings[0].values
    
    def construct_prompt(self, prompt, role):
        
        return {
            "role": role, 
            "parts": [{"text": self.process_text(prompt)}]
        }

    

