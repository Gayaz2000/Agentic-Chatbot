import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langgraph.graph import StateGraph, START, END
from src.agenticai.state.state import State
from src.agenticai.nodes.basic_chatbot_nodes import Basic_chatbot_node

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State) 

    def basic_chatbot_graph_build(self):
        """
        Buildeing basic chatbot using langgraph.
        """
        self.basic_chatbot_node = Basic_chatbot_node(self.llm)

        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def setup_graph(self, usecase: str):
        """
        Sets up the graph for selected usecase
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_graph_build()

        return self.graph_builder.compile()

        