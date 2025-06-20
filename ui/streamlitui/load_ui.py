import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from project_configs.config_load import Config #Load_Config
class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}
    
    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())
        st.session_state.timeframe = ""
        st.session_state.IsFetchButtonClicked = False

        with st.sidebar:
            llm_option = self.config.get_llm_options()
            usecase_option = self.config.get_usecase_options()
            
            model_option = self.config.get_groq_model_options()
            if model_option == "groq":
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_option)

            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_option)
            self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key", type="password")
            #os.environ["GROQ_API_KEY"] == 
            if not self.user_controls["GROQ_API_KEY"]:
                st.warning("⚠ Please enter valid groq api key")

            self.user_controls["selected_usecase"] = st.selectbox("Select Usecase", usecase_option)

            if self.usecase_option in ["Chatbot with web", "AI news"]:
                self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("Tavily API Key", type="password")
                #os.environ["TAVILY_API_KEY"] == 
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠ Please enter valid groq api key")

            if self.user_controls["selected_usecase"]  == "AI news":
                st.subheader("AI news Explorer")
                with st.sidebar:
                    time_frame = st.selectbox(
                        "Select Time Frame",
                        ["Daily", "Weekly", "Monthly"],
                        index=0,
                    )

                if st.button("Fetch latest news", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame

        return self.user_controls
    
if __name__ == "__main__":
    obj = LoadStreamlitUI()
    print(obj.load_streamlit_ui())