import streamlit as st
import pandas as pd
import numpy as np
from utils.storage import get_vitals_history, save_vitals
from utils.models import get_risk_category
import plotly.express as px

st.set_page_config(page_title="Health Recommendations", page_icon="H", layout="wide")

st.title("Personalized Health Recommendations")
st.markdown("Get evidence-based recommendations tailored to your heart disease risk factors and health profile.")

# Check if we have prediction data
if 'latest_prediction' not in st.session_state:
    st.warning("Please make a prediction first to get personalized recommendations.")
    if st.button("Make Prediction"):
        st.switch_page("pages/01_Prediction.py")
    st.stop()

latest_prediction = st.session_state['latest_prediction']
risk_score = latest_prediction['score']
risk_category = latest_prediction['category']
input_data = latest_prediction['input_data']

# Header with current risk status
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current Risk Score", f"{risk_score:.1%}")
with col2:
    st.metric("Risk Category", risk_category)
with col3:
    priority_level = "HIGH" if risk_score > 0.7 else "MEDIUM" if risk_score > 0.3 else "LOW"
    st.metric("Priority Level", priority_level)

# Risk-based alert
if risk_category == "High Risk":
    st.error(" **High Risk Detected**: These recommendations are critical for your heart health. Please consult with a healthcare professional immediately.")
elif risk_category == "Medium Risk":
    st.warning(" **Moderate Risk**: Following these recommendations can significantly improve your heart health.")
else:
    st.success(" **Low Risk**: Maintain these healthy habits to keep your heart disease risk low.")

# Generate recommendations based on risk factors
st.markdown("---")

def analyze_risk_factors(input_data):
    """Analyze input data to identify specific risk factors"""
    risk_factors = []
    recommendations = {
        'immediate': [],
        'lifestyle': [],
        'dietary': [],
        'exercise': [],
        'medical': [],
        'monitoring': []
    }
    
    # Blood pressure analysis
    bp = input_data.get('resting_bp', 120)
    if bp >= 140:
        risk_factors.append('High Blood Pressure')
        recommendations['immediate'].append("Monitor blood pressure daily and consult healthcare provider")
        recommendations['lifestyle'].append("Reduce sodium intake to less than 2,300mg per day")
        recommendations['exercise'].append("Engage in 30 minutes of moderate aerobic activity 5 days per week")
    elif bp >= 130:
        risk_factors.append('Elevated Blood Pressure')
        recommendations['lifestyle'].append("Limit sodium intake and manage stress levels")
        recommendations['exercise'].append("Increase physical activity to 150 minutes per week")
    
    # Cholesterol analysis
    chol = input_data.get('cholesterol', 200)
    if chol >= 240:
        risk_factors.append('High Cholesterol')
        recommendations['immediate'].append("Schedule lipid panel and cardiology consultation")
        recommendations['dietary'].append("Follow a heart-healthy diet low in saturated fats")
        recommendations['dietary'].append("Increase fiber intake with whole grains, fruits, and vegetables")
    elif chol >= 200:
        risk_factors.append('Borderline High Cholesterol')
        recommendations['dietary'].append("Reduce saturated fat intake to less than 7% of daily calories")
        recommendations['dietary'].append("Include omega-3 rich foods like fish twice per week")
    
    # Age factor
    age = input_data.get('age', 50)
    if age >= 65:
        risk_factors.append('Advanced Age')
        recommendations['medical'].append("Schedule annual comprehensive cardiac evaluation")
        recommendations['monitoring'].append("Monitor blood pressure and cholesterol every 6 months")
    elif age >= 55:
        risk_factors.append('Increased Age Risk')
        recommendations['monitoring'].append("Annual cardiac risk assessment recommended")
    
    # Heart rate and fitness
    max_hr = input_data.get('max_heart_rate', 150)
    predicted_max = 220 - age
    if max_hr < (predicted_max * 0.7):
        risk_factors.append('Poor Cardiovascular Fitness')
        recommendations['exercise'].append("Start with low-impact exercises and gradually increase intensity")
        recommendations['exercise'].append("Consider cardiac rehabilitation program evaluation")
    
    # Diabetes indicator
    if input_data.get('fasting_blood_sugar', 0) == 1:
        risk_factors.append('Diabetes/High Blood Sugar')
        recommendations['immediate'].append("Optimize diabetes management with healthcare provider")
        recommendations['dietary'].append("Follow diabetic diet guidelines and monitor blood sugar regularly")
        recommendations['monitoring'].append("HbA1c testing every 3-6 months")
    
    # Chest pain analysis
    chest_pain = input_data.get('chest_pain_type', 4)
    if chest_pain in [1, 2]:
        risk_factors.append('Chest Pain Symptoms')
        recommendations['immediate'].append("Report any chest pain episodes to healthcare provider immediately")
        recommendations['lifestyle'].append("Learn to recognize cardiac emergency symptoms")
    
    # Exercise tolerance
    if input_data.get('exercise_angina', 0) == 1:
        risk_factors.append('Exercise Intolerance')
        recommendations['immediate'].append("Cardiac stress test and exercise prescription needed")
        recommendations['exercise'].append("Supervised exercise program recommended initially")
    
    # ECG abnormalities
    if input_data.get('rest_ecg', 0) != 0:
        risk_factors.append('ECG Abnormalities')
        recommendations['medical'].append("Regular cardiac monitoring and follow-up ECGs")
        recommendations['monitoring'].append("Annual echocardiogram to assess heart function")
    
    return risk_factors, recommendations

