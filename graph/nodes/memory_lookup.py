from graph.state import GraphState
from graph.chains.router import MemoryLookup, memory_lookup_chain

def memory_lookup(state: GraphState) -> str:
    """
    Perform a memory lookup to retrieve relevant information from chat history.
    """
    print("---MEMORY LOOKUP---")
    if state.get("chat_history") is None or len(state["chat_history"]) == 0:
        print("---NO CHAT HISTORY AVAILABLE---")
        return {"generate_from_memory": False, "question": state["question"], "chat_history": []}
        
    
    # Invoke the memory lookup chain
    print("---CHECKING CHAT HISTORY FOR RELEVANT INFORMATION---")
    memory_lookup_result: MemoryLookup = memory_lookup_chain.invoke({
        "chat_history": state["chat_history"],
        "question": state["question"]
    })
    
    if memory_lookup_result.summary == "generate":
        print("---RELEVANT INFORMATION FOUND IN CHAT HISTORY---")
        state["generate_from_memory"] = True
        docs = [doc["content"] for doc in state["chat_history"] if doc["role"] == "assistant"]
        state["documents"] = docs
        # print("---DOCUMENTS FROM CHAT HISTORY---", state["documents"])
        return {"generate_from_memory": True, "question": state["question"], "chat_history": state["chat_history"], "documents": state["documents"]}
    else:
        print("---NO RELEVANT INFORMATION FOUND IN CHAT HISTORY---")
        state["generate_from_memory"] = False
        return {"generate_from_memory": False, "question": state["question"], "chat_history": state["chat_history"]}