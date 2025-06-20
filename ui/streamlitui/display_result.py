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

        elif usecase == "AI news":
            frequency = self.user_message
            with st.spinner("Fetching and Summarizing AI News..")
                res = graph.invoke({"messages": frequency})
                try:
                    AI_NEWS_PATH = f"./AINEWS/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH, "r") as file:
                        markdown_content = file.read()

                    st.markdown(markdown_content, unsafe_allow_html=True)

                except FileNotFoundError:
                    st.error(f"News not generated or File was not found: {AI_NEWS_PATH}")
                except Exception as e:
                    st.error(f"An error occured: {str(e)}")