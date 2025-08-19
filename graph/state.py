"""
state.py
--------
Defines and manages the state for the Adaptive RAG pipeline, including any shared variables or stateful logic used across the graph.
"""

from typing import List, TypedDict, Optional, Dict

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search
        documents: list of documents
    """
    question: str
    generation: str
    web_search: bool
    documents: List[str]