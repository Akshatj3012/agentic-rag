"""
generation.py
-------------
Implements the chain for generating answers or summaries using the LLM in the Adaptive RAG pipeline.
"""

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from model import llm_model
llm=llm_model

prompt = hub.pull("rlm/rag-prompt")
generation_chain = prompt | llm | StrOutputParser()