risk_factors, recommendations = analyze_risk_factors(input_data)

# Display identified risk factors
st.subheader("Identified Risk Factors")
if risk_factors:
    cols = st.columns(min(len(risk_factors), 3))
    for i, factor in enumerate(risk_factors):
        with cols[i % 3]:
            st.error(f" {factor}")
else:
    st.success("No major modifiable risk factors identified!")

# Recommendations by category
st.markdown("---")
st.subheader("Personalized Recommendations")

# Immediate actions (if any)
if recommendations['immediate']:
    st.markdown("###  Immediate Actions Required")
    for rec in recommendations['immediate']:
        st.error(f"• {rec}")

# Create tabs for different recommendation categories
lifestyle_tab, diet_tab, exercise_tab, medical_tab, monitoring_tab = st.tabs([
    "Lifestyle Changes", "Dietary Guidelines", "Exercise Program", "Medical Care", "Health Monitoring"
])

with lifestyle_tab:
    st.markdown("### Lifestyle Modifications")
    
    if recommendations['lifestyle']:
        for rec in recommendations['lifestyle']:
            st.write(f"• {rec}")
    
    # General lifestyle recommendations based on risk level
    st.markdown("#### General Recommendations:")
    
    lifestyle_recs = [
        "Quit smoking completely if you currently smoke",
        "Limit alcohol consumption to moderate levels (1-2 drinks per day for men, 1 for women)",
        "Maintain a healthy sleep schedule (7-9 hours per night)",
        "Practice stress management techniques (meditation, deep breathing, yoga)",
        "Maintain social connections and mental health support"
    ]
    
    if risk_category == "High Risk":
        lifestyle_recs.extend([
            "Consider joining a cardiac support group",
            "Create an emergency action plan with family members",
            "Keep emergency medications readily available"
        ])
    
    for rec in lifestyle_recs:
        st.write(f"• {rec}")

