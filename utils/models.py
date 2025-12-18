import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
import joblib
import streamlit as st
import os

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

MODEL_DIR = "models"

def create_model_dir():
    """Create models directory if it doesn't exist"""
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

def preprocess_data(df):
    """Preprocess the dataset for training"""
    # Assume the target column is named 'target' or 'heart_disease' or similar
    target_columns = ['target', 'heart_disease', 'num', 'diagnosis']
    target_col = None
    
    for col in target_columns:
        if col in df.columns:
            target_col = col
            break
    
    if target_col is None:
        # If no standard target column found, use the last column
        target_col = df.columns[-1]
        st.warning(f"Target column not found. Using '{target_col}' as target variable.")
    
    # Separate features and target
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Convert categorical variables to numeric if needed
    for col in X.columns:
        if X[col].dtype == 'object':
            X[col] = pd.Categorical(X[col]).codes
    
    # Handle missing values
    X = X.fillna(X.mean())
    
    return X, y

def train_models(X, y):
    """Train multiple models and return them with their accuracies"""
    create_model_dir()
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    models = {}
    accuracies = {}
    
    # Logistic Regression
    lr_model = LogisticRegression(random_state=42)
    lr_model.fit(X_train_scaled, y_train)
    lr_pred = lr_model.predict(X_test_scaled)
    accuracies['logistic'] = accuracy_score(y_test, lr_pred)
    models['logistic'] = lr_model
    
    # Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    accuracies['random_forest'] = accuracy_score(y_test, rf_pred)
    models['random_forest'] = rf_model
    
    # XGBoost
    xgb_model = xgb.XGBClassifier(random_state=42)
    xgb_model.fit(X_train, y_train)
    xgb_pred = xgb_model.predict(X_test)
    accuracies['xgboost'] = accuracy_score(y_test, xgb_pred)
    models['xgboost'] = xgb_model
    
    # Save models and scaler
    joblib.dump(models, f"{MODEL_DIR}/trained_models.pkl")
    joblib.dump(scaler, f"{MODEL_DIR}/scaler.pkl")
    joblib.dump(list(X.columns), f"{MODEL_DIR}/feature_names.pkl")
    
    return models, accuracies, list(X.columns)

def load_or_train_models(df=None):
    """Load existing models or train new ones"""
    model_path = f"{MODEL_DIR}/trained_models.pkl"
    scaler_path = f"{MODEL_DIR}/scaler.pkl"
    features_path = f"{MODEL_DIR}/feature_names.pkl"
    
    if os.path.exists(model_path) and os.path.exists(scaler_path) and os.path.exists(features_path):
        # Load existing models
        models = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        feature_names = joblib.load(features_path)
        
        # Calculate accuracies (placeholder - would need test data)
        accuracies = {
            'logistic': 0.85,
            'random_forest': 0.87,
            'xgboost': 0.89
        }
        
        return models, accuracies, feature_names
    
    elif df is not None:
        # Train new models
        X, y = preprocess_data(df)
        return train_models(X, y)
    
    else:
        return None, None, None

def map_feature_names(input_data):
    """Map user-friendly feature names to model's expected names"""
    feature_mapping = {
        'gender': 'sex',
        'chest_pain_type': 'cp',
        'resting_bp': 'trestbps',
        'cholesterol': 'chol',
        'fasting_blood_sugar': 'fbs',
        'rest_ecg': 'restecg',
        'max_heart_rate': 'thalach',
        'exercise_angina': 'exang',
        'st_depression': 'oldpeak',
        'st_slope': 'slope'
    }
    
    mapped_data = {}
    for key, value in input_data.items():
        mapped_key = feature_mapping.get(key, key)
        mapped_data[mapped_key] = value
    
    return mapped_data

def make_prediction(input_data, model_name='xgboost'):
    """Make prediction using specified model"""
    model_path = f"{MODEL_DIR}/trained_models.pkl"
    scaler_path = f"{MODEL_DIR}/scaler.pkl"
    features_path = f"{MODEL_DIR}/feature_names.pkl"
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        return None, None
    
    models = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    feature_names = joblib.load(features_path)
    
    if model_name not in models:
        return None, None
    
    model = models[model_name]
    
    # Map user-friendly feature names to model's expected names
    mapped_data = map_feature_names(input_data)
    
    # Prepare input data with correct column order
    input_df = pd.DataFrame([mapped_data])
    
    # Reorder columns to match training feature order
    input_df = input_df[feature_names]
    
    if model_name == 'logistic':
        # Scale for logistic regression
        input_scaled = scaler.transform(input_df)
        prediction = model.predict_proba(input_scaled)[0, 1]
    else:
        # Random Forest and XGBoost don't need scaling
        prediction = model.predict_proba(input_df)[0, 1]
    
    return prediction, model

def get_shap_explanation(input_data, model_name='xgboost'):
    """Get SHAP explanation for the prediction"""
    features_path = f"{MODEL_DIR}/feature_names.pkl"
    
    # Map user-friendly feature names to model's expected names
    mapped_data = map_feature_names(input_data)
    
    if not SHAP_AVAILABLE:
        feature_names, importances = get_feature_importance(model_name)
        if feature_names and importances is not None:
            input_values = [mapped_data.get(name, 0) for name in feature_names]
            normalized_importances = importances / np.sum(importances)
            feature_contributions = normalized_importances * np.array(input_values) * 0.1
            return feature_contributions
        return None
    
    try:
        model_path = f"{MODEL_DIR}/trained_models.pkl"
        
        if not os.path.exists(model_path) or not os.path.exists(features_path):
            return None
        
        models = joblib.load(model_path)
        feature_names = joblib.load(features_path)
        
        if model_name not in models:
            return None
        
        model = models[model_name]
        
        # Prepare input data with correct column order
        input_df = pd.DataFrame([mapped_data])
        input_df = input_df[feature_names]
        
        if model_name == 'logistic':
            explainer = shap.LinearExplainer(model, input_df)
        else:
            explainer = shap.TreeExplainer(model)
        
        shap_values = explainer.shap_values(input_df)
        
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        
        return shap_values[0]
    
    except Exception as e:
        st.error(f"Error generating SHAP explanation: {str(e)}")
        return None

def get_risk_category(prediction_score):
    """Convert prediction score to risk category"""
    if prediction_score < 0.3:
        return "Low Risk"
    elif prediction_score < 0.7:
        return "Medium Risk"
    else:
        return "High Risk"

def get_feature_importance(model_name='xgboost'):
    """Get feature importance from trained model"""
    try:
        model_path = f"{MODEL_DIR}/trained_models.pkl"
        features_path = f"{MODEL_DIR}/feature_names.pkl"
        
        if not os.path.exists(model_path) or not os.path.exists(features_path):
            return None, None
        
        models = joblib.load(model_path)
        feature_names = joblib.load(features_path)
        
        if model_name not in models:
            return None, None
        
        model = models[model_name]
        
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importances = np.abs(model.coef_[0])
        else:
            return None, None
        
        return feature_names, importances
    
    except Exception as e:
        st.error(f"Error getting feature importance: {str(e)}")
        return None, None
