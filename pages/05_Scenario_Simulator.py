import streamlit as st
import pandas as pd
import numpy as np
from utils.models import make_prediction, get_risk_category
from utils.visualizations import create_risk_gauge
import plotly.graph_objects as go
from copy import deepcopy

st.set_page_config(page_title="What-If Scenario Simulator", page_icon="H", layout="wide")

st.title("What-If Scenario Simulator")
st.markdown("Test how lifestyle changes could affect your heart disease risk. Adjust different factors and see the impact in real-time.")

# Check if models are available and we have baseline data
if 'models' not in st.session_state:
    st.warning("Please upload and train models on the main page first.")
    st.stop()

# Get baseline data from latest prediction or use default
if 'latest_prediction' in st.session_state:
    baseline_data = st.session_state['latest_prediction']['input_data'].copy()
    baseline_risk = st.session_state['latest_prediction']['score']
    st.success("Using your latest prediction as baseline.")
else:
    # Use default baseline
    baseline_data = {
        'age': 50,
        'gender': 1,  # Male
        'chest_pain_type': 3,
        'resting_bp': 130,
        'cholesterol': 240,
        'fasting_blood_sugar': 0,
        'rest_ecg': 0,
        'max_heart_rate': 150,
        'exercise_angina': 0,
        'st_depression': 1.0,
        'st_slope': 2,
        'ca': 0,
        'thal': 2
    }
    baseline_risk, _ = make_prediction(baseline_data)
    st.info("Using default baseline data. Make a prediction first for personalized simulation.")

# Initialize simulation data
if 'simulation_data' not in st.session_state:
    st.session_state.simulation_data = deepcopy(baseline_data)

# Simulation interface
st.markdown("---")
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Adjust Lifestyle Factors")
    
    # Create tabs for different categories
    lifestyle_tab, medical_tab, exercise_tab = st.tabs(["Lifestyle Factors", "Medical Parameters", "Exercise & Stress"])
    
    with lifestyle_tab:
        st.markdown("**Modifiable Lifestyle Factors**")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            # Blood pressure (lifestyle modifiable)
            new_bp = st.slider(
                "Resting Blood Pressure (mmHg)",
                min_value=90,
                max_value=200,
                value=int(st.session_state.simulation_data['resting_bp']),
                step=5,
                help="Target: <120 (Normal), 120-139 (Elevated), ≥140 (High)"
            )
            st.session_state.simulation_data['resting_bp'] = new_bp
            
            # Cholesterol (diet modifiable)
            new_chol = st.slider(
                "Cholesterol (mg/dl)",
                min_value=100,
                max_value=400,
                value=int(st.session_state.simulation_data['cholesterol']),
                step=10,
                help="Target: <200 (Desirable), 200-239 (Borderline), ≥240 (High)"
            )
            st.session_state.simulation_data['cholesterol'] = new_chol
        
        with col_b:
            # Max heart rate (fitness level)
            new_hr = st.slider(
                "Maximum Heart Rate Achieved",
                min_value=60,
                max_value=220,
                value=int(st.session_state.simulation_data['max_heart_rate']),
                step=5,
                help="Higher values generally indicate better cardiovascular fitness"
            )
            st.session_state.simulation_data['max_heart_rate'] = new_hr
            
            # Blood sugar
            new_fbs = st.selectbox(
                "Fasting Blood Sugar > 120 mg/dl",
                options=[0, 1],
                index=st.session_state.simulation_data['fasting_blood_sugar'],
                format_func=lambda x: "No" if x == 0 else "Yes",
                help="Diabetes management through diet and medication"
            )
            st.session_state.simulation_data['fasting_blood_sugar'] = new_fbs
    
    with medical_tab:
        st.markdown("**Medical Parameters**")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            # ECG results
            new_ecg = st.selectbox(
                "Resting ECG Results",
                options=[0, 1, 2],
                index=st.session_state.simulation_data['rest_ecg'],
                format_func=lambda x: {
                    0: "Normal",
                    1: "ST-T Wave Abnormality",
                    2: "Left Ventricular Hypertrophy"
                }[x]
            )
            st.session_state.simulation_data['rest_ecg'] = new_ecg
            
            # Chest pain type
            new_cp = st.selectbox(
                "Chest Pain Type",
                options=[1, 2, 3, 4],
                index=[1, 2, 3, 4].index(st.session_state.simulation_data['chest_pain_type']),
                format_func=lambda x: {
                    1: "Typical Angina",
                    2: "Atypical Angina",
                    3: "Non-Anginal Pain",
                    4: "Asymptomatic"
                }[x]
            )
            st.session_state.simulation_data['chest_pain_type'] = new_cp
        
        with col_b:
            # CA (number of vessels)
            new_ca = st.selectbox(
                "Major Vessels (0-4)",
                options=[0, 1, 2, 3, 4],
                index=st.session_state.simulation_data['ca'],
                help="Number of major vessels colored by fluoroscopy"
            )
            st.session_state.simulation_data['ca'] = new_ca
            
            # Thalassemia
            new_thal = st.selectbox(
                "Thalassemia",
                options=[1, 2, 3],
                index=[1, 2, 3].index(st.session_state.simulation_data['thal']),
                format_func=lambda x: {
                    1: "Normal",
                    2: "Fixed Defect",
                    3: "Reversible Defect"
                }[x]
            )
            st.session_state.simulation_data['thal'] = new_thal
    
    with exercise_tab:
        st.markdown("**Exercise & Stress Test Results**")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            # Exercise angina
            new_angina = st.selectbox(
                "Exercise Induced Angina",
                options=[0, 1],
                index=st.session_state.simulation_data['exercise_angina'],
                format_func=lambda x: "No" if x == 0 else "Yes",
                help="Chest pain during exercise"
            )
            st.session_state.simulation_data['exercise_angina'] = new_angina
            
            # ST depression
            new_st = st.slider(
                "ST Depression",
                min_value=0.0,
                max_value=6.0,
                value=float(st.session_state.simulation_data['st_depression']),
                step=0.1,
                help="Depression induced by exercise relative to rest"
            )
            st.session_state.simulation_data['st_depression'] = new_st
        
        with col_b:
            # ST slope
            new_slope = st.selectbox(
                "ST Slope",
                options=[1, 2, 3],
                index=[1, 2, 3].index(st.session_state.simulation_data['st_slope']),
                format_func=lambda x: {
                    1: "Upsloping",
                    2: "Flat", 
                    3: "Downsloping"
                }[x],
                help="Slope of the peak exercise ST segment"
            )
            st.session_state.simulation_data['st_slope'] = new_slope

