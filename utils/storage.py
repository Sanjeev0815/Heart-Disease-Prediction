import json
import os
from datetime import datetime
import pandas as pd

DATA_DIR = "data"
VITALS_FILE = os.path.join(DATA_DIR, "vitals_history.json")
PREDICTIONS_FILE = os.path.join(DATA_DIR, "predictions.json")
MENTAL_HEALTH_FILE = os.path.join(DATA_DIR, "mental_health.json")

def init_storage():
    """Initialize storage directory and files"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    for file_path in [VITALS_FILE, PREDICTIONS_FILE, MENTAL_HEALTH_FILE]:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)

def load_data(file_path):
    """Load data from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except:
        return []

def save_data(file_path, data):
    """Save data to JSON file"""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def save_vitals(vitals_data, prediction_result, risk_category):
    """Save user vitals"""
    data = load_data(VITALS_FILE)
    
    # Convert numpy types to Python native types for JSON serialization
    clean_vitals = {}
    for key, value in vitals_data.items():
        if hasattr(value, 'item'):  # numpy types have .item() method
            clean_vitals[key] = value.item()
        else:
            clean_vitals[key] = value
    
    record = {
        'id': len(data) + 1,
        'user_id': 'default_user',
        'date_recorded': datetime.now().isoformat(),
        **clean_vitals,
        'prediction_result': float(prediction_result),
        'risk_category': risk_category
    }
    data.append(record)
    save_data(VITALS_FILE, data)

def get_vitals_history():
    """Retrieve vitals history"""
    data = load_data(VITALS_FILE)
    if data:
        df = pd.DataFrame(data)
        df = df.sort_values('date_recorded', ascending=False)
        return df
    return pd.DataFrame()

def save_prediction(model_used, input_features, prediction_score, risk_category, shap_values=None):
    """Save prediction result"""
    data = load_data(PREDICTIONS_FILE)
    record = {
        'id': len(data) + 1,
        'user_id': 'default_user',
        'prediction_date': datetime.now().isoformat(),
        'model_used': model_used,
        'input_features': str(input_features),
        'prediction_score': float(prediction_score),
        'risk_category': risk_category,
        'shap_values': str(shap_values) if shap_values else None
    }
    data.append(record)
    save_data(PREDICTIONS_FILE, data)

def get_predictions_history():
    """Retrieve prediction history"""
    data = load_data(PREDICTIONS_FILE)
    if data:
        df = pd.DataFrame(data)
        df = df.sort_values('prediction_date', ascending=False)
        return df
    return pd.DataFrame()

def get_community_stats():
    """Get anonymized community statistics"""
    df = get_vitals_history()
    
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()
    
    age_groups = pd.cut(df['age'], bins=[0, 30, 45, 60, 120], 
                        labels=['Under 30', '30-45', '46-60', 'Over 60'])
    df['age_group'] = age_groups
    
    age_stats = df.groupby('age_group').agg({
        'prediction_result': 'mean',
        'id': 'count'
    }).reset_index()
    age_stats.columns = ['age_group', 'avg_risk', 'count']
    
    gender_stats = df.groupby('gender').agg({
        'prediction_result': 'mean',
        'id': 'count'
    }).reset_index()
    gender_stats.columns = ['gender', 'avg_risk', 'count']
    
    return age_stats, gender_stats

def save_mental_health(mental_health_data):
    """Save mental health data"""
    data = load_data(MENTAL_HEALTH_FILE)
    record = {
        'id': len(data) + 1,
        'user_id': 'default_user',
        'date_recorded': datetime.now().isoformat(),
        **mental_health_data
    }
    data.append(record)
    save_data(MENTAL_HEALTH_FILE, data)

def get_mental_health_history():
    """Retrieve mental health history"""
    data = load_data(MENTAL_HEALTH_FILE)
    if data:
        df = pd.DataFrame(data)
        df = df.sort_values('date_recorded', ascending=False)
        return df
    return pd.DataFrame()
