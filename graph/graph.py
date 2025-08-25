"""
graph.py
--------
Defines the main graph structure and logic for the Adaptive RAG pipeline, orchestrating the flow between nodes.
"""

from dotenv import load_dotenv
from langgraph.graph import END, StateGraph

from graph.chains.answer_grader import answer_grader
from graph.chains.hallucination_grader import hallucination_grader
from graph.chains.router import RouteQuery, question_router, MemoryLookup, memory_lookup_chain
from graph.consts import GENERATE, GRADE_DOCUMENTS, RETRIEVE, WEBSEARCH, ADDED_TO_MEMORY
from graph.nodes.generate import generate
from graph.nodes.grade_documents import grade_documents
from graph.nodes.retrieve import retrieve
from graph.nodes.web_search import web_search
from graph.state import GraphState
from graph.nodes.add_to_memory import add_to_memory
from graph.nodes.memory_lookup import memory_lookup
# from graph.nodes.memory import memory_lookup

load_dotenv()
MEMORY_LOOKUP = "memory_lookup"







def decide_to_generate(state):
    print("---ASSESS GRADED DOCUMENTS---")

    if state["web_search"]:
        print(
            "---DECISION: NOT ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, INCLUDE WEB SEARCH---"
        )
        return WEBSEARCH
    else:
        print("---DECISION: GENERATE---")
        return GENERATE


def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:
    print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )

    if hallucination_grade := score.binary_score:
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        print("---GRADE GENERATION vs QUESTION---")
        score = answer_grader.invoke({"question": question, "generation": generation})
        if answer_grade := score.binary_score:
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"


def route_question(state: GraphState) -> str:
    """
    Route question to web search or RAG.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """

    print("---ROUTE QUESTION---")
    question = state["question"]
    source: RouteQuery = question_router.invoke({"question": question})

    if source.datasource == WEBSEARCH:
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return WEBSEARCH
    elif source.datasource == "vectorstore":
        print("---ROUTE QUESTION TO RAG---")
        return RETRIEVE


workflow = StateGraph(GraphState)

workflow.add_node(MEMORY_LOOKUP, memory_lookup)
workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)
workflow.add_node(ADDED_TO_MEMORY, add_to_memory)

# New entry point: always check memory first
workflow.set_entry_point(MEMORY_LOOKUP)

def after_memory_lookup(state: GraphState) -> str:
    print("---DECIDE NEXT STEP AFTER MEMORY LOOKUP---")
    print("State keys:", list(state.keys()))
    if state["generate_from_memory"]:
        return GENERATE
    else:
        question = state["question"]
        source: RouteQuery = question_router.invoke({"question": question})
        if source.datasource == WEBSEARCH:
            return WEBSEARCH
        elif source.datasource == "vectorstore":
            return RETRIEVE
        else:
            return RETRIEVE

workflow.add_conditional_edges(
    MEMORY_LOOKUP,
    after_memory_lookup,
    {
        GENERATE: GENERATE,
        WEBSEARCH: WEBSEARCH,
        RETRIEVE: RETRIEVE,
    },
)

workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    {
        WEBSEARCH: WEBSEARCH,
        GENERATE: GENERATE,
    },
)

workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    {
        "not supported": GENERATE,
        "useful": ADDED_TO_MEMORY,
        "not useful": WEBSEARCH,
    },
)
workflow.add_edge(WEBSEARCH, GENERATE)
workflow.add_edge(GENERATE, ADDED_TO_MEMORY)
workflow.add_edge(ADDED_TO_MEMORY, END)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")