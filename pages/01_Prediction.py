import streamlit as st
import pandas as pd
import numpy as np
from utils.models import make_prediction, get_risk_category, get_shap_explanation
from utils.storage import save_vitals, save_prediction
from utils.visualizations import create_risk_gauge, create_shap_waterfall

st.set_page_config(page_title="Heart Disease Prediction", page_icon="H", layout="wide")

st.title("Heart Disease Risk Prediction")

# Check if models are available
if 'models' not in st.session_state:
    st.warning("Please upload and train models on the main page first.")
    st.stop()

st.markdown("Enter your health information below to get a personalized heart disease risk assessment.")

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    st.subheader("Basic Information")
    age = st.number_input("Age", min_value=1, max_value=120, value=50)
    gender = st.selectbox("Gender", ["Male", "Female"])
    
    st.subheader("Cardiovascular Measurements")
    resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", min_value=80, max_value=200, value=120)
    cholesterol = st.number_input("Cholesterol (mg/dl)", min_value=100, max_value=600, value=200)
    max_heart_rate = st.number_input("Maximum Heart Rate Achieved", min_value=60, max_value=220, value=150)
    
    st.subheader("Exercise & Stress Tests")
    st_depression = st.number_input("ST Depression (induced by exercise)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)

with col2:
    st.subheader("Medical History")
    chest_pain_type = st.selectbox(
        "Chest Pain Type",
        [1, 2, 3, 4],
        format_func=lambda x: {
            1: "Typical Angina",
            2: "Atypical Angina", 
            3: "Non-Anginal Pain",
            4: "Asymptomatic"
        }[x]
    )
    
    fasting_blood_sugar = st.selectbox(
        "Fasting Blood Sugar > 120 mg/dl",
        [0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )
    
    rest_ecg = st.selectbox(
        "Resting ECG Results",
        [0, 1, 2],
        format_func=lambda x: {
            0: "Normal",
            1: "ST-T Wave Abnormality",
            2: "Left Ventricular Hypertrophy"
        }[x]
    )
    
    exercise_angina = st.selectbox(
        "Exercise Induced Angina",
        [0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )
    
    st_slope = st.selectbox(
        "Slope of Peak Exercise ST Segment",
        [1, 2, 3],
        format_func=lambda x: {
            1: "Upsloping",
            2: "Flat",
            3: "Downsloping"
        }[x]
    )
    
    ca = st.selectbox("Number of Major Vessels Colored by Fluoroscopy", [0, 1, 2, 3, 4])
    thal = st.selectbox(
        "Thalassemia",
        [1, 2, 3],
        format_func=lambda x: {
            1: "Normal",
            2: "Fixed Defect", 
            3: "Reversible Defect"
        }[x]
    )

# Prepare input data
input_data = {
    'age': age,
    'gender': 1 if gender == "Male" else 0,
    'chest_pain_type': chest_pain_type,
    'resting_bp': resting_bp,
    'cholesterol': cholesterol,
    'fasting_blood_sugar': fasting_blood_sugar,
    'rest_ecg': rest_ecg,
    'max_heart_rate': max_heart_rate,
    'exercise_angina': exercise_angina,
    'st_depression': st_depression,
    'st_slope': st_slope,
    'ca': ca,
    'thal': thal
}

# Model selection
st.markdown("---")
model_choice = st.selectbox(
    "Select Prediction Model",
    ["xgboost", "random_forest", "logistic"],
    format_func=lambda x: {
        "xgboost": "XGBoost (Recommended)",
        "random_forest": "Random Forest",
        "logistic": "Logistic Regression"
    }[x]
)

if st.button("Predict Risk", type="primary"):
    with st.spinner("Calculating risk..."):
        # Make prediction
        prediction, model = make_prediction(input_data, model_choice)
        
        if prediction is not None:
            risk_category = get_risk_category(prediction)
            
            # Store results in session state
            st.session_state['latest_prediction'] = {
                'score': prediction,
                'category': risk_category,
                'model': model_choice,
                'input_data': input_data
            }
            
            # Save to database
            save_vitals(input_data, prediction, risk_category)
            save_prediction(model_choice, input_data, prediction, risk_category)
            
            st.success("Prediction completed!")
            
            # Display results in columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Risk Assessment")
                
                # Risk gauge
                fig = create_risk_gauge(prediction)
                st.plotly_chart(fig, use_container_width=True)
                
                # Risk details
                st.metric("Risk Score", f"{prediction:.1%}")
                st.metric("Risk Category", risk_category)
                
                # Color-coded risk message
                if risk_category == "Low Risk":
                    st.success(f"Your {risk_category.lower()} indicates a lower probability of heart disease.")
                elif risk_category == "Medium Risk":
                    st.warning(f"Your {risk_category.lower()} suggests moderate concern. Consider lifestyle improvements.")
                else:
                    st.error(f"Your {risk_category.lower()} indicates higher probability. Please consult a healthcare professional.")
            
            with col2:
                st.subheader("Model Explanation")
                
                # Get SHAP explanation
                shap_values = get_shap_explanation(input_data, model_choice)
                
                if shap_values is not None:
                    feature_names = list(input_data.keys())
                    
                    # Create SHAP waterfall plot
                    shap_fig = create_shap_waterfall(shap_values, feature_names, input_data)
                    if shap_fig:
                        st.plotly_chart(shap_fig, use_container_width=True)
                    
                    # Top contributing factors
                    top_indices = np.argsort(np.abs(shap_values))[-5:]
                    st.write("**Top 5 Contributing Factors:**")
                    
                    for i in reversed(top_indices):
                        factor = feature_names[i]
                        impact = shap_values[i]
                        direction = "increases" if impact > 0 else "decreases"
                        st.write(f"• **{factor}**: {direction} risk by {abs(impact):.3f}")
                
                else:
                    st.info("Model explanation not available for this prediction.")
            
            # Model performance comparison
            st.markdown("---")
            st.subheader("All Model Predictions")
            
            models = ["logistic", "random_forest", "xgboost"]
            model_results = {}
            
            for model_name in models:
                pred, _ = make_prediction(input_data, model_name)
                if pred is not None:
                    model_results[model_name] = {
                        'score': pred,
                        'category': get_risk_category(pred)
                    }
            
            # Display comparison table
            comparison_data = []
            for model_name, result in model_results.items():
                comparison_data.append({
                    'Model': model_name.replace('_', ' ').title(),
                    'Risk Score': f"{result['score']:.1%}",
                    'Risk Category': result['category'],
                    'Accuracy': f"{st.session_state.model_accuracies.get(model_name, 0):.3f}"
                })
            
            if comparison_data:
                df_comparison = pd.DataFrame(comparison_data)
                st.dataframe(df_comparison, use_container_width=True)
        
        else:
            st.error("Unable to make prediction. Please check your input data and ensure models are trained.")

# Quick actions
st.markdown("---")
st.subheader("Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("View Dashboard"):
        st.switch_page("pages/02_Dashboard.py")

with col2:
    if st.button("Chat with AI"):
        st.switch_page("pages/03_Chatbot.py")

with col3:
    if st.button("Get Recommendations"):
        st.switch_page("pages/06_Recommendations.py")
