"""
retrieve.py
-----------
Implements the retrieval node for fetching relevant documents from the index in the Adaptive RAG pipeline.
"""

from typing import Any, Dict, List, Optional
from graph.state import GraphState
from ingestion import retriever

def retrieve(state: GraphState) -> Dict[str, Any]:
    """Retrieve documents based on the question in the state.
    Args:
        state (GraphState): The current state of the graph containing the question.
    Returns:
        Dict[str, Any]: A dictionary containing the retrieved documents and the question.
    """
    print("---RETRIEVE---")
    question = state["question"]

    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}