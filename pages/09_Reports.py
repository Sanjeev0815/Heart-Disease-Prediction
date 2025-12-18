import streamlit as st
import pandas as pd
from datetime import datetime
from utils.storage import get_vitals_history, get_predictions_history
from utils.pdf_generator import generate_health_report, generate_quick_summary
from utils.models import get_risk_category
import base64

st.set_page_config(page_title="Health Reports", page_icon="H", layout="wide")

st.title("Health Report Generator")
st.markdown("Generate comprehensive PDF reports with your health data, predictions, and personalized recommendations.")

# Check for required data
if 'latest_prediction' not in st.session_state:
    st.warning("Please make a prediction first to generate a health report.")
    if st.button("Make Prediction"):
        st.switch_page("pages/01_Prediction.py")
    st.stop()

# Get data
latest_prediction = st.session_state['latest_prediction']
vitals_history = get_vitals_history()
predictions_history = get_predictions_history()

# Report overview
st.markdown("---")
st.subheader("Report Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Current Risk Score", f"{latest_prediction['score']:.1%}")

with col2:
    st.metric("Risk Category", latest_prediction['category'])

with col3:
    total_records = len(vitals_history) if not vitals_history.empty else 0
    st.metric("Health Records", total_records)

with col4:
    total_predictions = len(predictions_history) if not predictions_history.empty else 0
    st.metric("Total Predictions", total_predictions)

# Report customization
st.markdown("---")
st.subheader("Report Options")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Report Sections")
    
    include_prediction = st.checkbox("Prediction Results", value=True, disabled=True, help="Always included")
    include_vitals = st.checkbox("Vitals History", value=True, disabled=len(vitals_history) == 0)
    include_recommendations = st.checkbox("Health Recommendations", value=True)
    include_trends = st.checkbox("Health Trends Analysis", value=len(vitals_history) > 1, disabled=len(vitals_history) <= 1)

with col2:
    st.markdown("#### Report Format")
    
    report_type = st.radio("Report Type", [
        "Comprehensive Report", 
        "Summary Report", 
        "Medical Provider Report"
    ])
    
    date_range = st.selectbox("Data Range", [
        "All available data",
        "Last 3 months", 
        "Last 6 months",
        "Last year"
    ])

# Generate report preview
st.markdown("---")
st.subheader("Report Preview")

def get_filtered_data(vitals_df, date_range):
    """Filter data based on selected date range"""
    if vitals_df.empty or date_range == "All available data":
        return vitals_df
    
    current_date = datetime.now()
    
    if date_range == "Last 3 months":
        cutoff_date = current_date - pd.DateOffset(months=3)
    elif date_range == "Last 6 months":
        cutoff_date = current_date - pd.DateOffset(months=6)
    else:  # Last year
        cutoff_date = current_date - pd.DateOffset(years=1)
    
    vitals_df['date_recorded'] = pd.to_datetime(vitals_df['date_recorded'])
    return vitals_df[vitals_df['date_recorded'] >= cutoff_date]

# Filter data based on selection
filtered_vitals = get_filtered_data(vitals_history, date_range)

# Show what will be included
with st.expander("Report Contents Preview", expanded=True):
    if include_prediction:
        st.markdown(" **Prediction Results Section**")
        st.write(f"• Current risk assessment: {latest_prediction['score']:.1%} ({latest_prediction['category']})")
        st.write(f"• Model used: {latest_prediction['model'].replace('_', ' ').title()}")
        st.write("• Risk factor analysis and contributing factors")
        
    if include_vitals and not filtered_vitals.empty:
        st.markdown(" **Vitals History Section**")
        st.write(f"• {len(filtered_vitals)} health records from {date_range.lower()}")
        st.write("• Blood pressure, cholesterol, and heart rate trends")
        st.write("• Risk score progression over time")
        
    if include_recommendations:
        st.markdown(" **Health Recommendations Section**")
        st.write("• Personalized lifestyle recommendations")
        st.write("• Dietary guidelines based on risk factors")
        st.write("• Exercise and activity suggestions")
        st.write("• Medical care recommendations")
        
    if include_trends and len(filtered_vitals) > 1:
        st.markdown(" **Health Trends Analysis**")
        st.write("• Risk score trends and patterns")
        st.write("• Vitals correlation analysis")
        st.write("• Progress toward health goals")

