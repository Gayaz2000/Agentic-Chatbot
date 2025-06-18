import streamlit as st
from ui.streamlitui.load_ui import LoadStreamlitUI
from src.agenticai.LLMs.groqllms import GroqLLM
from src.agenticai.graphs.graph_builder import GraphBuilder
from ui.streamlitui.display_result import DisplayStreamlitResult

def load_langgraph_agenticai_app():
    """
    Loads and run langgraph agentic ai with streamlit ui.
    This function initializes ui, handles user input, configures the llm model,
    sets up the graph based on selected usecase and display the output 
    while implementing exception handling for robustness
    """

    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from ui")
        return
    
    user_message = st.chat_input("Enter your message: ")
    if user_message:
        try:
            obj_llm_config = GroqLLM(user_controls=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initated.")
                return
            
            usecase = user_input.get("selected_usecase")

            if not usecase:
                st.error("Error: No usecase selected.")
                return
            
            graph_builder = GraphBuilder(model)

            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayStreamlitResult(usecase, graph, user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Falied to setup graph {e}.")
                return
        except Exception as e:
            st.error(f"Error: User input is not provided {e}.")
            return