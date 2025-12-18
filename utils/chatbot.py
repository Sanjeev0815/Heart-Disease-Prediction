import streamlit as st

class HeartHealthChatbot:
    def __init__(self):
        self.knowledge_base = {
            'risk_score': {
                'keywords': ['risk score', 'prediction', 'what does', 'mean', 'score'],
                'response': """Your heart disease risk score is a probability estimate between 0-100% that indicates your likelihood of having heart disease based on various health factors. 

- **Low Risk (0-30%)**: Your heart health appears good. Continue maintaining healthy habits.
- **Medium Risk (30-70%)**: Some factors may be concerning. Consider lifestyle modifications.
- **High Risk (70-100%)**: Several risk factors detected. Consult a healthcare professional soon.

The score is based on age, blood pressure, cholesterol, and other medical factors analyzed by machine learning models."""
            },
            'improve_health': {
                'keywords': ['improve', 'better', 'reduce risk', 'lower', 'healthier'],
                'response': """Here are key ways to improve your heart health:

**Diet & Nutrition:**
- Eat more fruits, vegetables, and whole grains
- Choose lean proteins (fish, chicken, legumes)
- Limit saturated fats, salt, and processed foods
- Control portion sizes

**Physical Activity:**
- Aim for 150 minutes of moderate exercise per week
- Include both cardio and strength training
- Start slowly if you're not active now

**Lifestyle Changes:**
- Quit smoking if you smoke
- Limit alcohol consumption
- Manage stress through relaxation techniques
- Get 7-8 hours of quality sleep

**Medical Management:**
- Take prescribed medications as directed
- Monitor blood pressure and cholesterol regularly
- Attend regular check-ups with your doctor"""
            },
            'lifestyle': {
                'keywords': ['lifestyle', 'changes', 'habits', 'daily'],
                'response': """Essential lifestyle changes for heart health:

1. **Nutrition**: Follow a heart-healthy diet rich in vegetables, fruits, whole grains, and lean proteins.

2. **Exercise**: Regular physical activity (30 minutes most days) strengthens your heart.

3. **Weight Management**: Maintain a healthy BMI through balanced diet and exercise.

4. **Stress Management**: Practice meditation, yoga, or other relaxation techniques.

5. **Sleep**: Get adequate quality sleep (7-8 hours nightly).

6. **Avoid Tobacco**: Quit smoking and avoid secondhand smoke.

7. **Limit Alcohol**: If you drink, do so in moderation.

8. **Monitor Health**: Regular check-ups and track your vitals.

Small, consistent changes make the biggest difference over time!"""
            },
            'doctor': {
                'keywords': ['doctor', 'physician', 'see a', 'medical help', 'consult'],
                'response': """You should see a doctor if you experience:

**Immediate/Emergency (Call 911):**
- Severe chest pain or pressure
- Difficulty breathing or shortness of breath
- Pain radiating to arm, jaw, or back
- Sudden severe headache or dizziness
- Loss of consciousness

**Schedule Appointment Soon:**
- Persistent fatigue or weakness
- Irregular heartbeat or palpitations
- Swelling in legs, ankles, or feet
- Unexplained weight gain
- High risk score from this assessment

**Regular Check-ups:**
- Annual physical examinations
- Blood pressure and cholesterol monitoring
- Review of medications and symptoms
- Discuss prevention strategies

Always consult healthcare professionals for medical decisions. This tool provides information only."""
            },
            'warning_signs': {
                'keywords': ['warning', 'signs', 'symptoms', 'indicators'],
                'response': """Common warning signs of heart disease:

**Chest Discomfort:**
- Pressure, squeezing, or pain in the chest
- May feel like indigestion or heartburn

**Breathing Problems:**
- Shortness of breath during activity or rest
- Difficulty breathing when lying down

**Circulation Issues:**
- Pain, numbness, or coldness in extremities
- Swelling in legs, ankles, or feet

**Other Symptoms:**
- Rapid or irregular heartbeat
- Persistent fatigue or weakness
- Dizziness or lightheadedness
- Nausea or loss of appetite

**Women May Experience:**
- Extreme fatigue
- Sleep disturbances
- Indigestion or stomach discomfort

If you experience any severe symptoms, seek immediate medical attention. Don't ignore warning signs!"""
            },
            'exercise': {
                'keywords': ['exercise', 'physical activity', 'workout', 'fitness'],
                'response': """Exercise is crucial for heart health:

**Benefits:**
- Strengthens heart muscle
- Improves circulation
- Lowers blood pressure
- Reduces cholesterol
- Helps maintain healthy weight
- Reduces stress

**Recommended Activities:**
- Brisk walking (easiest to start)
- Swimming or water aerobics
- Cycling (stationary or outdoor)
- Dancing
- Gardening or yard work

**Guidelines:**
- Start slowly and increase gradually
- Aim for 150 minutes moderate activity per week
- Include warm-up and cool-down
- Listen to your body
- Stay hydrated

**Safety Tips:**
- Consult doctor before starting new routine
- Stop if you feel chest pain or severe breathlessness
- Monitor heart rate during exercise
- Choose activities you enjoy for sustainability"""
            },
            'diet': {
                'keywords': ['food', 'diet', 'eat', 'nutrition', 'meal'],
                'response': """Heart-healthy eating guidelines:

**Foods to Include:**
- Vegetables and fruits (5+ servings daily)
- Whole grains (brown rice, oats, whole wheat)
- Lean proteins (fish, chicken, beans)
- Healthy fats (olive oil, nuts, avocados)
- Low-fat dairy products

**Foods to Limit:**
- Saturated and trans fats
- Sodium/salt (under 2,300mg daily)
- Added sugars
- Processed and fried foods
- Red meat (limit to occasional)

**Specific Recommendations:**
- Eat fish twice weekly (salmon, mackerel)
- Choose fiber-rich foods
- Read nutrition labels carefully
- Control portion sizes
- Drink plenty of water

**Cooking Tips:**
- Bake, grill, or steam instead of frying
- Use herbs and spices instead of salt
- Prepare meals at home when possible
- Plan meals ahead to make better choices"""
            },
            'stress': {
                'keywords': ['stress', 'anxiety', 'mental', 'emotional'],
                'response': """Stress significantly affects heart health:

**How Stress Harms Your Heart:**
- Raises blood pressure
- Increases inflammation
- May lead to unhealthy coping behaviors
- Affects sleep quality
- Can trigger irregular heartbeat

**Stress Management Techniques:**

1. **Relaxation Practices:**
   - Deep breathing exercises
   - Progressive muscle relaxation
   - Meditation or mindfulness

2. **Physical Activity:**
   - Regular exercise reduces stress hormones
   - Yoga combines movement and relaxation

3. **Healthy Habits:**
   - Maintain regular sleep schedule
   - Eat balanced meals
   - Limit caffeine and alcohol

4. **Social Support:**
   - Connect with friends and family
   - Join support groups
   - Consider professional counseling

5. **Time Management:**
   - Prioritize tasks
   - Set realistic goals
   - Take regular breaks

Remember: Managing stress is as important as diet and exercise for heart health!"""
            },
            'cholesterol': {
                'keywords': ['cholesterol', 'lipid', 'hdl', 'ldl'],
                'response': """Understanding cholesterol and heart health:

**Types of Cholesterol:**
- **LDL (Bad)**: Should be <100 mg/dL. Builds up in arteries.
- **HDL (Good)**: Should be >60 mg/dL. Removes cholesterol from arteries.
- **Total**: Should be <200 mg/dL.
- **Triglycerides**: Should be <150 mg/dL.

**How to Lower Cholesterol:**

**Diet Changes:**
- Reduce saturated fats (butter, red meat)
- Avoid trans fats (processed foods)
- Eat more fiber (oats, beans, apples)
- Include omega-3 fatty acids (fish, walnuts)

**Lifestyle:**
- Maintain healthy weight
- Exercise regularly (30+ min daily)
- Quit smoking
- Limit alcohol

**Medical Treatment:**
- Statins or other medications if prescribed
- Regular monitoring with blood tests

High cholesterol often has no symptoms, so regular testing is important!"""
            },
            'blood_pressure': {
                'keywords': ['blood pressure', 'hypertension', 'bp'],
                'response': """Blood pressure and heart disease:

**Understanding Readings:**
- **Normal**: <120/80 mmHg
- **Elevated**: 120-129/<80 mmHg
- **High Stage 1**: 130-139/80-89 mmHg
- **High Stage 2**: ≥140/90 mmHg

**How to Lower Blood Pressure:**

**Dietary Approaches:**
- Reduce sodium (under 2,300mg daily)
- Follow DASH diet (fruits, vegetables, low-fat dairy)
- Limit alcohol
- Increase potassium-rich foods

**Lifestyle Changes:**
- Lose excess weight (even 5-10 lbs helps)
- Exercise regularly
- Manage stress
- Get adequate sleep
- Quit smoking

**Monitoring:**
- Check BP regularly at home
- Keep a log of readings
- Share results with doctor

**Medications:**
- Take as prescribed
- Don't skip doses
- Report side effects to doctor

Uncontrolled high blood pressure is a major heart disease risk factor!"""
            }
        }
    
    def get_response(self, user_message, context=None):
        """Get chatbot response based on keywords"""
        user_message_lower = user_message.lower()
        
        # Check for matches in knowledge base
        for topic, data in self.knowledge_base.items():
            if any(keyword in user_message_lower for keyword in data['keywords']):
                response = data['response']
                
                # Add context-specific information if available
                if context and 'high risk' in context.lower():
                    response += "\n\n**Note:** Your assessment shows elevated risk. Please consult a healthcare professional for personalized guidance."
                elif context and 'medium risk' in context.lower():
                    response += "\n\n**Note:** Your assessment shows moderate risk. Implementing lifestyle changes could be beneficial."
                
                return response
        
        # Default response if no match found
        default_response = """I can help you understand heart health and your risk assessment. Here are some topics I can discuss:

- Understanding your risk score and what it means
- Ways to improve heart health and reduce risk
- Lifestyle changes for better cardiovascular health
- When to see a doctor
- Warning signs of heart disease
- Exercise and heart health
- Heart-healthy diet and nutrition
- Stress management

Please ask me about any of these topics, and I'll provide detailed information!"""
        
        return default_response
    
    def get_prediction_explanation(self, prediction_score, risk_category, top_factors):
        """Get explanation for prediction results"""
        explanation = f"""**Your Heart Disease Risk Assessment:**

**Risk Score:** {prediction_score:.1%}
**Category:** {risk_category}

"""
        
        if risk_category == "Low Risk":
            explanation += """**What This Means:**
Your assessment suggests a lower probability of heart disease. This is encouraging! Continue maintaining your healthy habits.

**Next Steps:**
- Keep up with regular health check-ups
- Maintain a heart-healthy lifestyle
- Monitor your vitals periodically
- Stay physically active
"""
        elif risk_category == "Medium Risk":
            explanation += """**What This Means:**
Your assessment shows moderate risk. Some health factors may need attention, but there's significant room for improvement.

**Next Steps:**
- Discuss results with your healthcare provider
- Focus on modifiable risk factors
- Implement lifestyle changes (diet, exercise)
- Monitor blood pressure and cholesterol
- Consider stress management techniques
"""
        else:  # High Risk
            explanation += """**What This Means:**
Your assessment indicates elevated risk. This doesn't mean you have heart disease, but several risk factors need attention.

**Immediate Actions:**
- **Consult a healthcare professional soon** for comprehensive evaluation
- Discuss these results with your doctor
- Get recommended tests (ECG, stress test, etc.)
- Review medications and treatment options

**Lifestyle Modifications:**
- Make heart-healthy diet changes
- Increase physical activity (as approved by doctor)
- Quit smoking if applicable
- Manage stress and get adequate sleep
"""
        
        if top_factors:
            explanation += f"\n**Key Contributing Factors:** {', '.join(top_factors)}\n"
            explanation += "\nFocusing on these areas could help improve your heart health.\n"
        
        explanation += "\n**Important:** This assessment provides information only. Always consult healthcare professionals for medical decisions."
        
        return explanation
    
    def get_lifestyle_recommendations(self, risk_factors):
        """Get personalized lifestyle recommendations"""
        recommendations = """**Personalized Lifestyle Recommendations:**

"""
        
        if 'high cholesterol' in [rf.lower() for rf in risk_factors]:
            recommendations += """**For High Cholesterol:**
- Reduce saturated fats (red meat, butter, cheese)
- Increase fiber intake (oats, beans, fruits)
- Add omega-3 rich foods (salmon, walnuts)
- Choose lean proteins and low-fat dairy

"""
        
        if 'high blood pressure' in [rf.lower() for rf in risk_factors]:
            recommendations += """**For High Blood Pressure:**
- Limit sodium to under 2,300mg daily
- Follow DASH diet (fruits, vegetables, whole grains)
- Maintain healthy weight
- Practice stress reduction techniques
- Limit alcohol and avoid tobacco

"""
        
        if 'exercise intolerance' in [rf.lower() for rf in risk_factors]:
            recommendations += """**For Exercise Intolerance:**
- Start with light activities (walking, swimming)
- Gradually increase duration and intensity
- Include rest days for recovery
- Consult doctor before starting new routines
- Monitor heart rate during activity

"""
        
        recommendations += """**General Heart-Healthy Habits:**
- Get 7-8 hours of quality sleep
- Manage stress through relaxation techniques
- Stay socially connected
- Keep regular medical appointments
- Track your health metrics

**Remember:** Small, consistent changes lead to lasting improvements. Start with one or two changes and build from there!

Consult your healthcare provider before making major lifestyle changes, especially if you have existing health conditions."""
        
        return recommendations
    
    def get_symptom_guidance(self, symptoms):
        """Get guidance for reported symptoms"""
        symptoms_lower = symptoms.lower()
        
        emergency_keywords = ['severe', 'chest pain', 'difficulty breathing', 'unconscious', 'crushing']
        urgent_keywords = ['pain', 'shortness of breath', 'dizzy', 'irregular heartbeat', 'palpitation']
        
        response = "**Symptom Guidance:**\n\n"
        
        # Check for emergency symptoms
        if any(keyword in symptoms_lower for keyword in emergency_keywords):
            response += """🚨 **EMERGENCY:** Your symptoms may require immediate medical attention!

**Call 911 or go to the emergency room immediately if you have:**
- Severe chest pain or pressure
- Difficulty breathing
- Pain radiating to arm, jaw, or back
- Loss of consciousness
- Severe dizziness or confusion

**Do not drive yourself. Call emergency services now!**

This is NOT a substitute for emergency medical care.
"""
            return response
        
        # Check for urgent symptoms
        if any(keyword in symptoms_lower for keyword in urgent_keywords):
            response += """⚠️ **Important:** Your symptoms warrant medical evaluation.

**You should contact your healthcare provider soon if experiencing:**
- Chest discomfort or unusual sensations
- Shortness of breath
- Irregular or rapid heartbeat
- Persistent dizziness or lightheadedness

**In the meantime:**
- Rest and avoid strenuous activity
- Monitor your symptoms
- Note when symptoms occur and what triggers them
- Seek immediate help if symptoms worsen

"""
        
        response += """**General Symptom Information:**

Common heart-related symptoms include:
- Chest pressure or discomfort
- Shortness of breath
- Fatigue or weakness
- Palpitations or irregular heartbeat
- Swelling in legs or ankles
- Dizziness or lightheadedness

**What to do:**
1. Keep a symptom diary (when, duration, triggers)
2. Note any activities that worsen symptoms
3. Share all symptoms with your doctor
4. Don't ignore persistent or worsening symptoms

**Important Reminders:**
- This is educational information only
- Always consult healthcare professionals for diagnosis
- When in doubt, seek medical attention
- Better safe than sorry with heart symptoms!

Would you like information about any specific aspect of heart health?"""
        
        return response
    
    def stream_response(self, user_message, context=None):
        """Stream chatbot response for better UX"""
        response = self.get_response(user_message, context)
        
        # Simulate streaming by yielding in chunks
        words = response.split()
        current_chunk = ""
        
        for i, word in enumerate(words):
            current_chunk += word + " "
            if (i + 1) % 3 == 0 or i == len(words) - 1:  # Yield every 3 words
                yield current_chunk
                current_chunk = ""

