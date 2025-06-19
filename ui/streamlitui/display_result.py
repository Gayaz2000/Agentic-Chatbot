import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
#import json

class DisplayStreamlitResult:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        if usecase == "Basic Chatbot":
            for event in graph.stream({"messages":("user", user_message)}):
                print(event.values())
                for value in event.values():
                    print(value["messages"])
                    with st.chat_message("user"):
                        st.write(user_message)
                    with st.chat_message("assistant"):
                        st.write(value["messages"].content)

        elif usecase == "Chatbot with web":
            initial_message = {"messages": [user_message]}
            res = graph.invoke(initial_message)
            for msg in res["messages"]:
                if type(msg) == HumanMessage:
                    with st.chat_message("user"):
                        st.write(msg.content)
                elif type(msg) == ToolMessage:
                    with st.chat_message("ai"):
                        st.write("Tool Call Started")
                        st.write(msg.content)
                        st.write("Tool Call Ended")
                elif type(msg) == AIMessage and msg.content:
                    with st.chat_message("assitant"):
                        st.write(msg.content)
                