with col2:
    st.subheader("Live Risk Assessment")
    
    # Calculate current risk
    current_risk, _ = make_prediction(st.session_state.simulation_data)
    
    if current_risk is not None:
        # Risk gauge
        fig = create_risk_gauge(current_risk)
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk comparison
        risk_change = current_risk - baseline_risk
        
        st.metric(
            "Current Risk",
            f"{current_risk:.1%}",
            delta=f"{risk_change:.1%}" if risk_change != 0 else None
        )
        
        st.metric("Risk Category", get_risk_category(current_risk))
        
        # Risk interpretation
        if risk_change > 0.05:
            st.error(f"Risk increased by {risk_change:.1%}")
        elif risk_change < -0.05:
            st.success(f"Risk decreased by {abs(risk_change):.1%}")
        else:
            st.info("Risk relatively unchanged")

# Scenario comparison
st.markdown("---")
st.subheader("Scenario Comparison")

# Predefined scenarios
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Optimal Health Scenario"):
        optimal_data = deepcopy(baseline_data)
        optimal_data.update({
            'resting_bp': 110,
            'cholesterol': 180,
            'max_heart_rate': min(220 - optimal_data['age'], 180),
            'fasting_blood_sugar': 0,
            'exercise_angina': 0,
            'st_depression': 0.5,
            'chest_pain_type': 4  # Asymptomatic
        })
        
        optimal_risk, _ = make_prediction(optimal_data)
        if optimal_risk is not None:
            st.success(f"Optimal Risk: {optimal_risk:.1%}")
            improvement = baseline_risk - optimal_risk
            st.write(f"Potential improvement: {improvement:.1%}")

with col2:
    if st.button("Lifestyle Improvement"):
        improved_data = deepcopy(baseline_data)
        improved_data.update({
            'resting_bp': max(baseline_data['resting_bp'] - 20, 100),
            'cholesterol': max(baseline_data['cholesterol'] - 40, 150),
            'max_heart_rate': min(baseline_data['max_heart_rate'] + 20, 200),
            'fasting_blood_sugar': 0
        })
        
        improved_risk, _ = make_prediction(improved_data)
        if improved_risk is not None:
            st.info(f"Improved Risk: {improved_risk:.1%}")
            improvement = baseline_risk - improved_risk
            st.write(f"Potential improvement: {improvement:.1%}")

