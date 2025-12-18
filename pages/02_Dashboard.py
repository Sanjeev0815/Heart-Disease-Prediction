import streamlit as st
import pandas as pd
from utils.storage import get_vitals_history, get_community_stats
from utils.visualizations import (
    create_risk_gauge, create_risk_trend_chart, create_vitals_correlation_matrix,
    create_model_comparison_chart, create_age_risk_distribution, create_gender_risk_comparison
)
from utils.models import get_feature_importance
import plotly.express as px

st.set_page_config(page_title="Health Dashboard", page_icon="H", layout="wide")

st.title("Interactive Health Dashboard")

# Check if there's a latest prediction
if 'latest_prediction' not in st.session_state:
    st.info("Make a prediction first to see personalized dashboard data.")
    if st.button("Go to Prediction"):
        st.switch_page("pages/01_Prediction.py")
    st.stop()

# Get data
vitals_history = get_vitals_history()
community_stats = get_community_stats()

# Dashboard header with key metrics
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

latest_prediction = st.session_state['latest_prediction']

with col1:
    st.metric(
        "Latest Risk Score", 
        f"{latest_prediction['score']:.1%}",
        delta=None
    )

with col2:
    st.metric(
        "Risk Category", 
        latest_prediction['category'],
        delta=None
    )

with col3:
    total_predictions = len(vitals_history) if not vitals_history.empty else 0
    st.metric(
        "Total Predictions", 
        total_predictions,
        delta=None
    )

with col4:
    if not vitals_history.empty and len(vitals_history) > 1:
        current_risk = vitals_history.iloc[0]['prediction_result']
        previous_risk = vitals_history.iloc[1]['prediction_result']
        change = current_risk - previous_risk
        st.metric(
            "Risk Change", 
            f"{current_risk:.1%}",
            delta=f"{change:.1%}"
        )
    else:
        st.metric("Risk Change", "N/A", delta=None)

# Main dashboard content
st.markdown("---")

# Row 1: Current Risk Assessment
col1, col2 = st.columns(2)

with col1:
    st.subheader("Current Risk Assessment")
    fig = create_risk_gauge(latest_prediction['score'])
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk interpretation
    risk_score = latest_prediction['score']
    if risk_score < 0.3:
        st.success("Low Risk: Continue maintaining healthy lifestyle habits.")
    elif risk_score < 0.7:
        st.warning("Medium Risk: Consider implementing preventive measures.")
    else:
        st.error("High Risk: Recommend immediate consultation with healthcare provider.")

with col2:
    st.subheader("Model Performance Comparison")
    if 'model_accuracies' in st.session_state:
        fig = create_model_comparison_chart(st.session_state['model_accuracies'])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Model accuracy data not available")

# Row 2: Feature Analysis
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Feature Importance")
    feature_names, importances = get_feature_importance(latest_prediction['model'])
    
    if feature_names and importances is not None:
        # Create feature importance chart
        from utils.visualizations import create_feature_importance_chart
        fig = create_feature_importance_chart(feature_names, importances)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Feature importance data not available")

with col2:
    st.subheader("Risk Factors Analysis")
    
    input_data = latest_prediction['input_data']
    
    # Identify high-risk factors
    high_risk_factors = []
    
    if input_data.get('age', 0) > 55:
        high_risk_factors.append("Age > 55 years")
    if input_data.get('resting_bp', 0) > 140:
        high_risk_factors.append("High Blood Pressure")
    if input_data.get('cholesterol', 0) > 240:
        high_risk_factors.append("High Cholesterol")
    if input_data.get('chest_pain_type', 0) in [1, 2]:
        high_risk_factors.append("Chest Pain Symptoms")
    if input_data.get('exercise_angina', 0) == 1:
        high_risk_factors.append("Exercise-Induced Angina")
    
    if high_risk_factors:
        st.error("**Identified Risk Factors:**")
        for factor in high_risk_factors:
            st.write(f"• {factor}")
    else:
        st.success("No major risk factors identified")
    
    # Protective factors
    protective_factors = []
    
    if input_data.get('max_heart_rate', 0) > 150:
        protective_factors.append("Good Exercise Capacity")
    if input_data.get('cholesterol', 0) < 200:
        protective_factors.append("Healthy Cholesterol Level")
    if input_data.get('resting_bp', 0) < 120:
        protective_factors.append("Normal Blood Pressure")
    
    if protective_factors:
        st.success("**Protective Factors:**")
        for factor in protective_factors:
            st.write(f"• {factor}")

# Row 3: Trends and History
if not vitals_history.empty:
    st.markdown("---")
    st.subheader("Health Trends Over Time")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = create_risk_trend_chart(vitals_history)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Insufficient data for trend analysis")
    
    with col2:
        fig = create_vitals_correlation_matrix(vitals_history)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Insufficient data for correlation analysis")
    
    # Vitals summary table
    st.subheader("Recent Vitals Summary")
    
    # Display recent entries
    recent_vitals = vitals_history.head(10)
    
    # Select and format columns for display
    display_columns = ['date_recorded', 'age', 'resting_bp', 'cholesterol', 'max_heart_rate', 'prediction_result', 'risk_category']
    available_columns = [col for col in display_columns if col in recent_vitals.columns]
    
    if available_columns:
        display_df = recent_vitals[available_columns].copy()
        display_df['date_recorded'] = pd.to_datetime(display_df['date_recorded']).dt.strftime('%Y-%m-%d %H:%M')
        if 'prediction_result' in display_df.columns:
            display_df['prediction_result'] = display_df['prediction_result'].apply(lambda x: f"{x:.1%}")
        
        st.dataframe(display_df, use_container_width=True)

# Row 4: Community Insights
st.markdown("---")
st.subheader("Community Health Insights")

age_stats, gender_stats = community_stats

col1, col2 = st.columns(2)

with col1:
    fig = create_age_risk_distribution((age_stats, gender_stats))
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insufficient community data for age analysis")

with col2:
    fig = create_gender_risk_comparison((age_stats, gender_stats))
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insufficient community data for gender analysis")

# Quick insights
st.markdown("---")
st.subheader("Key Insights")

insights = []

# Risk trend insight
if not vitals_history.empty and len(vitals_history) > 1:
    current_risk = vitals_history.iloc[0]['prediction_result']
    previous_risk = vitals_history.iloc[1]['prediction_result']
    
    if current_risk > previous_risk:
        insights.append(" Your risk score has increased since last assessment. Consider reviewing your lifestyle factors.")
    elif current_risk < previous_risk:
        insights.append(" Great news! Your risk score has improved since last assessment.")
    else:
        insights.append(" Your risk score remains stable.")

# Age comparison insight
if not age_stats.empty:
    user_age = input_data.get('age', 0)
    for _, row in age_stats.iterrows():
        if user_age < 30 and row['age_group'] == 'Under 30':
            avg_risk = row['avg_risk']
            if latest_prediction['score'] > avg_risk:
                insights.append(f" Your risk is higher than average for your age group ({avg_risk:.1%})")
            else:
                insights.append(f" Your risk is lower than average for your age group ({avg_risk:.1%})")
            break

# Display insights
if insights:
    for insight in insights:
        st.info(insight)
else:
    st.info("Continue tracking your health to generate personalized insights.")

# Navigation buttons
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("New Prediction"):
        st.switch_page("pages/01_Prediction.py")

with col2:
    if st.button("View History"):
        st.switch_page("pages/04_Historical_Tracker.py")

with col3:
    if st.button("Get Recommendations"):
        st.switch_page("pages/06_Recommendations.py")

with col4:
    if st.button("Generate Report"):
        st.switch_page("pages/09_Reports.py")
