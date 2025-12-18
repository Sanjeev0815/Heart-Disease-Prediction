import streamlit as st
import pandas as pd
import plotly.express as px
from utils.storage import get_vitals_history, get_predictions_history
from utils.visualizations import create_risk_trend_chart, create_vitals_correlation_matrix
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(page_title="Historical Health Tracker", page_icon="H", layout="wide")

st.title("Historical Health Tracker")
st.markdown("Track your health metrics and risk predictions over time.")

# Get historical data
vitals_history = get_vitals_history()
predictions_history = get_predictions_history()

if vitals_history.empty:
    st.info("No historical data available yet. Make some predictions to start tracking your health trends!")
    if st.button("Make Your First Prediction"):
        st.switch_page("pages/01_Prediction.py")
    st.stop()

# Time range selector
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    time_range = st.selectbox(
        "Select Time Range",
        ["Last 7 days", "Last 30 days", "Last 90 days", "All time"]
    )

with col2:
    # Calculate date range
    end_date = datetime.now()
    if time_range == "Last 7 days":
        start_date = end_date - timedelta(days=7)
    elif time_range == "Last 30 days":
        start_date = end_date - timedelta(days=30)
    elif time_range == "Last 90 days":
        start_date = end_date - timedelta(days=90)
    else:
        start_date = datetime(2020, 1, 1)  # All time
    
    st.metric("Records Found", len(vitals_history))

with col3:
    # Export option
    if st.button("Export Data"):
        csv = vitals_history.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"heart_health_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# Filter data by date range
if 'date_recorded' in vitals_history.columns:
    vitals_history['date_recorded'] = pd.to_datetime(vitals_history['date_recorded'])
    filtered_data = vitals_history[
        (vitals_history['date_recorded'] >= start_date) & 
        (vitals_history['date_recorded'] <= end_date)
    ]
else:
    filtered_data = vitals_history

# Main dashboard
st.markdown("---")

# Summary statistics
col1, col2, col3, col4 = st.columns(4)

with col1:
    if not filtered_data.empty:
        avg_risk = filtered_data['prediction_result'].mean()
        st.metric("Average Risk", f"{avg_risk:.1%}")
    else:
        st.metric("Average Risk", "N/A")

with col2:
    if not filtered_data.empty:
        latest_risk = filtered_data.iloc[0]['prediction_result']
        previous_risk = filtered_data.iloc[1]['prediction_result'] if len(filtered_data) > 1 else latest_risk
        change = latest_risk - previous_risk
        st.metric(
            "Latest Risk", 
            f"{latest_risk:.1%}",
            delta=f"{change:.1%}" if change != 0 else None
        )
    else:
        st.metric("Latest Risk", "N/A")

with col3:
    if not filtered_data.empty:
        high_risk_count = sum(filtered_data['prediction_result'] > 0.7)
        st.metric("High Risk Days", high_risk_count)
    else:
        st.metric("High Risk Days", "N/A")

with col4:
    total_predictions = len(filtered_data)
    st.metric("Total Predictions", total_predictions)

# Risk trend visualization
st.markdown("---")
st.subheader("Risk Score Trends")

col1, col2 = st.columns(2)

with col1:
    if not filtered_data.empty:
        fig = create_risk_trend_chart(filtered_data)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Unable to create trend chart")
    else:
        st.info("No data available for selected time range")

with col2:
    if not filtered_data.empty and len(filtered_data) > 5:
        # Risk category distribution
        risk_categories = []
        for risk_score in filtered_data['prediction_result']:
            if risk_score < 0.3:
                risk_categories.append("Low Risk")
            elif risk_score < 0.7:
                risk_categories.append("Medium Risk")
            else:
                risk_categories.append("High Risk")
        
        category_counts = pd.Series(risk_categories).value_counts()
        
        fig = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title="Risk Category Distribution",
            color_discrete_map={
                "Low Risk": "green",
                "Medium Risk": "orange", 
                "High Risk": "red"
            }
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white"}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Need more data points for distribution analysis")

# Vitals trends
st.markdown("---")
st.subheader("Vitals Trends Over Time")

if not filtered_data.empty:
    # Select vitals to display
    vital_options = [col for col in ['resting_bp', 'cholesterol', 'max_heart_rate', 'age'] 
                    if col in filtered_data.columns]
    
    selected_vitals = st.multiselect(
        "Select vitals to display:",
        vital_options,
        default=vital_options[:3] if len(vital_options) >= 3 else vital_options
    )
    
    if selected_vitals:
        # Create subplots for selected vitals
        fig_vitals = px.line(
            filtered_data, 
            x='date_recorded', 
            y=selected_vitals,
            title="Vitals Trends",
            labels={'value': 'Value', 'date_recorded': 'Date'}
        )
        fig_vitals.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white"},
            height=400
        )
        st.plotly_chart(fig_vitals, use_container_width=True)
    
    # Correlation analysis
    col1, col2 = st.columns(2)
    
    with col1:
        fig_corr = create_vitals_correlation_matrix(filtered_data)
        if fig_corr:
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.info("Insufficient data for correlation analysis")
    
    with col2:
        # Statistical summary
        st.subheader("Statistical Summary")
        
        summary_cols = [col for col in ['prediction_result', 'resting_bp', 'cholesterol', 'max_heart_rate'] 
                       if col in filtered_data.columns]
        
        if summary_cols:
            summary_stats = filtered_data[summary_cols].describe()
            st.dataframe(summary_stats, use_container_width=True)