# Generate recommendations for report
def generate_report_recommendations(user_data, risk_score, risk_category):
    """Generate recommendations for the PDF report"""
    recommendations = {
        'immediate_actions': [],
        'lifestyle_changes': [],
        'dietary_guidelines': [],
        'exercise_program': [],
        'medical_follow_up': []
    }
    
    # Immediate actions based on risk level
    if risk_category == "High Risk":
        recommendations['immediate_actions'].extend([
            "Schedule immediate consultation with cardiologist",
            "Monitor blood pressure daily",
            "Keep emergency contact information readily available",
            "Consider cardiac rehabilitation program evaluation"
        ])
    elif risk_category == "Medium Risk":
        recommendations['immediate_actions'].extend([
            "Schedule appointment with primary care physician",
            "Begin monitoring blood pressure regularly",
            "Discuss family history with healthcare provider"
        ])
    
    # Lifestyle recommendations based on specific risk factors
    bp = user_data.get('resting_bp', 120)
    if bp >= 140:
        recommendations['lifestyle_changes'].append("Reduce sodium intake to less than 2,300mg daily")
        recommendations['dietary_guidelines'].append("Follow DASH diet principles for blood pressure control")
    
    chol = user_data.get('cholesterol', 200)
    if chol >= 240:
        recommendations['dietary_guidelines'].extend([
            "Limit saturated fat to less than 7% of daily calories",
            "Include omega-3 rich foods (fish, walnuts, flaxseeds)"
        ])
    
    # Exercise recommendations
    max_hr = user_data.get('max_heart_rate', 150)
    age = user_data.get('age', 50)
    if max_hr < (220 - age) * 0.7:
        recommendations['exercise_program'].extend([
            "Start with low-intensity exercise 3-4 times per week",
            "Gradually increase to 150 minutes moderate activity weekly",
            "Consider supervised exercise program initially"
        ])
    else:
        recommendations['exercise_program'].extend([
            "Maintain 150+ minutes moderate aerobic activity weekly",
            "Include strength training 2-3 times per week",
            "Add flexibility and balance exercises"
        ])
    
    # Medical follow-up
    if risk_category != "Low Risk":
        recommendations['medical_follow_up'].extend([
            "Regular blood pressure and cholesterol monitoring",
            "Annual comprehensive cardiac evaluation",
            "Medication compliance review if applicable"
        ])
    
    # General recommendations
    recommendations['lifestyle_changes'].extend([
        "Maintain healthy sleep schedule (7-9 hours nightly)",
        "Practice stress management techniques",
        "Avoid tobacco use and limit alcohol consumption"
    ])
    
    return recommendations

# Generate report data
user_data = latest_prediction['input_data']
recommendations = generate_report_recommendations(
    user_data, 
    latest_prediction['score'], 
    latest_prediction['category']
)

# Prepare prediction results for all models
prediction_results = {}

# Get predictions for all models if available
if 'model_accuracies' in st.session_state:
    from utils.models import make_prediction
    
    models = ['logistic', 'random_forest', 'xgboost']
    for model_name in models:
        pred, _ = make_prediction(user_data, model_name)
        if pred is not None:
            prediction_results[model_name] = {
                'score': pred,
                'category': get_risk_category(pred)
            }
else:
    # Use current prediction only
    prediction_results[latest_prediction['model']] = {
        'score': latest_prediction['score'],
        'category': latest_prediction['category']
    }

# Report generation
st.markdown("---")
st.subheader("Generate Report")

col1, col2 = st.columns(2)

