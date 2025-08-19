"""
answer_grader.py
----------------
Implements logic for grading the quality or correctness of generated answers in the Adaptive RAG pipeline.
"""

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from model import llm_model
from langchain_core.runnables import RunnableSequence

class GradeAnswer(BaseModel):
    """Binary score for correctness check on generated answer."""

    binary_score: str = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )

llm=llm_model

structured_llm_grader = llm.with_structured_output(GradeAnswer)

system = """You are a grader assessing whether an answer addresses / resolves a question \n 
     Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."""
answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
    ]
)

answer_grader: RunnableSequence = answer_prompt | structured_llm_grader