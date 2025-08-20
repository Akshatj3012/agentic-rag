"""
router.py
---------
Implements routing logic for directing the flow between different chains or nodes in the Adaptive RAG pipeline.
"""

from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from model import llm_model

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vectorstore", "websearch"] = Field(
        ...,
        description="Given a user question choose to route it to web search or a vectorstore.",
    )

llm = llm_model

structured_llm_router = llm.with_structured_output(RouteQuery)

system = """You are an expert at routing a user question to a vectorstore or web search.
The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
Use the vectorstore for questions on these topics. For all else, use web-search."""
route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

question_router = route_prompt | structured_llm_router

class MemoryLookup(BaseModel):
    """Memory lookup to retrieve relevant information from chat history."""

    summary:  Literal["generate", "no relevant information found"] = Field(
        ...,
        description="Summary of relevant information from chat history or a message indicating no relevant information found.",
    )

memory_lookup_llm = llm.with_structured_output(MemoryLookup)

memory_lookup_system_message = """You are an expert at summarizing chat history.
Given the chat history and the current question, return generate
If there is no relevant information, return 'No relevant information found'."""

memory_lookup_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", memory_lookup_system_message),
        ("human", "Here is the chat history:\n{chat_history}\nThis is the current question:\n{question}\nIf there is relevant information in the chat history, return it as a summary, otherwise return 'No relevant information found'."),
    ]
)
memory_lookup_chain = memory_lookup_prompt | memory_lookup_llm