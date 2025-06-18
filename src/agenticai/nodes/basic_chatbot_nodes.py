from state.state import State


class Basic_chatbot_node:
    def __init__(self, model):
        self.llm = model

    def process(self,state: State)->dict:
        """
        Process the input and generate the chat response.
        """
        return {"messages": [self.llm.invoke(state["messages"])]}