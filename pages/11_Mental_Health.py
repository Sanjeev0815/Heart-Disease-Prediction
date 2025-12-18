import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.storage import (
    init_storage, save_mental_health, get_mental_health_history, get_vitals_history
)

st.set_page_config(page_title="Mental Health - HeartSafe", layout="wide")

init_storage()

st.title("Stress & Mental Health Integration")
st.markdown("Track your mental health and stress levels to understand their impact on heart health.")

tab1, tab2, tab3 = st.tabs(["Log Mental Health", "View Trends", "Correlation Analysis"])

with tab1:
    st.markdown("### Record Your Mental Health Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        stress_level = st.slider(
            "Stress Level",
            min_value=1,
            max_value=10,
            value=5,
            help="Rate your stress level: 1 = Very Low, 10 = Very High"
        )
        
        sleep_hours = st.number_input(
            "Sleep Hours (last night)",
            min_value=0.0,
            max_value=24.0,
            value=7.0,
            step=0.5
        )
        
        anxiety_level = st.slider(
            "Anxiety Level",
            min_value=1,
            max_value=10,
            value=5,
            help="Rate your anxiety level: 1 = None, 10 = Severe"
        )
        
        depression_level = st.slider(
            "Depression Level",
            min_value=1,
            max_value=10,
            value=5,
            help="Rate your depression level: 1 = None, 10 = Severe"
        )
    
    with col2:
        work_hours = st.number_input(
            "Work Hours (today)",
            min_value=0.0,
            max_value=24.0,
            value=8.0,
            step=0.5
        )
        
        physical_activity_min = st.number_input(
            "Physical Activity (minutes)",
            min_value=0,
            max_value=1440,
            value=30,
            step=5
        )
        
        social_interaction_level = st.slider(
            "Social Interaction Level",
            min_value=1,
            max_value=10,
            value=5,
            help="Rate your social interaction: 1 = Very Low, 10 = Very High"
        )
        
        notes = st.text_area(
            "Additional Notes",
            placeholder="Any specific events, feelings, or observations..."
        )
    
    if st.button("Save Mental Health Record", type="primary"):
        mental_health_data = {
            'stress_level': stress_level,
            'sleep_hours': sleep_hours,
            'anxiety_level': anxiety_level,
            'depression_level': depression_level,
            'work_hours': work_hours,
            'physical_activity_min': physical_activity_min,
            'social_interaction_level': social_interaction_level,
            'notes': notes
        }
        save_mental_health(mental_health_data)
        st.success("Mental health record saved successfully!")
        st.rerun()

