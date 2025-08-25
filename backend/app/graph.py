from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage

# Import the real nodes
from .services.router import intelligent_router_node
from .services.rag_system import rag_node
from .services.sql_database import sql_node
from .services.end_detection import end_conversation_node

class GraphState(TypedDict):
    user_message: str
    conversation_history: List[BaseMessage]
    bot_response: str
    next_node: str
    logs: List[str]
    current_job_role: Optional[str]
    booking_status: Optional[str]
    conversation_ended: Optional[bool]
    new_session_required: Optional[bool]



# --- Graph Definition ---
workflow = StateGraph(GraphState)

workflow.add_node("router", intelligent_router_node)
workflow.add_node("rag_system", rag_node)
workflow.add_node("sql_database", sql_node)
workflow.add_node("end_conversation", end_conversation_node)

workflow.set_entry_point("router")

def decide_next_node(state: GraphState):
    next_node_decision = state.get("next_node")
    if next_node_decision == "rag_system":
        return "rag_system"
    elif next_node_decision == "sql_database":
        return "sql_database"
    else:
        # This will now correctly route to the new end_conversation node
        return "end_conversation"

workflow.add_conditional_edges(
    "router",
    decide_next_node,
    {
        "rag_system": "rag_system",
        "sql_database": "sql_database",
        "end_conversation": "end_conversation"  # Route to the end_conversation node
    }
)


# After tool nodes finish generating a response, end this graph run.
# The next user message will start a new run from the router.
workflow.add_edge("rag_system", END)
workflow.add_edge("sql_database", END)

# Add edge from end_conversation to END
workflow.add_edge("end_conversation", END)

# Compile the graph
compiled_graph = workflow.compile()
