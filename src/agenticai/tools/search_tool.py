from langchain_community.tools import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools():
    """get all tools"""
    tools = [TavilySearchResults(max_results=3)]
    return tools

def create_search_tool_node(tools):
    """
    create and return a tool node for graph
    """
    return ToolNode(tools=tools)