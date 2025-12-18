import streamlit as st
import pandas as pd
import numpy as np
from utils.storage import get_community_stats, get_vitals_history, get_predictions_history
from utils.visualizations import create_age_risk_distribution, create_gender_risk_comparison
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Community Health Insights", page_icon="H", layout="wide")

st.title("Community Health Insights")
st.markdown("Explore anonymized health trends and compare your risk profile with community statistics.")

# Get community data
age_stats, gender_stats = get_community_stats()
vitals_history = get_vitals_history()
predictions_history = get_predictions_history()

# Check if we have enough data for community insights
total_users = len(vitals_history['id'].unique()) if not vitals_history.empty else 0

if total_users < 5:
    st.info("Community insights will be available when more users contribute data. Your data helps create valuable insights while maintaining complete privacy.")
    
    # Show basic app statistics instead
    st.markdown("---")
    st.subheader("Platform Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Predictions", len(predictions_history) if not predictions_history.empty else 0)
    
    with col2:
        st.metric("Health Records", len(vitals_history) if not vitals_history.empty else 0)
    
    with col3:
        if not vitals_history.empty:
            avg_risk = vitals_history['prediction_result'].mean()
            st.metric("Average Risk", f"{avg_risk:.1%}")
        else:
            st.metric("Average Risk", "N/A")
    
    with col4:
        active_users = 1 if 'latest_prediction' in st.session_state else 0
        st.metric("Active Users", active_users)
    
    st.markdown("---")
    st.info("Make predictions and track your health to contribute to community insights!")
    
    if st.button("Make a Prediction"):
        st.switch_page("pages/01_Prediction.py")
    
    st.stop()

# Community overview
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Community Members", total_users)

with col2:
    total_predictions = len(predictions_history) if not predictions_history.empty else 0
    st.metric("Total Predictions", total_predictions)

with col3:
    if not vitals_history.empty:
        avg_community_risk = vitals_history['prediction_result'].mean()
        st.metric("Average Community Risk", f"{avg_community_risk:.1%}")
    else:
        st.metric("Average Community Risk", "N/A")

with col4:
    if not vitals_history.empty:
        recent_activity = len(vitals_history[
            pd.to_datetime(vitals_history['date_recorded']) >= (datetime.now() - timedelta(days=7))
        ])
        st.metric("Active This Week", recent_activity)
    else:
        st.metric("Active This Week", 0)

# Risk distribution analysis
st.markdown("---")
st.subheader("Community Risk Distribution")

col1, col2 = st.columns(2)

with col1:
    # Age group analysis
    if not age_stats.empty:
        fig = create_age_risk_distribution((age_stats, gender_stats))
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Insufficient data for age group analysis")
    else:
        st.info("No age group data available yet")

with col2:
    # Gender comparison
    if not gender_stats.empty:
        fig = create_gender_risk_comparison((age_stats, gender_stats))
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Insufficient data for gender analysis")
    else:
        st.info("No gender comparison data available yet")

