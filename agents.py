import streamlit as st
import os

# Inject secrets into env before any client is instantiated
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage
from tools import web_search, scrape_url

# Model setup
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

# Custom Functional Agent to bypass LangChain's failing tool-calling factory
class SimpleFunctionalAgent:
    def __init__(self, tool_func):
        self.tool_func = tool_func
        
    def invoke(self, inputs):
        messages = inputs.get("messages", [])
        # Extract the query string from the ("user", "query") tuple passed by app.py
        query = messages[-1][1] if messages else ""
        
        # Directly invoke the Tavily or Scrape tool
        try:
            output = self.tool_func.invoke(query) if hasattr(self.tool_func, "invoke") else self.tool_func(query)
        except Exception as e:
            output = f"Tool execution error: {str(e)}"
            
        # Return an AIMessage directly so .content works perfectly in app.py
        return {"messages": [AIMessage(content=str(output))]}

# 1st agent
def build_search_agent():
    return SimpleFunctionalAgent(web_search)

# 2nd agent
def build_reader_agent():
    return SimpleFunctionalAgent(scrape_url)

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
