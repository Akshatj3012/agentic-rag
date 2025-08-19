"""
retrieval_grader.py
------------------
This module defines the retrieval grading chain for evaluating the relevance of retrieved documents to a user question. It uses a binary scoring system ('yes' or 'no') to indicate relevance, leveraging a structured LLM output and a custom prompt template.

Classes:
- GradeDocuments: Pydantic model for binary relevance grading.

Variables:
- structured_llm_grader: LLM with structured output for grading.
- system: System prompt for the grader.
- grade_prompt: ChatPromptTemplate for the grading task.
- retrieval_grader: The composed chain for grading retrievals.
"""

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from model import llm_model

llm = llm_model

class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )


structured_llm_grader = llm.with_structured_output(GradeDocuments)

system = """You are a grader assessing relevance of a retrieved document to a user question. \n 
    If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant. \n
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)

retrieval_grader = grade_prompt | structured_llm_grader