# Detailed community statistics
if not vitals_history.empty:
    st.markdown("---")
    st.subheader("Detailed Community Statistics")
    
    # Create risk categories
    vitals_history['risk_category'] = vitals_history['prediction_result'].apply(
        lambda x: 'Low Risk' if x < 0.3 else 'Medium Risk' if x < 0.7 else 'High Risk'
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk category distribution
        risk_distribution = vitals_history['risk_category'].value_counts()
        
        fig = px.pie(
            values=risk_distribution.values,
            names=risk_distribution.index,
            title="Community Risk Category Distribution",
            color_discrete_map={
                "Low Risk": "#2E8B57",
                "Medium Risk": "#FF8C00", 
                "High Risk": "#DC143C"
            }
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white"}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Risk score histogram
        fig = px.histogram(
            vitals_history,
            x='prediction_result',
            nbins=20,
            title="Community Risk Score Distribution",
            labels={'prediction_result': 'Risk Score', 'count': 'Number of Users'}
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white"}
        )
        st.plotly_chart(fig, use_container_width=True)

# Health metrics comparison
if not vitals_history.empty and len(vitals_history) > 20:
    st.markdown("---")
    st.subheader("Community Health Metrics")
    
    # Calculate percentiles for comparison
    metrics = ['age', 'resting_bp', 'cholesterol', 'max_heart_rate']
    available_metrics = [col for col in metrics if col in vitals_history.columns]
    
    if available_metrics:
        col1, col2 = st.columns(2)
        
        with col1:
            # Blood pressure distribution
            if 'resting_bp' in vitals_history.columns:
                fig = px.box(
                    vitals_history,
                    y='resting_bp',
                    title="Community Blood Pressure Distribution"
                )
                fig.add_hline(y=120, line_dash="dash", line_color="green", 
                             annotation_text="Normal (<120)")
                fig.add_hline(y=140, line_dash="dash", line_color="red", 
                             annotation_text="High (≥140)")
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={'color': "white"}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Cholesterol distribution
            if 'cholesterol' in vitals_history.columns:
                fig = px.box(
                    vitals_history,
                    y='cholesterol',
                    title="Community Cholesterol Distribution"
                )
                fig.add_hline(y=200, line_dash="dash", line_color="green", 
                             annotation_text="Desirable (<200)")
                fig.add_hline(y=240, line_dash="dash", line_color="red", 
                             annotation_text="High (≥240)")
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={'color': "white"}
                )
                st.plotly_chart(fig, use_container_width=True)

# Personal comparison (if user has made predictions)
if 'latest_prediction' in st.session_state and not vitals_history.empty:
    st.markdown("---")
    st.subheader("Your Profile vs Community")
    
    user_data = st.session_state['latest_prediction']['input_data']
    user_risk = st.session_state['latest_prediction']['score']
    
    # Calculate percentiles
    risk_percentile = (vitals_history['prediction_result'] < user_risk).mean() * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Your Risk Percentile", 
            f"{risk_percentile:.0f}%",
            help="Percentage of community with lower risk than yours"
        )
    
    with col2:
        if 'age' in user_data and 'age' in vitals_history.columns:
            age_percentile = (vitals_history['age'] < user_data['age']).mean() * 100
            st.metric("Age Percentile", f"{age_percentile:.0f}%")
    
    with col3:
        if 'resting_bp' in user_data and 'resting_bp' in vitals_history.columns:
            bp_percentile = (vitals_history['resting_bp'] < user_data['resting_bp']).mean() * 100
            st.metric("Blood Pressure Percentile", f"{bp_percentile:.0f}%")
    
    # Comparison insights
    st.markdown("#### Insights:")
    insights = []
    
    if risk_percentile > 75:
        insights.append(" Your risk is higher than 75% of the community. Consider consulting a healthcare provider.")
    elif risk_percentile > 50:
        insights.append("🟡 Your risk is above the community median. Lifestyle improvements could help.")
    elif risk_percentile > 25:
        insights.append("🟢 Your risk is below the community median. Keep up the good work!")
    else:
        insights.append(" Your risk is in the lowest 25% of the community. Excellent heart health!")
    
    if 'resting_bp' in user_data and 'resting_bp' in vitals_history.columns:
        community_avg_bp = vitals_history['resting_bp'].mean()
        if user_data['resting_bp'] > community_avg_bp + 10:
            insights.append("Your blood pressure is significantly above the community average.")
        elif user_data['resting_bp'] < community_avg_bp - 10:
            insights.append("Your blood pressure is below the community average - great job!")
    
    for insight in insights:
        if "" in insight or "significantly above" in insight:
            st.error(insight)
        elif "🟡" in insight or "above the" in insight:
            st.warning(insight)
        else:
            st.success(insight)

# Trends over time
if not vitals_history.empty and 'date_recorded' in vitals_history.columns:
    st.markdown("---")
    st.subheader("Community Trends Over Time")
    
    # Monthly trend analysis
    vitals_history['date_recorded'] = pd.to_datetime(vitals_history['date_recorded'])
    vitals_history['month'] = vitals_history['date_recorded'].dt.to_period('M')
    
    monthly_stats = vitals_history.groupby('month').agg({
        'prediction_result': ['mean', 'count'],
        'resting_bp': 'mean',
        'cholesterol': 'mean'
    }).round(3)
    
    if len(monthly_stats) > 1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk trend over time
            fig = px.line(
                x=monthly_stats.index.astype(str),
                y=monthly_stats[('prediction_result', 'mean')],
                title="Average Community Risk Over Time"
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "white"},
                xaxis_title="Month",
                yaxis_title="Average Risk Score"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Community activity
            fig = px.bar(
                x=monthly_stats.index.astype(str),
                y=monthly_stats[('prediction_result', 'count')],
                title="Community Activity Over Time"
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "white"},
                xaxis_title="Month",
                yaxis_title="Number of Predictions"
            )
            st.plotly_chart(fig, use_container_width=True)

