import streamlit as st
import os

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url

# Model setup
llm = ChatGroq(model="meta-llama/llama-prompt-guard-2-22m", temperature=0)

# 1st agent: Direct tool execution simulation to avoid LangChain BadRequest errors
def build_search_agent():
    # We return a custom runner object or function instead of a breaking LangChain agent
    class SimpleAgent:
        def invoke(self, inputs):
            query = inputs["messages"][-1][1]
            search_output = web_search.invoke(query)
            return {"messages": [("assistant", search_output)]}
    return SimpleAgent()

# 2nd agent: Direct reader tool execution
def build_reader_agent():
    class SimpleReaderAgent:
        def invoke(self, inputs):
            text_prompt = inputs["messages"][-1][1]
            # Extract URL or search content and pass to scraper tool if needed
            scraped_content = scrape_url.invoke("https://duckduckgo.com/?q=" + text_prompt[:50])
            return {"messages": [("assistant", scraped_content)]}
    return SimpleReaderAgent()

# Writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()
