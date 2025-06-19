from src.agenticai.state.state import State


class ChatBotWithTool:
    def __init__(self, model):
        self.llm = model

    def process_function(self, state:State):
        """A chatbot node """
        user_input = state["messages"][-1] if state["messages"] else ""
        llm_response = self.llm.invoke([{"role":"user", "content":user_input}])

        tool_response = f"Tool integration for: '{user_input}'"

        return {"messages":[llm_response, tool_response]}
    
    def create_chatbot(self, tools):
        """A chatbot with with web tool"""
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            """A chatbot logic for processing"""
            return {"messages":[llm_with_tools.invoke(state["messages"])]}
        
        return chatbot_node
