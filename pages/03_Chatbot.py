import streamlit as st
from utils.chatbot import initialize_chatbot, add_to_chat_history, display_chat_history, get_contextual_suggestions

st.set_page_config(page_title="AI Health Chatbot", page_icon="H", layout="wide")

st.title("AI Health Chatbot")
st.markdown("Get personalized guidance and answers about your heart health from our AI assistant.")

# Initialize chatbot
initialize_chatbot()

# Main chat interface
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Chat with HeartSafe AI")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        display_chat_history()
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about heart health..."):
            # Add user message to history
            add_to_chat_history("user", prompt)
            
            # Display user message
            with st.chat_message("user"):
                st.write(prompt)
            
            # Generate context from latest prediction if available
            context = None
            if 'latest_prediction' in st.session_state:
                latest = st.session_state['latest_prediction']
                context = f"""
                Latest prediction: {latest['score']:.1%} risk ({latest['category']})
                Model used: {latest['model']}
                Key health metrics: Age {latest['input_data'].get('age')}, 
                BP {latest['input_data'].get('resting_bp')}, 
                Cholesterol {latest['input_data'].get('cholesterol')}
                """
            
            # Generate and display AI response
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                
                # Stream response
                response_text = ""
                for chunk in st.session_state.chatbot.stream_response(prompt, context):
                    response_text += chunk
                    response_placeholder.write(response_text)
                
                # Add assistant response to history
                add_to_chat_history("assistant", response_text)

with col2:
    st.subheader("Quick Questions")
    
    # Get contextual suggestions
    suggestions = get_contextual_suggestions()
    
    st.markdown("**Common Questions:**")
    
    for suggestion in suggestions[:8]:  # Show top 8 suggestions
        if st.button(suggestion, key=f"suggestion_{suggestion[:20]}", use_container_width=True):
            # Add suggestion to chat
            add_to_chat_history("user", suggestion)
            
            # Generate context
            context = None
            if 'latest_prediction' in st.session_state:
                latest = st.session_state['latest_prediction']
                context = f"""
                Latest prediction: {latest['score']:.1%} risk ({latest['category']})
                Model used: {latest['model']}
                """
            
            # Get response
            response = st.session_state.chatbot.get_response(suggestion, context)
            add_to_chat_history("assistant", response)
            
            # Rerun to update chat
            st.rerun()
    
    st.markdown("---")
    
    # Specialized features
    st.subheader("Specialized Features")
    
    if st.button("Explain My Prediction", use_container_width=True):
        if 'latest_prediction' in st.session_state:
            latest = st.session_state['latest_prediction']
            
            # Get top risk factors (simplified)
            input_data = latest['input_data']
            top_factors = []
            
            if input_data.get('age', 0) > 55:
                top_factors.append("Age")
            if input_data.get('cholesterol', 0) > 240:
                top_factors.append("High Cholesterol")
            if input_data.get('resting_bp', 0) > 140:
                top_factors.append("High Blood Pressure")
            
            explanation = st.session_state.chatbot.get_prediction_explanation(
                latest['score'], 
                latest['category'], 
                top_factors
            )
            
            add_to_chat_history("user", "Please explain my heart disease prediction")
            add_to_chat_history("assistant", explanation)
            st.rerun()
        else:
            st.warning("Make a prediction first to get an explanation.")
    
    if st.button("Get Lifestyle Tips", use_container_width=True):
        if 'latest_prediction' in st.session_state:
            latest = st.session_state['latest_prediction']
            input_data = latest['input_data']
            
            # Identify risk factors
            risk_factors = []
            if input_data.get('cholesterol', 0) > 240:
                risk_factors.append("high cholesterol")
            if input_data.get('resting_bp', 0) > 140:
                risk_factors.append("high blood pressure")
            if input_data.get('exercise_angina', 0) == 1:
                risk_factors.append("exercise intolerance")
            
            tips = st.session_state.chatbot.get_lifestyle_recommendations(risk_factors)
            
            add_to_chat_history("user", "What lifestyle changes should I make?")
            add_to_chat_history("assistant", tips)
            st.rerun()
        else:
            st.warning("Make a prediction first to get personalized tips.")
    
    # Symptom checker
    st.markdown("---")
    st.subheader("Symptom Checker")
    
    symptoms = st.text_area(
        "Describe any symptoms you're experiencing:",
        placeholder="e.g., chest pain, shortness of breath, fatigue...",
        height=100
    )
    
    if st.button("Analyze Symptoms", use_container_width=True):
        if symptoms:
            response = st.session_state.chatbot.get_symptom_guidance(symptoms)
            
            add_to_chat_history("user", f"I'm experiencing: {symptoms}")
            add_to_chat_history("assistant", response)
            st.rerun()
        else:
            st.warning("Please describe your symptoms first.")

# Chat statistics and controls
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.success("Chat history cleared!")
        st.rerun()

with col2:
    total_messages = len(st.session_state.get('chat_history', []))
    st.metric("Total Messages", total_messages)

with col3:
    user_messages = len([msg for msg in st.session_state.get('chat_history', []) if msg['role'] == 'user'])
    st.metric("Your Messages", user_messages)

# Help section
with st.expander("How to use the AI Chatbot"):
    st.markdown("""
    **The AI Health Chatbot can help you with:**
    
    - Understanding your heart disease risk prediction
    - Explaining medical terms and concepts
    - Providing lifestyle and dietary recommendations
    - Answering general heart health questions
    - Analyzing symptoms (for informational purposes)
    - Suggesting when to seek professional medical care
    
    **Important Notes:**
    - This chatbot provides educational information only
    - Always consult healthcare professionals for medical decisions
    - In case of emergency symptoms, seek immediate medical attention
    - The AI uses your latest prediction data to provide personalized responses
    
    **Tips for better responses:**
    - Be specific about your questions
    - Mention relevant symptoms or concerns
    - Ask follow-up questions for clarification
    - Use the quick questions for common topics
    """)

# Emergency notice
st.error("""
**EMERGENCY NOTICE:** If you're experiencing severe chest pain, difficulty breathing, 
or other emergency symptoms, call emergency services immediately. This chatbot is not 
a substitute for emergency medical care.
""")
