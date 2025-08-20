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
        chat_history: chat history
        generate_from_memory: whether to generate from memory
    """
    question: str
    generation: str
    web_search: bool
    documents: List[str]
    chat_history: List[Dict[str, str]]
    generate_from_memory: bool 


if __name__ == "__main__":
    # Example usage
    state: GraphState = {
        "question": "What is the capital of France?",
        "generation": "",
        "web_search": False,
        "documents": [],
        "chat_history": [],
        "generate_from_memory": False
    }
    print(state)
    print ("State Generate from Memory: ", state["generate_from_memory"])
    # Output: {'question': 'What is the capital of France?', 'generation': '',