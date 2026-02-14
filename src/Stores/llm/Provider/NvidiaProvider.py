from ..LLMinterface import LLMinterface
from ..LLMenums import OpenAIEnum
from openai import OpenAI

import logging


class NvidiaProvider(LLMinterface):
    
    def __init__(self,api_key:str,stream:bool=False,base_url:str=None,model:str=None
                 ,default_input_max_characters:int=1000
                 ,default_output_max_characters:int=1000,default_temperature:float=0.2,embed_url:str=None):
        

        self.api_key=api_key
        self.stream=stream
        self.base_url=base_url
        self.model=model
        self.embed_url=embed_url

        self.default_input_max_characters=default_input_max_characters
        self.default_output_max_characters=default_output_max_characters
        self.default_temperature=default_temperature
        
        self.generation_model_id=None

        self.embedding_model_id=None
        self.embedding_size=None

        self.client=OpenAI(base_url=self.base_url,api_key=self.api_key)
        self.embed_client=OpenAI(base_url=self.embed_url,api_key="anything")
        
        self.logger=logging.getLogger(__name__)

    def set_generation_model(self, model_id):
        self.generation_model_id=model_id


    def set_embedding_model(self, model_id, embed_size):
        self.embedding_model_id=model_id
        self.embedding_size=embed_size
    

    def process_text(self,text:str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt,chat_history, max_output_token, temperature = None):
       
       if not self.client:
            self.logger.error("Nvidia Client was not set")
            return None
       if not self.generation_model_id:
            self.logger.error("Nvidia model was not set")
            return None
       max_output_token=max_output_token if max_output_token else self.default_output_max_characters
       temperature=temperature if temperature else self.default_temperature
       chat_history.append(self.construct_prompt(prompt=prompt,role=OpenAIEnum.USER.value))

       
       response=self.client.chat.completions.create(
           model=self.model,
           messages=chat_history,
           max_tokens=max_output_token,
           temperature=temperature,
           

       )

       if not response or not response.choices or len(response.choices)==0 or not response.choices[0].message:
           self.logger.error("Error while generate text to user message")
           return None
       
       response = response.choices[0].message["content"]

       chat_history.append(self.construct_prompt(prompt=response,role=OpenAIEnum.ASSISTANT.value))
       return response

    
    def embed_text(self, text, document_type=None):
        
        if not self.embed_client:
            self.logger.error("embed Client was not set")
            return None
        if not self.embedding_model_id:
            self.logger.error("Embedding model was not set")
            return None
        response= self.embed_client.embeddings.create(model=self.embedding_model_id,input=text)

        if not response or not response.data or len(response.data)==0 or not response.data[0].embedding:
            self.logger.error("Error while embedding the text")
            return None
        
        return response.data[0].embedding
    
    def construct_prompt(self, prompt, role):
        
        return {"role":role,"content":self.process_text(prompt)}

        
    
    