with col3:
    if st.button("Reset to Baseline"):
        st.session_state.simulation_data = deepcopy(baseline_data)
        st.rerun()

# Factor impact analysis
st.markdown("---")
st.subheader("Factor Impact Analysis")

st.markdown("See how individual factors affect your risk when changed in isolation:")

# Calculate individual factor impacts
factor_impacts = {}
factors_to_test = {
    'resting_bp': [(100, 'Optimal BP'), (120, 'Normal BP'), (140, 'High BP'), (160, 'Very High BP')],
    'cholesterol': [(150, 'Optimal'), (200, 'Good'), (240, 'Borderline'), (280, 'High')],
    'max_heart_rate': [(120, 'Poor Fitness'), (140, 'Fair'), (160, 'Good'), (180, 'Excellent')],
    'exercise_angina': [(0, 'No Angina'), (1, 'With Angina')]
}

for factor, values in factors_to_test.items():
    factor_risks = []
    factor_labels = []
    
    for value, label in values:
        test_data = deepcopy(baseline_data)
        test_data[factor] = value
        
        test_risk, _ = make_prediction(test_data)
        if test_risk is not None:
            factor_risks.append(test_risk * 100)
            factor_labels.append(label)
    
    if factor_risks:
        factor_impacts[factor] = (factor_labels, factor_risks)

# Display impact charts
if factor_impacts:
    cols = st.columns(2)
    
    for i, (factor, (labels, risks)) in enumerate(factor_impacts.items()):
        col_idx = i % 2
        
        with cols[col_idx]:
            fig = go.Figure(data=[
                go.Bar(x=labels, y=risks, marker_color='lightcoral')
            ])
            
            fig.update_layout(
                title=f"Impact of {factor.replace('_', ' ').title()}",
                xaxis_title=factor.replace('_', ' ').title(),
                yaxis_title="Risk (%)",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "white"},
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)

# Recommendations based on simulation
st.markdown("---")
st.subheader("Personalized Recommendations")

recommendations = []

# Analyze current simulation vs baseline
current_risk, _ = make_prediction(st.session_state.simulation_data)

if current_risk is not None:
    sim_data = st.session_state.simulation_data
    
    # Blood pressure recommendations
    if sim_data['resting_bp'] > 130:
        recommendations.append({
            'category': 'Blood Pressure',
            'suggestion': 'Consider reducing sodium intake, increasing physical activity, and managing stress to lower blood pressure.',
            'target': 'Aim for <120 mmHg systolic'
        })
    
    # Cholesterol recommendations
    if sim_data['cholesterol'] > 200:
        recommendations.append({
            'category': 'Cholesterol',
            'suggestion': 'Adopt a heart-healthy diet rich in fiber, reduce saturated fats, and consider omega-3 fatty acids.',
            'target': 'Aim for <200 mg/dl total cholesterol'
        })
    
    # Fitness recommendations
    if sim_data['max_heart_rate'] < 140:
        recommendations.append({
            'category': 'Cardiovascular Fitness',
            'suggestion': 'Gradually increase aerobic exercise. Start with 150 minutes of moderate activity per week.',
            'target': 'Improve exercise capacity and heart rate response'
        })
    
    # Diabetes management
    if sim_data['fasting_blood_sugar'] == 1:
        recommendations.append({
            'category': 'Blood Sugar',
            'suggestion': 'Focus on diabetes management through diet, exercise, and medication compliance.',
            'target': 'Achieve fasting blood sugar <100 mg/dl'
        })

# Display recommendations
if recommendations:
    for rec in recommendations:
        with st.expander(f"{rec['category']}"):
            st.write(rec['suggestion'])
            st.info(f"Target: {rec['target']}")
else:
    st.success("Your current parameters look good! Continue maintaining healthy lifestyle habits.")

# Action buttons
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Save Current Scenario"):
        # In a real app, this would save to database
        st.success("Scenario saved! (Feature would be implemented in full version)")

with col2:
    if st.button("Get Detailed Recommendations"):
        st.switch_page("pages/06_Recommendations.py")

with col3:
    if st.button("View Dashboard"):
        st.switch_page("pages/02_Dashboard.py")
