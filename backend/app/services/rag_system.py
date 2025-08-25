from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ..config import JOB_ROLE_MAPPING, OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_INDEX_NAME

# --- Initialize Pinecone client ---
pc = Pinecone(api_key=PINECONE_API_KEY)

embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)
llm = ChatOpenAI(model="gpt-4o", openai_api_key=OPENAI_API_KEY, temperature=0)

def get_retrieved_documents(query: str, logs: list, role_id: str = None, k: int = 5) -> str:
    logs.append("Retrieving documents from Pinecone...")
    pinecone_index = pc.Index(PINECONE_INDEX_NAME)
    
    filter_dict = {}
    if role_id:
        filter_dict['role_id'] = role_id
        logs.append(f"Applying metadata filter: role_id = '{role_id}'")

    query_embedding = embeddings_model.embed_query(query)
    
    retrieval_results = pinecone_index.query(
        vector=query_embedding, top_k=k, filter=filter_dict or None, include_metadata=True
    )
    
    context = "\n\n---\n\n".join([match['metadata']['text'] for match in retrieval_results['matches']])
    logs.append(f"Found {len(retrieval_results['matches'])} relevant document chunks.")
    return context

template = """You are an expert assistant answering questions about a job description.
Your task is to provide helpful information based on the user's input and the CONTEXT below.

**IMPORTANT RULES:**
1. If the user asks a specific question, answer it based on the CONTEXT.
2. If the user just mentions a role (like "Data analyst"), provide a general overview of that role from the CONTEXT.
3. If the user's question cannot be answered from the CONTEXT, say: "I'm sorry, but that specific information is not available in the provided job description."
4. Keep responses concise, professional, and informative.
5. Always provide useful information when possible.

CONTEXT:
{context}
USER INPUT:
{question}
RESPONSE:
"""
prompt = ChatPromptTemplate.from_template(template)

def rag_node(state):
    logs = state.get("logs", [])
    logs.append("Executing RAG node...")
    user_message = state["user_message"]
    
    # READ ONLY - Get role state from router
    role_id = state.get("current_job_role")
    logs.append(f"READING ROLE STATE: '{role_id}'")
    
    # Handle cases where no role is set
    if not role_id:
        logs.append("No role state available - handling general inquiries")
        
        # Check for multiple role mentions
        if state.get('multiple_roles_mentioned', False):
            state["bot_response"] = """I noticed you mentioned multiple roles. To provide you with the best assistance, please choose just one role that you'd like to learn more about:

• Data Analyst
• Machine Learning Engineer
• Python Developer
• Senior SQL Developer

Which specific role interests you the most?"""
            state["logs"] = logs
            return state
        
        # Check for position inquiry
        user_message_lower = user_message.lower()
        if any(phrase in user_message_lower for phrase in ['open position', 'available position', 'what position', 'current position', 'what roles', 'what jobs']):
            state["bot_response"] = """Here are our current open positions:

• Data Analyst
• Machine Learning Engineer  
• Python Developer
• Senior SQL Developer

Which role are you interested in learning more about?"""
            state["logs"] = logs
            return state
        
        # Check for introductions/greetings
        elif any(phrase in user_message_lower for phrase in ['hi', 'hello', 'my name is', 'i am', 'i\'m']):
            state["bot_response"] = """Hello! I'm an AI career assistant. I can help you with the following open positions:

• Data Analyst
• Machine Learning Engineer
• Python Developer
• Senior SQL Developer

Which role are you interested in learning more about?"""
            state["logs"] = logs
            return state
        
        # Default response for no role
        else:
            state["bot_response"] = "I can help you with information about our available positions. Which job role are you interested in?"
            state["logs"] = logs
            return state

    context = get_retrieved_documents(user_message, logs, role_id)
    
    rag_chain = prompt | llm | StrOutputParser()
    
    logs.append("Generating final answer with LLM...")
    bot_response = rag_chain.invoke({"context": context, "question": user_message})

    # Append a clear scheduling call-to-action when a role is selected and not yet booked
    should_offer = bool(state.get('should_offer_scheduling', False) or (
        state.get('current_job_role') and state.get('booking_status') != 'confirmed'
    ))
    if should_offer:
        logs.append("Adding scheduling call-to-action to response.")
        scheduling_offer = (
            "\n\nIf you're interested, we can proceed to scheduling. "
            "Would you like to book an interview for this role?"
        )
        bot_response += scheduling_offer

    
    logs.append("RAG node execution complete.")
    state["bot_response"] = bot_response
    state["logs"] = logs
    
    return state
