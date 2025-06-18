import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from config_files.config_load import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}
    
    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())

        with st.sidebar:
            llm_option = self.config.get_llm_options()
            usecase_option = self.config.get_usecase_options()
            
            model_option = self.config.get_groq_model_options()
            if model_option == "groq":
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_option)

            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_option)
            self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key", type="password")
    
            if not self.user_controls["GROQ_API_KEY"]:
                st.warning("⚠ Please enter valid groq api key")

            self.user_controls["selected_usecase"] = st.selectbox("Select Usecase", usecase_option)

        return self.user_controls
    
if __name__ == "__main__":
    obj = LoadStreamlitUI()
    print(obj.load_streamlit_ui())