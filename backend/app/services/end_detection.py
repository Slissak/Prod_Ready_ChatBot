
def end_conversation_node(state):
    """
    Handles the end of the conversation by setting a final message and signaling session restart.
    """
    if 'logs' not in state:
        state['logs'] = []
    
    state['logs'].append("Ending conversation and preparing for new session.")
    
    # Handle different types of end conversation scenarios
    user_message_lower = state['user_message'].lower()
    
    # Check for sign-off phrases
    sign_off_phrases = ['thank you, that\'s all', 'goodbye', 'no more questions', 'that\'s it', 'thanks, bye', 'end of conversation']
    if any(phrase in user_message_lower for phrase in sign_off_phrases):
        state["bot_response"] = "Thank you for your time. Have a great day!"
    
    # Check for not interested in roles
    elif any(phrase in user_message_lower for phrase in ['not interested', 'no interest', 'not for me', 'not what i\'m looking for']):
        state["bot_response"] = "I understand. Thank you for your interest in our company. If you change your mind or have any questions in the future, feel free to reach out. Have a great day!"
    
    # Check for booked interview with no more questions
    elif state.get('booking_status') == 'confirmed' and any(phrase in user_message_lower for phrase in ['no more questions', 'that\'s all', 'nothing else']):
        state["bot_response"] = "Perfect! Your interview has been confirmed. We look forward to meeting you. Have a great day!"
    
    # Default end conversation response
    else:
        state["bot_response"] = "Thank you for your time. Have a great day!"
    
    # Signal that this conversation has ended and a new session should start
    state["conversation_ended"] = True
    state["new_session_required"] = True
    
    # The graph will terminate after this node because there are no outgoing edges
    return state

