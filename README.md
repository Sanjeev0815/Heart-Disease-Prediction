HeartSafe - AI Heart Disease Prediction System

A comprehensive web application for predicting heart disease risk using machine learning models, with personalized health recommendations, medication tracking, and advanced health monitoring features.

Features

Core Features

Multi-Model Prediction – Heart disease risk assessment using Logistic Regression, Random Forest, and XGBoost

Interactive Dashboard – Real-time health metrics and risk visualization

AI Health Chatbot – Conversational AI for health guidance (requires OpenAI API key)

Historical Tracker – Track vitals and health metrics over time

Scenario Simulator – Test how lifestyle changes affect risk

Smart Recommendations – Personalized health advice based on risk factors

Medication Tracker – Log and monitor heart-related medications

Community Insights – Anonymized health statistics

Health Reports – Generate comprehensive PDF health reports

New Features
10. Genetic & Family History – Track family heart health history and genetic risk factors
11. Stress & Mental Health Integration – Monitor stress, sleep, anxiety, and their correlation with heart health
12. Health Resource Finder – Find nearby healthcare providers and telemedicine options
13. Gamified Challenges – Set health goals, track progress, and earn points
14. Voice Interface – Voice input and text-to-speech capabilities for accessibility

Local Installation

Prerequisites
Python 3.11 or higher
pip (Python package manager)

Installation Steps

Clone or download the repository
cd heartsafe-app

Install required packages
pip install joblib numpy pandas plotly reportlab scikit-learn streamlit xgboost

Optional: Install OpenAI for chatbot functionality
pip install openai

Create Streamlit configuration (if not exists)
mkdir -p .streamlit

Create .streamlit/config.toml file with the following content:
[server]
headless = true
address = "0.0.0.0"
port = 5000

Running the Application

Start the application
streamlit run app.py --server.port 5000

The application will be available at:
http://localhost:5000

Using a different port
If port 5000 is unavailable, you can use any port:
streamlit run app.py --server.port 8501

Data Storage

The application uses JSON files for data storage (no database required):
All data is stored in the data/ directory
Files are automatically created on first run
Data persists between sessions
Easy to backup by copying the data/ folder

Data files:
vitals_history.json – Health vitals and measurements
medications.json – Medication records
predictions.json – Prediction history
family_history.json – Family health history
mental_health.json – Mental health tracking
challenges.json – Health challenges and goals
challenge_progress.json – Challenge progress tracking

Configuration

OpenAI API Key (Optional)
For chatbot functionality, set your OpenAI API key as an environment variable:

Linux / Mac
export OPENAI_API_KEY='your-api-key-here'
streamlit run app.py

Windows
set OPENAI_API_KEY=your-api-key-here
streamlit run app.py

The application works without an API key, but the chatbot will not be available.

Using the Application

First Time Setup

Upload Dataset
Open the main page
Upload a heart disease dataset (CSV format)
Click "Train Prediction Models"
Wait for models to train

Make Predictions
Navigate to "Prediction" page
Enter your health parameters
Get risk assessment from multiple models

Explore Features
Use the sidebar to navigate between features
Track your health metrics over time
Log medications and family history
Create health challenges
Generate PDF reports

Features Detail

Prediction Engine
Input parameters include:
Age, Gender
Chest Pain Type
Blood Pressure, Cholesterol
Fasting Blood Sugar
ECG Results
Maximum Heart Rate
Exercise Angina
ST Depression, ST Slope
Number of Major Vessels
Thalassemia

Family History Tracking
Record family members with heart conditions
Track age at diagnosis
Calculate genetic risk score
View combined lifestyle and genetic risk

Mental Health Integration
Log stress, anxiety, depression levels
Track sleep hours and physical activity
View correlations with heart health
Visualize mental health trends

Gamified Challenges
Create custom health goals
Track progress over time
Earn points for achievements
View achievement levels and badges

Voice Interface
Browser-based speech recognition (no setup required)
Text-to-speech for accessibility
Voice commands for data entry
Multiple voice options

Troubleshooting

Port Already in Use
streamlit run app.py --server.port 8080

Missing Dependencies
pip install -r pyproject.toml

Data Not Persisting
Ensure the data/ directory exists
Check file permissions
Verify JSON files are not corrupted

Models Not Loading
Upload a valid dataset
Ensure dataset has required columns
Re-train models from the main page

Data Privacy

All data is stored locally on your machine
No data is sent to external servers (except OpenAI API if used)
JSON files are plain text and can be reviewed or edited
Easy to delete all data by removing the data/ folder

System Requirements

RAM: 4GB minimum, 8GB recommended
Storage: 500MB for application and data
Internet: Only required for OpenAI chatbot functionality
Browser: Chrome, Firefox, Safari, or Edge

Support

For issues or questions:
Check the troubleshooting section above
Review application logs in the terminal
Verify all dependencies are installed correctly

License

This project is for educational and personal use.

Disclaimer

Important: This application is for informational and educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with any questions regarding medical conditions.
