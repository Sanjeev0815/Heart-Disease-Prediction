import streamlit as st
import pandas as pd
import numpy as np
from utils.storage import init_storage
from utils.models import load_or_train_models

# Page configuration
st.set_page_config(
    page_title="HeartSafe - AI Heart Disease Prediction",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize storage
init_storage()

# Custom CSS for better dark theme
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #FF4B4B;
    }
    .metric-container {
        background-color: #262730;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">HeartSafe</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #FAFAFA;">AI-Powered Heart Disease Prediction & Health Management</p>', unsafe_allow_html=True)
    
    # Dataset upload section
    st.markdown("---")
    st.header("Dataset Management")
    
    uploaded_file = st.file_uploader(
        "Upload your heart disease dataset (CSV format)",
        type=['csv'],
        help="Upload a CSV file containing heart disease data for training the prediction models"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"Dataset uploaded successfully! Shape: {df.shape}")
            
            # Store dataset in session state
            st.session_state['dataset'] = df
            
            # Display basic dataset info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="metric-container"><h3>Rows</h3><h2>{}</h2></div>'.format(df.shape[0]), unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="metric-container"><h3>Columns</h3><h2>{}</h2></div>'.format(df.shape[1]), unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="metric-container"><h3>Missing Values</h3><h2>{}</h2></div>'.format(df.isnull().sum().sum()), unsafe_allow_html=True)
            
            # Show dataset preview
            st.subheader("Dataset Preview")
            st.dataframe(df.head())
            
            # Train models with uploaded dataset
            if st.button("Train Prediction Models", type="primary"):
                with st.spinner("Training models... This may take a few minutes."):
                    models, accuracies, feature_names = load_or_train_models(df)
                    if models:
                        st.session_state['models'] = models
                        st.session_state['model_accuracies'] = accuracies
                        st.session_state['feature_names'] = feature_names
                        st.success("Models trained successfully!")
                        
                        # Display model accuracies
                        if accuracies:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Logistic Regression", f"{accuracies.get('logistic', 0):.3f}")
                            with col2:
                                st.metric("Random Forest", f"{accuracies.get('random_forest', 0):.3f}")
                            with col3:
                                st.metric("XGBoost", f"{accuracies.get('xgboost', 0):.3f}")
            
        except Exception as e:
            st.error(f"Error loading dataset: {str(e)}")
    
    # App features overview
    st.markdown("---")
    st.header("Application Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>Multi-Model Prediction</h3>
            <p>Get heart disease risk predictions from Logistic Regression, Random Forest, and XGBoost models with accuracy comparison.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>Interactive Dashboard</h3>
            <p>Visualize your risk with color-coded gauge charts and feature contribution analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>AI Chatbot</h3>
            <p>Get personalized guidance and explanations about your heart health through conversational AI.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>Historical Tracking</h3>
            <p>Track your vitals over time and visualize trends with interactive charts.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>Scenario Simulator</h3>
            <p>Test how lifestyle changes could affect your heart disease risk with what-if analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>Smart Recommendations</h3>
            <p>Receive personalized health recommendations based on your risk factors and predictions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>Medication Tracker</h3>
            <p>Log and track your heart-related medications with reminder capabilities.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>Health Reports</h3>
            <p>Generate comprehensive PDF reports with predictions, trends, and recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation instructions
    st.markdown("---")
    st.info("Navigate through the different features using the sidebar menu. Start by uploading your dataset and training the models above.")

if __name__ == "__main__":
    main()
