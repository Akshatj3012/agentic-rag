from graph.state import GraphState

def add_to_memory(state: GraphState) -> GraphState:
    """
    Add the current question and answer to the chat history.
    """
    if not state["chat_history"]:
        state["chat_history"] = []
    
    # Append the current question and answer to chat history
    print("---ADDING QUESTION TO CHAT HISTORY---")
    state["chat_history"].append({
        "role": "user",
        "content": state["question"]
    })
    
    if state["generation"]:
        print("---ADDING GENERATION TO CHAT HISTORY---")
        state["chat_history"].append({
            "role": "assistant",
            "content": state["generation"]
        })
    print("---CHAT HISTORY UPDATED---", state["chat_history"])
    print("State after adding to memory:", state)
    return state