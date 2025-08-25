import os
from typing import Literal, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field # UPDATED IMPORT
from ..config import JOB_ROLE_MAPPING, OPENAI_API_KEY

# --- Dynamic Configuration from Central Mapping ---
VALID_ROLE_IDS = list(JOB_ROLE_MAPPING.keys())

role_instructions = "\n".join(
    f"- To discuss the {JOB_ROLE_MAPPING[role_id]['friendly_name']} role, use the ID '{role_id}'. The user might refer to it with aliases like: {', '.join(aliases)}."
    for role_id, aliases in [(k, v['aliases']) for k, v in JOB_ROLE_MAPPING.items()]
)

# --- Pydantic Model for Structured Output ---
class RouteQuery(BaseModel):
    """Routes a user query and extracts the canonical job role ID."""
    next_node: Literal["rag_system", "sql_database", "end_conversation"] = Field(
        ...,
        description="Given the user query, choose the best tool to handle it."
    )
    job_role_id: Optional[Literal[*VALID_ROLE_IDS]] = Field(
        None,
        description="If the user's query is about a specific job, extract its canonical ID."
    )

# --- LLM and Prompt Setup ---
llm = ChatOpenAI(model="gpt-4o", openai_api_key=OPENAI_API_KEY, temperature=0)
structured_llm = llm.with_structured_output(RouteQuery)

system_prompt = f"""You are a professional, polite, and helpful AI chat Assistant.
Your mission is to represent the company by providing which roles are available, information about the roles and schedule interviews.

**Your Core Directives:**
1. **Route to RAG for Role Information:** Route to `rag_system` when:
   - The candidate asks specific questions about a particular role (e.g., "what are the requirements for Data Analyst?", "tell me about the Python Developer role")
   - The candidate just mentions a specific role name (e.g., "Data analyst", "Python Developer") - provide them with general information about that role

2. **Route to Scheduling:** When the candidate agrees to schedule an interview or asks about times, route to `sql_database`. This includes:
   - Direct scheduling requests (e.g., "can we schedule an interview?", "I'd like to book an interview")
   - Time/date preferences (e.g., "I can come at 15:00", "3 days afternoon", "next week morning")
   - Confirmation of slots (e.g., "yes, that works", "I'll take that slot")

3. **End Conversation:** Choose `end_conversation` ONLY when:
   - The candidate uses clear sign-off phrases (e.g., "thank you, that's all", "goodbye", "no more questions", "that's it")
   - The candidate explicitly states they are not interested in any of the roles
   - The candidate has already booked an interview and confirms they have no more questions

4. **Proactive Scheduling:** proactively and politely ask if they'd like to schedule an interview. Be professional and never pushy.

**Context-Aware Routing Logic:**
- If the user mentions a specific role or asks questions about a specific role and hasn't been offered scheduling yet, route to `rag_system` and include a polite scheduling offer in your response.
- If the user has already been offered scheduling and is asking more questions about a specific role, continue routing to `rag_system` without being repetitive.
- For general questions about available positions, introductions, or role clarifications, route to `rag_system`.
- Always maintain a professional, helpful tone regardless of how many questions they ask.

**Job Role Extraction Logic:**
The candidate choose one role from the list, if he choose more than one role, you must ask him to choose just one role.
You must identify the user's desired job role using the following mapping. Extract the canonical ID.
{role_instructions}, if you can't find the role in the list, you must ask the user to choose one role from the list.
If a role was mentioned previously, maintain that context. If the user mentions a new role, switch to it.

"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="conversation_history"),
    ("human", "{user_message}"),
])

router_chain = prompt | structured_llm

def intelligent_router_node(state):
    if 'logs' not in state: state['logs'] = []
    state['logs'].append("Executing intelligent router...")
    
    # Debug: Log the user message
    state['logs'].append(f"User message: '{state['user_message']}'")

    
    # Count questions and role mentions (rough heuristic)
    question_indicators = ['what', 'how', 'when', 'where', 'why', 'tell me', 'explain', 'describe']
    user_message_lower = state['user_message'].lower()
    if any(indicator in user_message_lower for indicator in question_indicators):
        # Guard against missing counter in state
        state['questions_asked'] = int(state.get('questions_asked', 0)) + 1

    
    route_decision = router_chain.invoke({
        "user_message": state["user_message"],
        "conversation_history": state.get("conversation_history", [])
    })
    
    state['logs'].append(f"Router decision: {route_decision.next_node}")
    state["next_node"] = route_decision.next_node
    
    # ROLE STATE MANAGEMENT - ONLY THE ROUTER CAN CHANGE THIS
    if route_decision.job_role_id:
        # Update role state only if it's different
        if state.get('current_job_role') != route_decision.job_role_id:
            state['current_job_role'] = route_decision.job_role_id
            state['logs'].append(f"Role state changed to: '{route_decision.job_role_id}'")
        else:
            state['logs'].append(f"Role state unchanged: '{route_decision.job_role_id}'")
    else:
        # No new role mentioned - maintain existing role state
        if state.get('current_job_role'):
            state['logs'].append(f"Role state maintained: '{state.get('current_job_role')}'")
        else:
            state['logs'].append("No role state available")
    
    # Single source of truth - log the final role state
    state['logs'].append(f"ROLE STATE: '{state.get('current_job_role', 'None')}'")
    
    # Context-aware routing logic
    
    # If no job role is set and user is asking questions, route to RAG to ask for clarification
    if not state.get('current_job_role') and route_decision.next_node == "rag_system":
        state['logs'].append("No job role set, routing to RAG for clarification")
    
    # Fallback: If we can't determine what to do, ask for clarification
    if not route_decision.next_node or route_decision.next_node not in ["rag_system", "sql_database", "end_conversation"]:
        state['logs'].append("Could not determine next action, asking for clarification")
        state["bot_response"] = "I can help you with job information and scheduling interviews. Which role are you interested in?"
        state["next_node"] = "end_conversation"  # End this iteration
        return state
    
    if route_decision.next_node == "end_conversation":
        # Let the end_conversation_node handle the response and session restart signals
        # Don't set bot_response here - let the end_conversation_node do it
        state['logs'].append("Routing to end_conversation_node for proper session handling")

    # Encourage scheduling if a role is already selected and no booking yet
    if state.get('current_job_role') and state.get('booking_status') != 'confirmed':
        state['should_offer_scheduling'] = True

    return state