with diet_tab:
    st.markdown("### Heart-Healthy Diet Plan")
    
    if recommendations['dietary']:
        st.markdown("#### Specific to Your Risk Factors:")
        for rec in recommendations['dietary']:
            st.write(f"• {rec}")
    
    st.markdown("#### Mediterranean Diet Guidelines:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("** Foods to Include:**")
        good_foods = [
            "Fatty fish (salmon, mackerel, sardines) - 2-3 times per week",
            "Whole grains (oats, quinoa, brown rice)",
            "Fresh fruits and vegetables (5-9 servings daily)",
            "Nuts and seeds (almonds, walnuts, flaxseeds)",
            "Olive oil as primary cooking fat",
            "Legumes (beans, lentils, chickpeas)",
            "Low-fat dairy products",
            "Herbs and spices instead of salt"
        ]
        for food in good_foods:
            st.write(f"• {food}")
    
    with col2:
        st.markdown("** Foods to Limit/Avoid:**")
        avoid_foods = [
            "Red meat and processed meats",
            "Trans fats and hydrogenated oils",
            "Refined sugars and sweets",
            "Processed and packaged foods",
            "Excessive sodium (>2,300mg daily)",
            "Sugary beverages and alcohol excess",
            "Fried and fast foods",
            "Full-fat dairy products"
        ]
        for food in avoid_foods:
            st.write(f"• {food}")
    
    # Sample meal plan
    with st.expander("Sample Daily Meal Plan"):
        st.markdown("""
        **Breakfast:**
        - Oatmeal with berries and chopped walnuts
        - Green tea or coffee (limit caffeine)
        
        **Lunch:**
        - Grilled salmon with quinoa and steamed vegetables
        - Mixed green salad with olive oil dressing
        
        **Snack:**
        - Apple slices with almond butter
        - Handful of unsalted nuts
        
        **Dinner:**
        - Lean chicken breast with sweet potato
        - Sautéed spinach with garlic
        - Small portion of brown rice
        
        **Hydration:** 8-10 glasses of water daily
        """)

with exercise_tab:
    st.markdown("### Exercise Program")
    
    if recommendations['exercise']:
        st.markdown("#### Specific to Your Condition:")
        for rec in recommendations['exercise']:
            st.write(f"• {rec}")
    
    # Exercise recommendations based on current fitness level
    max_hr = input_data.get('max_heart_rate', 150)
    age = input_data.get('age', 50)
    predicted_max = 220 - age
    fitness_level = "Good" if max_hr >= (predicted_max * 0.8) else "Fair" if max_hr >= (predicted_max * 0.7) else "Needs Improvement"
    
    st.info(f"Current Fitness Level: {fitness_level}")
    
    # Tailored exercise plan
    if fitness_level == "Needs Improvement":
        st.markdown("#### Beginner Exercise Program (Weeks 1-4):")
        beginner_plan = [
            "Walking: Start with 10-15 minutes daily, increase by 2-3 minutes weekly",
            "Light resistance training: 2 days per week with light weights",
            "Stretching: 5-10 minutes daily focusing on major muscle groups",
            "Chair exercises if mobility is limited",
            "Water aerobics or swimming if available"
        ]
    elif fitness_level == "Fair":
        st.markdown("#### Intermediate Exercise Program:")
        beginner_plan = [
            "Brisk walking or light jogging: 30 minutes, 5 days per week",
            "Resistance training: 2-3 days per week with moderate weights",
            "Flexibility training: 10-15 minutes daily",
            "Low-impact activities: cycling, swimming, elliptical",
            "Group fitness classes: low-impact aerobics, yoga"
        ]
    else:
        st.markdown("#### Advanced Exercise Program:")
        beginner_plan = [
            "Varied cardio: 45-60 minutes, 5-6 days per week",
            "Strength training: 3-4 days per week with progressive overload",
            "High-intensity interval training (HIIT): 1-2 sessions per week",
            "Sports activities: tennis, basketball, swimming",
            "Advanced yoga or Pilates classes"
        ]
    
    for plan_item in beginner_plan:
        st.write(f"• {plan_item}")
    
    # Exercise precautions
    st.markdown("#### Exercise Safety Guidelines:")
    safety_tips = [
        "Always warm up for 5-10 minutes before exercising",
        "Monitor heart rate and stay within target zone",
        "Stop exercising if you experience chest pain, dizziness, or shortness of breath",
        "Cool down with 5-10 minutes of light activity and stretching",
        "Stay hydrated before, during, and after exercise",
        "Progress gradually - increase intensity by no more than 10% per week"
    ]
    
    for tip in safety_tips:
        st.write(f"• {tip}")

with medical_tab:
    st.markdown("### Medical Care & Follow-up")
    
    if recommendations['medical']:
        st.markdown("#### Specific Medical Actions:")
        for rec in recommendations['medical']:
            st.write(f"• {rec}")
    
    st.markdown("#### Recommended Healthcare Team:")
    
    healthcare_team = []
    if risk_category == "High Risk":
        healthcare_team = [
            "Cardiologist - Primary cardiac care and treatment planning",
            "Primary Care Physician - Overall health management and coordination",
            "Registered Dietitian - Nutrition counseling and meal planning",
            "Exercise Physiologist - Safe exercise prescription and monitoring",
            "Pharmacist - Medication management and interactions",
            "Mental Health Counselor - Stress management and lifestyle support"
        ]
    elif risk_category == "Medium Risk":
        healthcare_team = [
            "Primary Care Physician - Regular monitoring and prevention strategies",
            "Cardiologist - Annual evaluation and risk assessment",
            "Registered Dietitian - Nutrition guidance for heart health",
            "Exercise Specialist - Safe exercise program development"
        ]
    else:
        healthcare_team = [
            "Primary Care Physician - Annual check-ups and prevention",
            "Preventive Care Specialist - Risk factor modification guidance"
        ]
    
    for team_member in healthcare_team:
        st.write(f"• {team_member}")
    
    # Medication considerations
    st.markdown("#### Potential Medication Discussions:")
    med_discussions = [
        "Blood pressure medications (ACE inhibitors, beta-blockers) if BP elevated",
        "Cholesterol-lowering medications (statins) if cholesterol high",
        "Aspirin therapy for cardiovascular protection (discuss with doctor)",
        "Diabetes medications if blood sugar elevated",
        "Heart rhythm medications if ECG abnormalities present"
    ]
    
    for med in med_discussions:
        st.write(f"• {med}")
    
    st.warning(" Never start or stop medications without consulting your healthcare provider.")

with monitoring_tab:
    st.markdown("### Health Monitoring Plan")
    
    if recommendations['monitoring']:
        st.markdown("#### Specific Monitoring Needs:")
        for rec in recommendations['monitoring']:
            st.write(f"• {rec}")
    
    st.markdown("#### Regular Health Tracking:")
    
    # Monitoring frequency based on risk
    if risk_category == "High Risk":
        monitoring_plan = {
            "Daily": ["Blood pressure", "Weight", "Symptoms diary", "Medication compliance"],
            "Weekly": ["Exercise minutes", "Diet compliance", "Stress levels"],
            "Monthly": ["Overall assessment", "Goal review", "Healthcare provider contact"],
            "Every 3 months": ["Blood tests (lipids, glucose)", "Healthcare provider visit"],
            "Every 6 months": ["Comprehensive cardiac evaluation", "ECG", "Echocardiogram if needed"]
        }
    elif risk_category == "Medium Risk":
        monitoring_plan = {
            "Daily": ["Blood pressure (if elevated)", "Symptoms awareness"],
            "Weekly": ["Weight", "Exercise tracking", "Diet assessment"],
            "Monthly": ["Progress review", "Goal adjustment"],
            "Every 6 months": ["Blood tests", "Healthcare provider visit"],
            "Annually": ["Comprehensive physical", "Cardiac risk assessment"]
        }
    else:
        monitoring_plan = {
            "Weekly": ["Exercise tracking", "Weight maintenance"],
            "Monthly": ["Health habits review"],
            "Every 6 months": ["Basic health metrics"],
            "Annually": ["Complete physical exam", "Blood tests", "Cardiac screening"]
        }
    
    for frequency, items in monitoring_plan.items():
        st.markdown(f"**{frequency}:**")
        for item in items:
            st.write(f"• {item}")
        st.write("")

# Progress tracking and goal setting
st.markdown("---")
st.subheader("Goal Setting & Progress Tracking")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Short-term Goals (1-3 months):")
    short_goals = []
    
    if input_data.get('resting_bp', 120) > 130:
        short_goals.append("Reduce blood pressure by 5-10 mmHg")
    if input_data.get('cholesterol', 200) > 200:
        short_goals.append("Lower cholesterol by 20-30 mg/dl")
    if input_data.get('max_heart_rate', 150) < 140:
        short_goals.append("Improve exercise capacity by 10-15%")
    
    short_goals.extend([
        "Establish regular exercise routine (3-5 days/week)",
        "Implement heart-healthy diet changes",
        "Achieve and maintain healthy weight",
        "Develop stress management practices"
    ])
    
    for goal in short_goals[:5]:  # Show top 5 goals
        st.write(f"• {goal}")

with col2:
    st.markdown("#### Long-term Goals (6-12 months):")
    long_goals = [
        "Achieve target blood pressure (<120/80 mmHg)",
        "Reach optimal cholesterol levels (<200 mg/dl)",
        "Maintain healthy BMI (18.5-24.9)",
        "Complete cardiac rehabilitation if recommended",
        "Reduce overall cardiovascular risk by 20-30%",
        "Establish sustainable lifestyle habits"
    ]
    
    for goal in long_goals:
        st.write(f"• {goal}")

# Action plan generator
st.markdown("---")
st.subheader("Your Personal Action Plan")

with st.expander("Generate Detailed Action Plan"):
    priority = st.radio("Select your primary focus area:", 
                       ["Blood Pressure Control", "Cholesterol Management", "Weight Loss", "Fitness Improvement", "Overall Heart Health"])
    
    if st.button("Generate Action Plan"):
        st.markdown("### 30-Day Action Plan")
        
        if priority == "Blood Pressure Control":
            action_plan = [
                "Week 1: Start daily BP monitoring and reduce sodium intake",
                "Week 2: Begin 20-minute daily walks and stress reduction techniques",
                "Week 3: Increase exercise to 30 minutes and add meditation",
                "Week 4: Review progress with healthcare provider and adjust medications if needed"
            ]
        elif priority == "Cholesterol Management":
            action_plan = [
                "Week 1: Eliminate trans fats and reduce saturated fats in diet",
                "Week 2: Add 2 servings of fatty fish per week and increase fiber",
                "Week 3: Include plant sterols and increase physical activity",
                "Week 4: Get follow-up lipid panel and review with doctor"
            ]
        elif priority == "Weight Loss":
            action_plan = [
                "Week 1: Track caloric intake and establish 500-calorie daily deficit",
                "Week 2: Add strength training 2x per week to preserve muscle",
                "Week 3: Increase cardio sessions and focus on portion control",
                "Week 4: Reassess weight loss progress and adjust plan accordingly"
            ]
        elif priority == "Fitness Improvement":
            action_plan = [
                "Week 1: Establish baseline with fitness assessment and start walking program",
                "Week 2: Add resistance training and increase walk duration",
                "Week 3: Include interval training and flexibility work",
                "Week 4: Progress assessment and plan for next month's goals"
            ]
        else:  # Overall Heart Health
            action_plan = [
                "Week 1: Comprehensive health assessment and goal setting",
                "Week 2: Implement diet changes and begin exercise routine",
                "Week 3: Add stress management and optimize sleep habits",
                "Week 4: Review all metrics and plan for continued improvement"
            ]
        
        for week_plan in action_plan:
            st.write(f"• {week_plan}")

# Resources and support
st.markdown("---")
st.subheader("Additional Resources")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Educational Resources:")
    resources = [
        "American Heart Association - Heart-Healthy Living Guidelines",
        "Mayo Clinic - Heart Disease Prevention Resources",
        "National Heart, Lung, and Blood Institute - Educational Materials",
        "Academy of Nutrition and Dietetics - Heart-Healthy Recipes",
        "American College of Sports Medicine - Exercise Guidelines"
    ]
    
    for resource in resources:
        st.write(f"• {resource}")

with col2:
    st.markdown("#### Support Options:")
    support_options = [
        "Local cardiac rehabilitation programs",
        "Heart disease support groups",
        "Online communities and forums",
        "Telehealth monitoring services",
        "Mobile apps for heart health tracking",
        "Nutritionist and dietitian consultations"
    ]
    
    for option in support_options:
        st.write(f"• {option}")

# Emergency information
st.markdown("---")
st.error("""
###  When to Seek Emergency Care

Call 911 immediately if you experience:
• Chest pain or discomfort lasting more than a few minutes
• Pain spreading to arms, back, neck, jaw, or stomach
• Shortness of breath with or without chest discomfort
• Breaking out in cold sweat, nausea, or lightheadedness
• Rapid or irregular heartbeat with symptoms
• Sudden severe headache or confusion

**Don't wait - every minute matters in a cardiac emergency!**
""")

# Navigation
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("New Prediction"):
        st.switch_page("pages/01_Prediction.py")

with col2:
    if st.button("Track Progress"):
        st.switch_page("pages/04_Historical_Tracker.py")

with col3:
    if st.button("Medication Tracker"):
        st.switch_page("pages/07_Medication_Tracker.py")

with col4:
    if st.button("Generate Report"):
        st.switch_page("pages/09_Reports.py")
