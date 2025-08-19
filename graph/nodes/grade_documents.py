"""
grade_documents.py
------------------
Implements the grading logic for evaluating the relevance of retrieved documents in the Adaptive RAG pipeline.
"""

from typing import Any, Dict, List, Optional
from graph.chains.retrieval_grader import retrieval_grader
from graph.state import GraphState

def grade_documents(state: GraphState) -> Dict[str, Any]:
    """Grade the relevance of retrieved documents based on the question in the state.
    
    Args:
        state (GraphState): The current state of the graph containing the question and documents.
        
    Returns:
        Dict[str, Any]: A dictionary containing the binary scores for each document and the question.
    """
    print("---GRADE DOCUMENTS---")
    question = state["question"]
    documents = state["documents"]
    web_search = False
    filtered_documents = []
    for document in documents:
        score = retrieval_grader.invoke({"document": document.page_content, "question": question})
        grade = score.binary_score
        if grade == "yes":
            print("---GRADE: DOCUMENT IS RELEVANT---")
            filtered_documents.append(document) 
        else:
            print("---GRADE: DOCUMENT IS NOT RELEVANT---")
            web_search = True
            continue
    return {"documents": filtered_documents, "question": question, "web_search": web_search}