import os
from sqlalchemy import create_engine, text
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from ..config import JOB_ROLE_MAPPING, OPENAI_API_KEY, DATABASE_URL
from datetime import datetime

# --- Environment and Database Setup ---
engine = create_engine(DATABASE_URL)

def get_time_range(time_preference: str):
    """Converts a string like 'morning' into a time range."""
    time_preference = time_preference.lower()
    if 'morning' in time_preference:
        return '09:00:00', '12:00:00'
    elif 'afternoon' in time_preference:
        return '12:01:00', '17:00:00'
    else: # Default to any time
        return '09:00:00', '17:00:00'

@tool
def get_available_time_slots(role_id: str, date_preference: str, time_preference: str = 'any') -> str:
    """
    Finds available interview slots for a specific role_id on a given date and time preference.
    - role_id: The canonical ID for the job role (e.g., 'python_developer').
    - date_preference: The desired date in 'YYYY-MM-DD' format.
    - time_preference: A string, such as 'morning', 'afternoon', or 'any'.
    """
    role_info = JOB_ROLE_MAPPING.get(role_id)
    if not role_info: 
        return f"Error: Invalid role ID '{role_id}'. Available roles: {list(JOB_ROLE_MAPPING.keys())}"
    
    sql_position_name = role_info["sql_position_name"]
    start_time, end_time = get_time_range(time_preference)
    try:
        with engine.connect() as connection:
            query = text("""
                SELECT to_char(date, 'YYYY-MM-DD') || ' ' || to_char(time, 'HH24:MI') as start_time
                FROM "Schedule"
                WHERE available = TRUE AND position = :position AND date = :date AND time BETWEEN :start_time AND :end_time
                ORDER BY date, time LIMIT 10;
            """)
            result = connection.execute(query, {"position": sql_position_name, "date": date_preference, "start_time": start_time, "end_time": end_time})
            slots = [row[0] for row in result.fetchall()]
            if slots:
                return f"Great! I found these available slots for {date_preference} {time_preference}:\n" + "\n".join(slots)
            else:
                alt_query = text("""
                    SELECT to_char(date, 'YYYY-MM-DD') || ' ' || to_char(time, 'HH24:MI') as start_time
                    FROM "Schedule" WHERE available = TRUE AND position = :position AND date = :date
                    ORDER BY date, time LIMIT 5;
                """)
                alt_result = connection.execute(alt_query, {"position": sql_position_name, "date": date_preference})
                alt_slots = [row[0] for row in alt_result.fetchall()]
                if alt_slots:
                    return f"Unfortunately, there are no slots available in the {time_preference} on {date_preference}. However, I did find these other times on that day:\n" + "\n".join(alt_slots)
                else:
                    return f"I'm sorry, but there are no available interview slots at all on {date_preference} for the {role_info['friendly_name']} role."
    except Exception as e:
        return f"Database query failed: {e}"

@tool
def book_interview_slot(role_id: str, date: str, time: str) -> str:
    """
    Books an interview slot by updating its availability in the database.
    - role_id: The canonical ID for the job role.
    - date: The exact date of the slot to book in 'YYYY-MM-DD' format.
    - time: The exact time of the slot to book in 'HH24:MI' format.
    """
    role_info = JOB_ROLE_MAPPING.get(role_id)
    if not role_info: 
        return f"Error: Invalid role ID '{role_id}'. Available roles: {list(JOB_ROLE_MAPPING.keys())}"
    sql_position_name = role_info["sql_position_name"]
    try:
        with engine.connect() as connection:
            with connection.begin() as transaction:
                query = text("""
                    UPDATE "Schedule" SET available = FALSE
                    WHERE position = :position AND date = :date AND time = :time AND available = TRUE;
                """)
                result = connection.execute(query, {"position": sql_position_name, "date": date, "time": time})
                transaction.commit()
                if result.rowcount > 0:
                    return (f"Success! Your interview for the {role_info['friendly_name']} role has been booked for {date} at {time}. "
                            "Would you like to ask any more questions about the role?")
                else:
                    return "It seems that slot was just taken or does not exist. Please try searching for another time."
    except Exception as e:
        return f"Database update failed: {e}"

llm = ChatOpenAI(model="gpt-4o", openai_api_key=OPENAI_API_KEY, temperature=0)
llm_with_tools = llm.bind_tools([get_available_time_slots, book_interview_slot])

def sql_node(state):
    logs = state.get("logs", [])
    logs.append("Executing Scheduling Agent Node...")
    
    if state.get("booking_status") == "confirmed":
        logs.append("Interview already booked. Informing user.")
        state["bot_response"] = "It looks like you already have an interview booked. Can I help with anything else?"
        return state

    # READ ONLY - Get role state from router
    role_id = state.get("current_job_role")
    logs.append(f"READING ROLE STATE: '{role_id}'")
    
    if not role_id:
        logs.append("ERROR: No role state available from router")
        state["bot_response"] = "My apologies, I need to know which role we're discussing before I can schedule an interview. Could you remind me?"
        state["logs"] = logs
        return state

    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""You are a helpful and precise Scheduling Assistant. Your only goal is to get an interview booked for the user.
        
        **CRITICAL:** You are scheduling for the **{JOB_ROLE_MAPPING[role_id]['friendly_name']}** role (role_id: '{role_id}').
        Today's date is {datetime.now().strftime('%Y-%m-%d')}.
        **Booking Status:** An interview has **not yet** been booked.
        
        **IMPORTANT:** When calling tools, ALWAYS use role_id = '{role_id}' for the {JOB_ROLE_MAPPING[role_id]['friendly_name']} position.
        
        Follow this process strictly:
        1.  **Gather Information:** If you don't know the user's desired date and time preference, ask for it.
        2.  **Search for Slots:** Once you have preferences, use the `get_available_time_slots` tool with role_id = '{role_id}'.
        3.  **Present Options:** Clearly present the available slots.
        4.  **Await Confirmation:** The user must explicitly confirm which slot they want.
        5.  **Book the Slot:** Once confirmed, you must call the `book_interview_slot` tool with role_id = '{role_id}' and the exact date and time.
        6.  **Handle Declines:** If the user declines, ask for a different preference and restart from Step 2.
        """),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}"),
    ])
    
    chain = prompt | llm_with_tools
    ai_message = chain.invoke({"input": state["user_message"], "history": state.get("conversation_history", [])})
    
    if not ai_message.tool_calls:
        bot_response = ai_message.content
    else:
        tool_call = ai_message.tool_calls[0]
        logs.append(f"Scheduling Agent decided to call tool '{tool_call['name']}' with arguments: {tool_call['args']}")
        tool_args = tool_call["args"]
        
        # ALWAYS use the role_id from state, never trust the LLM's role_id
        tool_args['role_id'] = role_id
        logs.append(f"FORCING role_id to: '{role_id}'")
        
        tool_output = (get_available_time_slots if tool_call['name'] == 'get_available_time_slots' else book_interview_slot).invoke(tool_args)
        bot_response = tool_output
        
        if tool_call['name'] == 'book_interview_slot' and 'Success!' in tool_output:
            logs.append("Booking successful. Updating session state to 'confirmed'.")
            state['booking_status'] = 'confirmed'

    state["bot_response"] = bot_response
    state["logs"] = logs
    return state
