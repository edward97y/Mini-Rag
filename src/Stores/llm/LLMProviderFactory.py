from .LLMenums import ProvidersName
from .Provider.NvidiaProvider import NvidiaProvider

class LLMProviderFactorys:
    def __init__(self,config:dict):
        self.config=config

    def create(self,provider:str):
        if provider == ProvidersName.NVIDIA.value:
       
            return NvidiaProvider(api_key=self.config.NVIDIA_API_KEY,base_url=self.config.NVIDIA_BASE_URL,
                                  model=self.config.NVIDIA_MODEL,default_input_max_characters=self.config.DEFAULT_INPUT_MAX_CHARACTERS,
                                  default_output_max_characters=self.config.DEFAULT_OUTPUT_MAX_CHARACTERS,
                                  default_temperature=self.config.DEFAULT_TEMPERATURE,embed_url=self.config.EMBED_URL)
        return None