with tab2:
    st.markdown("### Mental Health Trends Over Time")
    
    mental_health_df = get_mental_health_history()
    
    if not mental_health_df.empty:
        mental_health_df['date_recorded'] = pd.to_datetime(mental_health_df['date_recorded'])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_stress = mental_health_df['stress_level'].mean()
            st.metric("Average Stress", f"{avg_stress:.1f}/10")
        
        with col2:
            avg_sleep = mental_health_df['sleep_hours'].mean()
            st.metric("Average Sleep", f"{avg_sleep:.1f} hrs")
        
        with col3:
            avg_anxiety = mental_health_df['anxiety_level'].mean()
            st.metric("Average Anxiety", f"{avg_anxiety:.1f}/10")
        
        with col4:
            avg_activity = mental_health_df['physical_activity_min'].mean()
            st.metric("Average Activity", f"{avg_activity:.0f} min")
        
        st.markdown("---")
        
        fig_stress = go.Figure()
        fig_stress.add_trace(go.Scatter(
            x=mental_health_df['date_recorded'],
            y=mental_health_df['stress_level'],
            mode='lines+markers',
            name='Stress Level',
            line=dict(color='red', width=2)
        ))
        fig_stress.update_layout(
            title='Stress Level Over Time',
            xaxis_title='Date',
            yaxis_title='Stress Level (1-10)',
            yaxis=dict(range=[0, 11])
        )
        st.plotly_chart(fig_stress, use_container_width=True)
        
        fig_sleep = go.Figure()
        fig_sleep.add_trace(go.Scatter(
            x=mental_health_df['date_recorded'],
            y=mental_health_df['sleep_hours'],
            mode='lines+markers',
            name='Sleep Hours',
            line=dict(color='blue', width=2)
        ))
        fig_sleep.update_layout(
            title='Sleep Duration Over Time',
            xaxis_title='Date',
            yaxis_title='Hours of Sleep'
        )
        st.plotly_chart(fig_sleep, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_anxiety = go.Figure()
            fig_anxiety.add_trace(go.Scatter(
                x=mental_health_df['date_recorded'],
                y=mental_health_df['anxiety_level'],
                mode='lines+markers',
                name='Anxiety',
                line=dict(color='orange', width=2)
            ))
            fig_anxiety.update_layout(
                title='Anxiety Level Trend',
                xaxis_title='Date',
                yaxis_title='Anxiety Level (1-10)',
                yaxis=dict(range=[0, 11])
            )
            st.plotly_chart(fig_anxiety, use_container_width=True)
        
        with col2:
            fig_depression = go.Figure()
            fig_depression.add_trace(go.Scatter(
                x=mental_health_df['date_recorded'],
                y=mental_health_df['depression_level'],
                mode='lines+markers',
                name='Depression',
                line=dict(color='purple', width=2)
            ))
            fig_depression.update_layout(
                title='Depression Level Trend',
                xaxis_title='Date',
                yaxis_title='Depression Level (1-10)',
                yaxis=dict(range=[0, 11])
            )
            st.plotly_chart(fig_depression, use_container_width=True)
        
    else:
        st.info("No mental health records found. Log your first record in the 'Log Mental Health' tab.")

with tab3:
    st.markdown("### Correlation Between Mental Health and Heart Risk")
    
    mental_health_df = get_mental_health_history()
    vitals_df = get_vitals_history()
    
    if not mental_health_df.empty and not vitals_df.empty:
        mental_health_df['date_recorded'] = pd.to_datetime(mental_health_df['date_recorded']).dt.date
        vitals_df['date_recorded'] = pd.to_datetime(vitals_df['date_recorded']).dt.date
        
        merged_df = pd.merge(
            mental_health_df,
            vitals_df[['date_recorded', 'prediction_result', 'resting_bp', 'max_heart_rate']],
            on='date_recorded',
            how='inner',
            suffixes=('_mental', '_vitals')
        )
        
        if not merged_df.empty:
            st.markdown("#### Key Correlations")
            
            correlations = merged_df[[
                'stress_level', 'sleep_hours', 'anxiety_level', 
                'depression_level', 'physical_activity_min', 
                'prediction_result', 'resting_bp', 'max_heart_rate'
            ]].corr()
            
            fig_corr = go.Figure(data=go.Heatmap(
                z=correlations.values,
                x=correlations.columns,
                y=correlations.columns,
                colorscale='RdBu_r',
                zmid=0,
                text=correlations.values,
                texttemplate='%{text:.2f}',
                textfont={"size": 10}
            ))
            fig_corr.update_layout(
                title='Correlation Matrix: Mental Health & Heart Metrics',
                height=600
            )
            st.plotly_chart(fig_corr, use_container_width=True)
            
            st.markdown("---")
            st.markdown("#### Stress vs Heart Risk")
            
            fig_scatter = px.scatter(
                merged_df,
                x='stress_level',
                y='prediction_result',
                labels={'stress_level': 'Stress Level', 'prediction_result': 'Heart Risk Probability'},
                title='Relationship Between Stress and Heart Disease Risk'
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_sleep = px.scatter(
                    merged_df,
                    x='sleep_hours',
                    y='prediction_result',
                    labels={'sleep_hours': 'Sleep Hours', 'prediction_result': 'Heart Risk'},
                    title='Sleep vs Heart Risk'
                )
                st.plotly_chart(fig_sleep, use_container_width=True)
            
            with col2:
                fig_activity = px.scatter(
                    merged_df,
                    x='physical_activity_min',
                    y='prediction_result',
                    labels={'physical_activity_min': 'Physical Activity (min)', 'prediction_result': 'Heart Risk'},
                    title='Physical Activity vs Heart Risk'
                )
                st.plotly_chart(fig_activity, use_container_width=True)
            
            st.markdown("---")
            st.markdown("#### Insights")
            
            stress_corr = correlations.loc['stress_level', 'prediction_result']
            sleep_corr = correlations.loc['sleep_hours', 'prediction_result']
            activity_corr = correlations.loc['physical_activity_min', 'prediction_result']
            
            if abs(stress_corr) > 0.3:
                st.warning(f"Strong correlation detected between stress and heart risk (r={stress_corr:.2f})")
            
            if abs(sleep_corr) > 0.3:
                st.info(f"Notable correlation between sleep and heart risk (r={sleep_corr:.2f})")
            
            if abs(activity_corr) > 0.3:
                st.success(f"Physical activity shows correlation with heart risk (r={activity_corr:.2f})")
            
        else:
            st.info("No matching dates found between mental health and vitals records.")
    
    else:
        st.info("Need both mental health and vitals data to show correlations.")

st.markdown("---")
st.markdown("""
**Note:** Mental health and stress have significant impacts on cardiovascular health. 
Regular monitoring can help identify patterns and triggers. This information is for 
educational purposes and should not replace professional mental health or medical advice.
""")