with col1:
    # Quick summary
    st.markdown("#### Quick Summary")
    summary_points = generate_quick_summary(prediction_results)
    for point in summary_points:
        st.write(f"• {point}")
    
    # Additional insights
    if len(filtered_vitals) > 1:
        current_risk = filtered_vitals.iloc[0]['prediction_result']
        previous_risk = filtered_vitals.iloc[1]['prediction_result']
        trend = "improving" if current_risk < previous_risk else "stable" if current_risk == previous_risk else "worsening"
        st.write(f"• Risk trend: {trend}")

with col2:
    # Generate PDF button
    st.markdown("#### Download Report")
    
    report_filename = f"HeartSafe_Health_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    
    if st.button("Generate PDF Report", type="primary"):
        with st.spinner("Generating your health report..."):
            try:
                # Prepare data for PDF generation
                pdf_vitals = filtered_vitals if include_vitals else pd.DataFrame()
                
                # Generate PDF
                pdf_buffer = generate_health_report(
                    user_data=user_data,
                    prediction_results=prediction_results,
                    vitals_history=pdf_vitals,
                    recommendations=recommendations,
                    medications=None
                )
                
                # Create download button
                b64 = base64.b64encode(pdf_buffer.read()).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="{report_filename}">Download Health Report PDF</a>'
                
                st.success("Report generated successfully!")
                st.markdown(href, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")
                st.error("Please ensure all required data is available and try again.")

# Report history and management
st.markdown("---")
st.subheader("Report History & Management")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Previous Reports")
    st.info("Report history feature would track previously generated reports with timestamps and settings.")
    
    # Placeholder for report history
    st.write("No previous reports found.")
    
    if st.button("View All Reports"):
        st.info("This feature would show a list of all previously generated reports.")

with col2:
    st.markdown("#### Export Options")
    
    # Export raw data
    if st.button("Export Raw Data (CSV)"):
        if not vitals_history.empty:
            csv_data = vitals_history.to_csv(index=False)
            st.download_button(
                label="Download Vitals History CSV",
                data=csv_data,
                file_name=f"vitals_history_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("No vitals history available for export.")

# Sharing and privacy
st.markdown("---")
st.subheader("Sharing & Privacy")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Report Sharing")
    st.info("""
    **Medical Provider Sharing**: Reports can be shared directly with healthcare providers 
    for medical consultations and treatment planning.
    
    **Family Sharing**: Share summary reports with family members for health awareness 
    and emergency preparedness.
    
    **Personal Records**: Keep copies for personal health record management and insurance 
    documentation.
    """)

with col2:
    st.markdown("#### Privacy Protection")
    st.success("""
    **Data Security**: All reports are generated locally and contain only your personal data.
    
    **No Cloud Storage**: Reports are not stored on external servers unless you choose to save them.
    
    **Anonymized Insights**: Community comparisons use only aggregated, anonymous data.
    
    **Your Control**: You decide what to include in each report and how to share it.
    """)

# Report customization tips
st.markdown("---")
with st.expander("Report Customization Tips"):
    st.markdown("""
    ### Getting the Most from Your Health Reports
    
    **For Medical Appointments:**
    - Include all available vitals history
    - Add current medications and dosages
    - Select "Medical Provider Report" format
    - Include trends analysis if available
    
    **For Personal Tracking:**
    - Generate monthly summary reports
    - Focus on trend analysis and progress
    - Include recommendations for goal setting
    
    **For Family/Emergency Contacts:**
    - Include current medications and emergency contacts
    - Focus on summary format with key risk factors
    - Keep reports updated quarterly
    
    **For Insurance/Employment:**
    - Use comprehensive report format
    - Include all historical data
    - Ensure dates and medical information are complete
    """)

# Navigation
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("View Dashboard"):
        st.switch_page("pages/02_Dashboard.py")

with col2:
    if st.button("Update Prediction"):
        st.switch_page("pages/01_Prediction.py")

with col3:
    if st.button("Track Medications"):
        st.switch_page("pages/07_Medication_Tracker.py")

with col4:
    if st.button("Get Recommendations"):
        st.switch_page("pages/06_Recommendations.py")
