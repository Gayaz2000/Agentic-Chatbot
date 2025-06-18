import yaml
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class Load_Config:
    def __init__(self, config_path: str = r"configfiles\configs.yaml"):
        self.config_path = config_path

    def load_config(self):
        """Loads all the configuration"""
        with open(self.config_path, "r") as file:
            self.config = yaml.safe_load(file)
        return self.config


class Config(Load_Config):
    def __init__(self):
        super().__init__() 
        self.config = self.load_config()

    def get_llm_options(self):
        """Takes llm options from the config"""
        self.config = self.load_config()
        return self.config["model_options"]["Groq_model_options"]
    
    def get_usecase_options(self):
        """Takes usecase options from the config"""
        self.config = self.load_config()
        return self.config["chat_options"]["usecase_options"]
    
    def get_groq_model_options(self):
        """Takes provider options from the config"""
        self.config = self.load_config()
        return self.config["provider_options"]["llm_options"]
    
    def get_page_title(self):
        """Takes provider options from the config"""
        self.config = self.load_config()
        return self.config["page"]["page_title"]
    