def initialize_chatbot():
    """Initialize chatbot in session state"""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = HeartHealthChatbot()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def add_to_chat_history(role, message):
    """Add message to chat history"""
    st.session_state.chat_history.append({
        "role": role,
        "message": message,
        "timestamp": st.session_state.get('timestamp_counter', 0)
    })
    st.session_state.timestamp_counter = st.session_state.get('timestamp_counter', 0) + 1

def display_chat_history():
    """Display chat history"""
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            with st.chat_message("user"):
                st.write(chat["message"])
        else:
            with st.chat_message("assistant"):
                st.write(chat["message"])

def get_contextual_suggestions():
    """Get contextual quick questions based on app state"""
    suggestions = [
        "What does my heart disease risk score mean?",
        "How can I improve my heart health?",
        "What lifestyle changes should I make?",
        "When should I see a doctor?",
        "What are the warning signs of heart disease?",
        "How does exercise affect heart health?",
        "What foods are good for heart health?",
        "How does stress affect my heart?"
    ]
    
    # Add context-specific suggestions based on session state
    if 'latest_prediction' in st.session_state:
        risk_category = st.session_state.latest_prediction.get('risk_category', '')
        if risk_category == 'High Risk':
            suggestions.insert(0, "I have high risk - what should I do immediately?")
        elif risk_category == 'Medium Risk':
            suggestions.insert(0, "How can I reduce my medium risk level?")
    
    return suggestions
