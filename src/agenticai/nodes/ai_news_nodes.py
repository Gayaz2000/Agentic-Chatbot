from tavily import TavillyClient
from langchain_core.prompts import ChatPromptTemplate


class AINewsNode:
    def __init__(self, llm):
        self.tavily = TavillyClient()
        self.llm = llm
        self.state = {}

    def fetch_news(self, state: dict)-> dict:
        """
        Fetch ai news based on specified frequency
        """
        frequency = state["messages"][0].content
        self.state["frequency"] = frequency
        time_range_map ={"daily":"d", "weekly":"w", "monthly":"m", "yearly":"y"}
        days_map = {"daily": 1, "weekly": 7, "monthly": 12, "yearly": 366}

        response = self.tavily.search(
                query = "Top Artifical Intelligence(AI) technology news India and globally "
                topic = "news",
                time_range = time_range_map[frequency],
                include_answer = "advanced",
                max_results = 14,
                days = days_map[frequency],
        )

        state["news_data"] = response.get("results", [])
        self.state["news_data"] = state["news_data"]
        return self.state
    
    def news_summarizer(self, state: dict)-> dict:
        """
        A function to summarize the news on ai
        """
        news_items = self.state["news_data"]

        ai_news_prompt = ChatPromptTemplate.from_template("""
        You are an expert technology journalist. Your task is to summarize the following news article related to artificial intelligence.

        --- ARTICLE START ---
        {article}
        --- ARTICLE END ---

        Summarize the article clearly and concisely, including:
        1. The main event or development.
        2. Any companies, organizations, or people involved.
        3. Key technologies, breakthroughs, or issues discussed.
        4. Implications or potential impact, if any.
        5. Tone of the article (e.g., optimistic, critical, neutral).

        Output the summary in this format:

        **Title**: [Insert a suitable title]
        **Summary**:
        - [Main point 1]
        - [Main point 2]
        - [Etc.]

        **Category**: [Choose from: Research, Business, Ethics, Regulation, Product Launch, Other]
        """)
        article_str = "\n\n".join([
            f"content: {item.get("content", "")}\nURL: {item.get("url", "")}\nDate: {item.get("published_date", "")}"
            for item in news_items
        ])

        response = self.llm.invoke(ai_news_prompt.format(article = article_str))
        state["summary"] = response.content
        self.state["summary"] = state["summary"]
        return self.state
    
    def save_result(self, state):
        """A function to  save ai news results"""
        frequency = self.state["frequency"]
        summary = self.state["summary"]
        filename = f"./AINews/{frequency}_summary.md"
        with open(filename, "w") as file:
            file.write(f"# {frequency.capitalized()} AI News Summary\n\n")
            file.write(summary)
        self.state["filename"] = filename
        return self.state 