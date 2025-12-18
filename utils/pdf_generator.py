from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
import io
import base64
import pandas as pd
from datetime import datetime
import streamlit as st

def generate_health_report(user_data, prediction_results, vitals_history, recommendations, medications=None):
    """Generate comprehensive health report as PDF"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.darkblue,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.darkred,
        spaceBefore=20,
        spaceAfter=10
    )
    
    # Title
    story.append(Paragraph("HeartSafe - Health Report", title_style))
    story.append(Spacer(1, 12))
    
    # Report date
    report_date = datetime.now().strftime("%B %d, %Y")
    story.append(Paragraph(f"Generated on: {report_date}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # User Information Section
    story.append(Paragraph("Patient Information", heading_style))
    
    user_info_data = [
        ['Age', str(user_data.get('age', 'N/A'))],
        ['Gender', str(user_data.get('gender', 'N/A'))],
        ['Blood Pressure', f"{user_data.get('resting_bp', 'N/A')} mmHg"],
        ['Cholesterol', f"{user_data.get('cholesterol', 'N/A')} mg/dl"],
        ['Max Heart Rate', f"{user_data.get('max_heart_rate', 'N/A')} bpm"]
    ]
    
    user_table = Table(user_info_data, colWidths=[2*inch, 2*inch])
    user_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(user_table)
    story.append(Spacer(1, 20))
    
    # Prediction Results Section
    story.append(Paragraph("Heart Disease Risk Assessment", heading_style))
    
    for model_name, result in prediction_results.items():
        risk_score = result.get('score', 0) * 100
        risk_category = result.get('category', 'Unknown')
        
        story.append(Paragraph(f"<b>{model_name.replace('_', ' ').title()}</b>", styles['Normal']))
        story.append(Paragraph(f"Risk Score: {risk_score:.1f}%", styles['Normal']))
        story.append(Paragraph(f"Risk Category: {risk_category}", styles['Normal']))
        story.append(Spacer(1, 10))
    
    story.append(Spacer(1, 20))
    
    # Recommendations Section
    story.append(Paragraph("Personalized Recommendations", heading_style))
    
    for category, recs in recommendations.items():
        story.append(Paragraph(f"<b>{category.replace('_', ' ').title()}</b>", styles['Normal']))
        for rec in recs:
            story.append(Paragraph(f"• {rec}", styles['Normal']))
        story.append(Spacer(1, 10))
    
    story.append(Spacer(1, 20))
    
    # Vitals History Section
    if not vitals_history.empty:
        story.append(Paragraph("Recent Vitals History", heading_style))
        
        # Get last 5 entries
        recent_vitals = vitals_history.head(5)
        
        vitals_data = [['Date', 'Blood Pressure', 'Cholesterol', 'Heart Rate', 'Risk Score']]
        
        for _, row in recent_vitals.iterrows():
            vitals_data.append([
                pd.to_datetime(row['date_recorded']).strftime('%Y-%m-%d'),
                f"{row.get('resting_bp', 'N/A')}",
                f"{row.get('cholesterol', 'N/A')}",
                f"{row.get('max_heart_rate', 'N/A')}",
                f"{row.get('prediction_result', 0) * 100:.1f}%"
            ])
        
        vitals_table = Table(vitals_data, colWidths=[1.2*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        vitals_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8)
        ]))
        
        story.append(vitals_table)
        story.append(Spacer(1, 20))
    
    # Medications Section
    if medications is not None and not medications.empty:
        story.append(Paragraph("Current Medications", heading_style))
        
        meds_data = [['Medication', 'Dosage', 'Frequency', 'Start Date']]
        
        for _, med in medications.iterrows():
            meds_data.append([
                med['medication_name'],
                med['dosage'],
                med['frequency'],
                pd.to_datetime(med['start_date']).strftime('%Y-%m-%d') if pd.notna(med['start_date']) else 'N/A'
            ])
        
        meds_table = Table(meds_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
        meds_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8)
        ]))
        
        story.append(meds_table)
        story.append(Spacer(1, 20))
    
    # Disclaimer
    story.append(Paragraph("Important Disclaimer", heading_style))
    disclaimer_text = """
    This report is generated by an AI-powered system for educational and informational purposes only. 
    The predictions and recommendations provided should not be considered as medical advice. 
    Always consult with qualified healthcare professionals for proper medical evaluation, diagnosis, 
    and treatment decisions. The AI system's predictions are based on statistical models and may not 
    account for all individual health factors.
    """
    story.append(Paragraph(disclaimer_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    return buffer

def create_download_link(pdf_buffer, filename):
    """Create download link for PDF"""
    b64 = base64.b64encode(pdf_buffer.read()).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">Download Health Report (PDF)</a>'
    return href

def generate_quick_summary(prediction_results):
    """Generate quick text summary of results"""
    summary = []
    
    # Overall risk assessment
    avg_risk = sum(result.get('score', 0) for result in prediction_results.values()) / len(prediction_results)
    
    if avg_risk < 0.3:
        summary.append("Overall Assessment: Low risk for heart disease")
    elif avg_risk < 0.7:
        summary.append("Overall Assessment: Moderate risk for heart disease")
    else:
        summary.append("Overall Assessment: High risk for heart disease")
    
    # Model agreement
    risk_categories = [result.get('category', '') for result in prediction_results.values()]
    unique_categories = set(risk_categories)
    
    if len(unique_categories) == 1:
        summary.append(f"All models agree on {list(unique_categories)[0]} classification")
    else:
        summary.append("Models show mixed predictions - consider additional evaluation")
    
    return summary
