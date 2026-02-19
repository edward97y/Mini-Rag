from .LLMenums import ProvidersName
from .Provider import NvidiaProvider, CoHereProvider,GoogleProvider

class LLMProviderFactorys:
    def __init__(self,config:dict):
        self.config=config

    def create(self,provider:str):
        if provider == ProvidersName.NVIDIA.value:
       
            return NvidiaProvider(api_key=self.config.NVIDIA_API_KEY,base_url=self.config.NVIDIA_BASE_URL,
                                  model=self.config.NVIDIA_MODEL,default_input_max_characters=self.config.DEFAULT_INPUT_MAX_CHARACTERS,
                                  default_output_max_characters=self.config.DEFAULT_OUTPUT_MAX_CHARACTERS,
                                  default_temperature=self.config.DEFAULT_TEMPERATURE,embed_url=self.config.EMBED_URL)
        if provider == ProvidersName.GOOGLE.value:
           
            return GoogleProvider(api_key=self.config.GEMINI_API_KEY,model=self.config.GOOGLE_GENERATE_MODEL,
                                  default_input_max_characters=self.config.DEFAULT_INPUT_MAX_CHARACTERS,
                                  default_output_max_characters=self.config.DEFAULT_OUTPUT_MAX_CHARACTERS,
                                  default_temperature=self.config.DEFAULT_TEMPERATURE,embed_model=self.config.GOOGLE_EMBED_MODEL)
        if provider == ProvidersName.COHERE.value:
            return CoHereProvider(
                api_key = self.config.COHERE_API_KEY,
                default_input_max_characters=self.config.DEFAULT_INPUT_MAX_CHARACTERS,
                default_generation_max_output_tokens=self.config.DEFAULT_OUTPUT_MAX_CHARACTERS,
                default_generation_temperature=self.config.DEFAULT_TEMPERATURE
            )
        
        return None
