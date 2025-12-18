HeartSafe – AI Heart Disease Prediction System ❤️

HeartSafe is a smart, interactive web application designed to estimate heart disease risk using machine learning. It goes beyond a basic prediction tool by combining AI models, health tracking, and personalized insights into a single, easy-to-use platform. Built for learning, experimentation, and awareness, HeartSafe turns raw health data into meaningful understanding.

Why HeartSafe?

Heart disease is often silent until it is serious. HeartSafe focuses on early awareness by analyzing clinical parameters, lifestyle patterns, and mental health indicators. Instead of showing a single number, it explains risk, tracks progress over time, and helps users understand how daily choices can influence heart health.

Key Features

Core Capabilities

1. Multi-Model Risk Prediction – Uses Logistic Regression, Random Forest, and XGBoost to provide a balanced and reliable risk assessment.
2. Interactive Dashboard – Clean visualizations for vitals, trends, and predictions.
3. AI Health Chatbot – Conversational assistant for general heart-health guidance (optional OpenAI integration).
4. Health History Tracker – Stores and visualizes vitals and prediction history over time.
5. Scenario Simulator – Explore how changes in lifestyle may impact heart risk.
6. Smart Recommendations – Actionable suggestions tailored to individual risk factors.
7. Medication Tracker – Simple logging and monitoring of heart-related medications.
8. Community Insights – View anonymized statistics to understand broader health patterns.
9. PDF Health Reports – Generate structured reports for review or sharing.

Advanced Enhancements

10. Family History & Genetic Risk – Record family heart conditions and estimate inherited risk.
11. Mental Health Integration – Track stress, sleep, anxiety, and their relationship to heart health.
12. Health Resource Finder – Locate nearby healthcare providers and telemedicine options.
13. Gamified Health Challenges 🏆 – Set goals, track progress, and stay motivated with points and achievements.
14. Voice Interface 🎙️ – Voice input and text-to-speech for accessibility and ease of use.

Technology Stack

• Frontend and App Framework: Streamlit
• Machine Learning: scikit-learn, XGBoost
• Data Processing: NumPy, Pandas
• Visualization: Plotly
• Reports: ReportLab
• Storage: Local JSON-based persistence

Local Installation

Prerequisites

• Python 3.11 or higher
• pip package manager

Installation Steps

1. Clone or download the project
   cd heartsafe-app

2. Install dependencies
   pip install joblib numpy pandas plotly reportlab scikit-learn streamlit xgboost

3. Optional chatbot support
   pip install openai

4. Create Streamlit configuration
   mkdir -p .streamlit

5. Add config file (.streamlit/config.toml)
   [server]
   headless = true
   address = "0.0.0.0"
   port = 5000

Running the Application

Start the app

streamlit run app.py --server.port 5000

Open in your browser

[http://localhost:5000](http://localhost:5000)

If the port is busy, use another one

streamlit run app.py --server.port 8501

Data Management

HeartSafe uses local JSON files instead of a database. This keeps the system simple, transparent, and easy to back up.

Stored files include:

• vitals_history.json – Health measurements
• medications.json – Medication logs
• predictions.json – Prediction history
• family_history.json – Family heart records
• mental_health.json – Stress and sleep tracking
• challenges.json – Health goals
• challenge_progress.json – Challenge tracking

Configuration (Optional)

AI Chatbot Setup

Set your OpenAI API key as an environment variable.

Linux or Mac
export OPENAI_API_KEY='your-api-key'
streamlit run app.py

Windows
set OPENAI_API_KEY=your-api-key
streamlit run app.py

Without the API key, all features except the chatbot remain fully functional.

How to Use HeartSafe

First-Time Setup

1. Upload a heart disease dataset (CSV format).
2. Train the prediction models from the main page.
3. Navigate to the Prediction section and enter health details.
4. Explore dashboards, trackers, and reports.

Prediction Parameters

• Age and Gender
• Chest Pain Type
• Blood Pressure and Cholesterol
• Fasting Blood Sugar
• ECG Results
• Maximum Heart Rate
• Exercise-Induced Angina
• ST Depression and Slope
• Number of Major Vessels
• Thalassemia

Privacy and Safety

• All data stays on your local machine
• No external data sharing
• JSON files are readable and removable at any time
• Delete the data folder to erase all records

System Requirements

• RAM: 4 GB minimum (8 GB recommended)
• Storage: Around 500 MB
• Internet: Only required for chatbot feature
• Browser: Chrome, Firefox, Edge, or Safari

License

This project is intended for educational and personal learning purposes.

Disclaimer ⚠️

This application is not a medical device. It is designed for educational and informational use only and should never replace professional medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals regarding medical concerns.
