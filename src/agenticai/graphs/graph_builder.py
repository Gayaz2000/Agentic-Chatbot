import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langgraph.graph import StateGraph, START, END
from src.agenticai.state.state import State
from src.agenticai.nodes.basic_chatbot_nodes import Basic_chatbot_node
from src.agenticai.tools.search_tool import get_tools, create_search_tool_node
from langgraph.prebuilt import tools_condition
from src.agenticai.nodes.chatbot_with_tool import ChatBotWithTool
from src.agenticai.nodes.ai_news_nodes import AINewsNode

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

    def chatbot_with_tool_graph_build(self):
        """A chatbot with web tool"""
        tools = get_tools()
        tool_node = create_search_tool_node(tools)

        llm = self.llm

        node_obj_chatbot_with_tools=ChatBotWithTool(llm)
        chatbot_node = node_obj_chatbot_with_tools.create_chatbot(tools)

        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")

    def ai_news_graph_builder(self):
        """
        A funtion that uses llm to fetch news.
        """
        ai_news = AINewsNode(self.llm)

        self.graph_builder.add_node("Fetch news", ai_news.fetch_news)
        self.graph_builder.add_node("news summarizer", ai_news.news_summarizer)
        self.graph_builder.add_node("save results", ai_news.save_result)

        self.graph_builder.add_edge(START, "Fetch news")
        self.graph_builder.add_edge("Fetch news", "news summarizer")
        self.graph_builder.add_edge("news summarizer", "save results")
        self.graph_builder.add_edge("save results", END)
        

    def setup_graph(self, usecase: str):
        """
        Sets up the graph for selected usecase
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_graph_build()

        if usecase == "Chatbot with web":
            self.chatbot_with_tool_graph_build()
        
        if usecase == "AI news":
            self.ai_news_graph_builder()

        return self.graph_builder.compile()

        