# Detailed records table
st.markdown("---")
st.subheader("Detailed Records")

# Add filters for the table
col1, col2 = st.columns(2)

with col1:
    risk_filter = st.selectbox(
        "Filter by Risk Category",
        ["All", "Low Risk", "Medium Risk", "High Risk"]
    )

with col2:
    records_limit = st.selectbox(
        "Number of records to display",
        [10, 25, 50, 100],
        index=1
    )

# Apply filters
display_data = filtered_data.copy()

if risk_filter != "All":
    if risk_filter == "Low Risk":
        display_data = display_data[display_data['prediction_result'] < 0.3]
    elif risk_filter == "Medium Risk":
        display_data = display_data[(display_data['prediction_result'] >= 0.3) & (display_data['prediction_result'] < 0.7)]
    else:  # High Risk
        display_data = display_data[display_data['prediction_result'] >= 0.7]

# Format data for display
if not display_data.empty:
    display_cols = ['date_recorded', 'age', 'resting_bp', 'cholesterol', 'max_heart_rate', 'prediction_result', 'risk_category']
    available_cols = [col for col in display_cols if col in display_data.columns]
    
    display_df = display_data[available_cols].head(records_limit).copy()
    
    if 'date_recorded' in display_df.columns:
        display_df['date_recorded'] = display_df['date_recorded'].dt.strftime('%Y-%m-%d %H:%M')
    if 'prediction_result' in display_df.columns:
        display_df['prediction_result'] = display_df['prediction_result'].apply(lambda x: f"{x:.1%}")
    
    st.dataframe(display_df, use_container_width=True)
    
    # Download filtered data
    if st.button("Download Filtered Data"):
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"filtered_heart_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

else:
    st.info("No records match the selected filters.")

# Model performance over time
if not predictions_history.empty:
    st.markdown("---")
    st.subheader("Model Usage Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Model usage distribution
        model_counts = predictions_history['model_used'].value_counts()
        
        fig = px.bar(
            x=model_counts.index,
            y=model_counts.values,
            title="Model Usage Distribution",
            labels={'x': 'Model', 'y': 'Usage Count'}
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white"}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Model accuracy over time (if available)
        if 'prediction_date' in predictions_history.columns:
            predictions_history['prediction_date'] = pd.to_datetime(predictions_history['prediction_date'])
            recent_predictions = predictions_history.tail(20)  # Last 20 predictions
            
            fig = px.scatter(
                recent_predictions,
                x='prediction_date',
                y='prediction_score',
                color='model_used',
                title="Recent Prediction Scores by Model"
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "white"}
            )
            st.plotly_chart(fig, use_container_width=True)

# Insights and patterns
st.markdown("---")
st.subheader("Health Insights")

if not filtered_data.empty:
    insights = []
    
    # Risk trend analysis
    if len(filtered_data) > 1:
        recent_risks = filtered_data.head(5)['prediction_result']
        older_risks = filtered_data.tail(5)['prediction_result']
        
        recent_avg = recent_risks.mean()
        older_avg = older_risks.mean()
        
        if recent_avg > older_avg:
            insights.append(" Your risk scores have been increasing recently. Consider reviewing your lifestyle factors.")
        elif recent_avg < older_avg:
            insights.append(" Good news! Your risk scores have been improving over time.")
        else:
            insights.append(" Your risk scores have been stable.")
    
    # Vitals analysis
    if 'resting_bp' in filtered_data.columns:
        avg_bp = filtered_data['resting_bp'].mean()
        if avg_bp > 140:
            insights.append(" Your average blood pressure is elevated. Consider consulting a healthcare provider.")
        elif avg_bp < 120:
            insights.append(" Your blood pressure readings are generally in a healthy range.")
    
    if 'cholesterol' in filtered_data.columns:
        avg_chol = filtered_data['cholesterol'].mean()
        if avg_chol > 240:
            insights.append(" Your cholesterol levels are consistently high. Dietary changes may help.")
        elif avg_chol < 200:
            insights.append(" Your cholesterol levels are in a healthy range.")
    
    # Display insights
    if insights:
        for insight in insights:
            st.info(insight)
    else:
        st.info("Keep tracking your health to generate personalized insights!")

# Action buttons
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("New Prediction"):
        st.switch_page("pages/01_Prediction.py")

with col2:
    if st.button("View Dashboard"):
        st.switch_page("pages/02_Dashboard.py")

with col3:
    if st.button("Get Recommendations"):
        st.switch_page("pages/06_Recommendations.py")

with col4:
    if st.button("Generate Report"):
        st.switch_page("pages/09_Reports.py")
