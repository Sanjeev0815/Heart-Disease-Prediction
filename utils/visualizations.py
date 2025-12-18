import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st

def create_risk_gauge(risk_score):
    """Create a gauge chart for risk visualization"""
    # Determine color based on risk level
    if risk_score < 0.3:
        color = "green"
    elif risk_score < 0.7:
        color = "yellow"
    else:
        color = "red"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_score * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Heart Disease Risk (%)"},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 70], 'color': "lightyellow"},
                {'range': [70, 100], 'color': "lightcoral"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"},
        height=400
    )
    
    return fig

def create_shap_waterfall(shap_values, feature_names, input_values):
    """Create SHAP waterfall plot"""
    if shap_values is None or len(shap_values) == 0:
        return None
    
    # Sort features by absolute SHAP value
    indices = np.argsort(np.abs(shap_values))[-10:]  # Top 10 features
    
    sorted_shap = shap_values[indices]
    sorted_features = [feature_names[i] for i in indices]
    sorted_values = [input_values[feature_names[i]] for i in indices]
    
    # Create labels with feature names and values
    labels = [f"{feature} = {value}" for feature, value in zip(sorted_features, sorted_values)]
    
    fig = go.Figure(go.Bar(
        y=labels,
        x=sorted_shap,
        orientation='h',
        marker=dict(
            color=['red' if x < 0 else 'green' for x in sorted_shap],
        )
    ))
    
    fig.update_layout(
        title="Feature Impact on Prediction",
        xaxis_title="SHAP Value (Impact on Prediction)",
        yaxis_title="Features",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"},
        height=500
    )
    
    return fig

def create_feature_importance_chart(feature_names, importances):
    """Create feature importance chart"""
    if feature_names is None or importances is None:
        return None
    
    # Sort by importance
    indices = np.argsort(importances)[-10:]  # Top 10 features
    sorted_importance = importances[indices]
    sorted_features = [feature_names[i] for i in indices]
    
    fig = go.Figure(go.Bar(
        y=sorted_features,
        x=sorted_importance,
        orientation='h',
        marker_color='lightblue'
    ))
    
    fig.update_layout(
        title="Feature Importance",
        xaxis_title="Importance Score",
        yaxis_title="Features",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"},
        height=500
    )
    
    return fig

def create_risk_trend_chart(history_df):
    """Create risk trend over time"""
    if history_df.empty:
        return None
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=pd.to_datetime(history_df['date_recorded']),
        y=history_df['prediction_result'] * 100,
        mode='lines+markers',
        name='Risk Score',
        line=dict(color='red', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Heart Disease Risk Trend Over Time",
        xaxis_title="Date",
        yaxis_title="Risk Score (%)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"},
        height=400
    )
    
    return fig

def create_vitals_correlation_matrix(history_df):
    """Create correlation matrix for vitals"""
    if history_df.empty:
        return None
    
    # Select numeric columns for correlation
    numeric_cols = ['age', 'resting_bp', 'cholesterol', 'max_heart_rate', 'st_depression', 'prediction_result']
    available_cols = [col for col in numeric_cols if col in history_df.columns]
    
    if len(available_cols) < 2:
        return None
    
    corr_matrix = history_df[available_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0
    ))
    
    fig.update_layout(
        title="Vitals Correlation Matrix",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"},
        height=500
    )
    
    return fig

def create_model_comparison_chart(accuracies):
    """Create model accuracy comparison chart"""
    models = list(accuracies.keys())
    scores = list(accuracies.values())
    
    fig = go.Figure(data=[
        go.Bar(name='Accuracy', x=models, y=scores, marker_color=['#FF4B4B', '#00CC96', '#AB63FA'])
    ])
    
    fig.update_layout(
        title="Model Accuracy Comparison",
        xaxis_title="Models",
        yaxis_title="Accuracy Score",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"},
        height=400,
        yaxis=dict(range=[0, 1])
    )
    
    return fig

def create_age_risk_distribution(community_stats):
    """Create age group risk distribution chart"""
    age_stats, gender_stats = community_stats
    
    if age_stats.empty:
        return None
    
    fig = go.Figure(data=[
        go.Bar(x=age_stats['age_group'], y=age_stats['avg_risk'] * 100, 
               marker_color='lightcoral',
               text=age_stats['count'],
               texttemplate='n=%{text}',
               textposition='outside')
    ])
    
    fig.update_layout(
        title="Average Risk by Age Group",
        xaxis_title="Age Group",
        yaxis_title="Average Risk (%)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"},
        height=400
    )
    
    return fig

def create_gender_risk_comparison(community_stats):
    """Create gender risk comparison chart"""
    age_stats, gender_stats = community_stats
    
    if gender_stats.empty:
        return None
    
    fig = go.Figure(data=[
        go.Bar(x=gender_stats['gender'], y=gender_stats['avg_risk'] * 100, 
               marker_color=['lightblue', 'lightpink'],
               text=gender_stats['count'],
               texttemplate='n=%{text}',
               textposition='outside')
    ])
    
    fig.update_layout(
        title="Average Risk by Gender",
        xaxis_title="Gender",
        yaxis_title="Average Risk (%)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"},
        height=400
    )
    
    return fig

def create_medication_timeline(medications_df):
    """Create medication timeline visualization"""
    if medications_df.empty:
        return None
    
    fig = go.Figure()
    
    for idx, med in medications_df.iterrows():
        start_date = pd.to_datetime(med['start_date'])
        end_date = pd.to_datetime(med['end_date']) if pd.notna(med['end_date']) else pd.Timestamp.now()
        
        fig.add_trace(go.Scatter(
            x=[start_date, end_date],
            y=[idx, idx],
            mode='lines+markers',
            name=med['medication_name'],
            line=dict(width=10),
            hovertemplate=f"<b>{med['medication_name']}</b><br>" +
                         f"Dosage: {med['dosage']}<br>" +
                         f"Frequency: {med['frequency']}<br>" +
                         f"Start: {start_date.strftime('%Y-%m-%d')}<br>" +
                         f"End: {end_date.strftime('%Y-%m-%d') if pd.notna(med['end_date']) else 'Ongoing'}<extra></extra>"
        ))
    
    fig.update_layout(
        title="Medication Timeline",
        xaxis_title="Date",
        yaxis_title="Medications",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"},
        height=400,
        showlegend=False
    )
    
    return fig