# Risk factor prevalence
if not vitals_history.empty:
    st.markdown("---")
    st.subheader("Risk Factor Prevalence in Community")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Modifiable Risk Factors")
        
        risk_factor_stats = []
        
        if 'resting_bp' in vitals_history.columns:
            high_bp_pct = (vitals_history['resting_bp'] >= 140).mean() * 100
            risk_factor_stats.append(("High Blood Pressure (≥140)", high_bp_pct))
        
        if 'cholesterol' in vitals_history.columns:
            high_chol_pct = (vitals_history['cholesterol'] >= 240).mean() * 100
            risk_factor_stats.append(("High Cholesterol (≥240)", high_chol_pct))
        
        if 'fasting_blood_sugar' in vitals_history.columns:
            diabetes_pct = (vitals_history['fasting_blood_sugar'] == 1).mean() * 100
            risk_factor_stats.append(("Elevated Blood Sugar", diabetes_pct))
        
        if 'exercise_angina' in vitals_history.columns:
            angina_pct = (vitals_history['exercise_angina'] == 1).mean() * 100
            risk_factor_stats.append(("Exercise-Induced Angina", angina_pct))
        
        for factor, percentage in risk_factor_stats:
            st.metric(factor, f"{percentage:.1f}%")
    
    with col2:
        # Risk factor bar chart
        if risk_factor_stats:
            factors, percentages = zip(*risk_factor_stats)
            
            fig = px.bar(
                x=list(percentages),
                y=list(factors),
                orientation='h',
                title="Risk Factor Prevalence (%)",
                color=list(percentages),
                color_continuous_scale='Reds'
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "white"},
                xaxis_title="Percentage of Community",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

# Model usage statistics
if not predictions_history.empty:
    st.markdown("---")
    st.subheader("Community Model Usage")
    
    col1, col2 = st.columns(2)
    
    with col1:
        model_usage = predictions_history['model_used'].value_counts()
        
        fig = px.pie(
            values=model_usage.values,
            names=model_usage.index,
            title="Model Preference Distribution"
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white"}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Average risk by model
        if 'prediction_score' in predictions_history.columns:
            model_risk_avg = predictions_history.groupby('model_used')['prediction_score'].mean()
            
            fig = px.bar(
                x=model_risk_avg.index,
                y=model_risk_avg.values,
                title="Average Risk Score by Model"
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "white"},
                xaxis_title="Model",
                yaxis_title="Average Risk Score"
            )
            st.plotly_chart(fig, use_container_width=True)

# Privacy and data information
st.markdown("---")
st.subheader("Privacy & Data Information")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Data Privacy")
    st.info("""
    **Complete Anonymity**: All community insights are generated from completely anonymized data. 
    No personal information is stored or displayed.
    
    **Aggregated Statistics**: Individual data points are never shown. All statistics represent 
    group averages and distributions.
    
    **Secure Storage**: Your personal health data is encrypted and stored securely in your 
    local session.
    """)

with col2:
    st.markdown("#### How to Help the Community")
    st.success("""
    **Make Regular Predictions**: Regular use helps create more accurate community insights.
    
    **Track Your Progress**: Historical data helps identify community trends over time.
    
    **Share Safely**: Your data contributes to insights while maintaining complete privacy.
    
    **Benefit Everyone**: Community insights help all users understand their relative risk.
    """)

# Call to action for users without predictions
if 'latest_prediction' not in st.session_state:
    st.markdown("---")
    st.info("Make your first prediction to see how you compare with the community!")
    
    col1, col2, col3 = st.columns(3)
    
    with col2:
        if st.button("Make a Prediction", type="primary"):
            st.switch_page("pages/01_Prediction.py")

# Navigation
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("View Dashboard"):
        st.switch_page("pages/02_Dashboard.py")

with col2:
    if st.button("New Prediction"):
        st.switch_page("pages/01_Prediction.py")

with col3:
    if st.button("Historical Tracker"):
        st.switch_page("pages/04_Historical_Tracker.py")

with col4:
    if st.button("Get Recommendations"):
        st.switch_page("pages/06_Recommendations.py")
