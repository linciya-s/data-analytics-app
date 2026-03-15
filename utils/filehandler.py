"""
Utility functions for Data Analytics Application
"""

import streamlit as st
import pandas as pd
import PyPDF2
from io import BytesIO
import time
from datetime import datetime
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import json
from pathlib import Path


# ============================================================================
# FILE HANDLING UTILITIES
# ============================================================================

def read_csv_file(uploaded_file):
    """Read CSV file with multiple encoding attempts"""
    try:
        return pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            uploaded_file.seek(0)
            return pd.read_csv(uploaded_file, encoding='latin1')
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            return pd.read_csv(uploaded_file, encoding='cp1252')


def read_excel_file(uploaded_file):
    """Read Excel file (xlsx or xls)"""
    return pd.read_excel(uploaded_file)


def read_json_file(uploaded_file):
    """Read JSON file"""
    uploaded_file.seek(0)
    raw = json.load(uploaded_file)
    if isinstance(raw, list):
        return pd.json_normalize(raw)
    elif isinstance(raw, dict):
        return pd.json_normalize([raw])
    else:
        raise ValueError("Unsupported JSON structure")


def read_pdf_file(uploaded_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return pd.DataFrame({
            'Content': lines,
            'Line_Length': [len(line) for line in lines],
            'Word_Count': [len(line.split()) for line in lines]
        })
    except Exception as e:
        raise ValueError(f"Error reading PDF: {str(e)}")


# ============================================================================
# DATA ANALYSIS UTILITIES
# ============================================================================

def get_column_types(df):
    """Get numeric and categorical columns"""
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()
    return numeric_cols, categorical_cols


def get_data_summary(df):
    """Generate comprehensive data summary"""
    return {
        'rows': len(df),
        'columns': len(df.columns),
        'missing_values': df.isnull().sum().sum(),
        'duplicates': df.duplicated().sum(),
        'memory_usage': df.memory_usage(deep=True).sum() / 1024 ** 2  # MB
    }


def get_column_info(df):
    """Get detailed column information"""
    col_info = pd.DataFrame({
        "Column Name": df.columns.astype(str),
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,
        "Missing %": (df.isnull().sum().values / len(df) * 100).round(2),
        "Unique Values": df.nunique().values
    })
    return col_info


# ============================================================================
# EXPORT UTILITIES
# ============================================================================

def export_matplotlib_to_pdf(fig):
    """Export Matplotlib figure to PDF bytes"""
    try:
        buf = BytesIO()
        fig.savefig(buf, format='pdf', bbox_inches='tight', dpi=300)
        buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        st.error(f"Error exporting to PDF: {str(e)}")
        return None


def generate_analysis_report_pdf(df, file_name, numeric_cols):
    """Generate comprehensive PDF analysis report"""
    try:
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        elements = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#4F46E5'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#4F46E5'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        
        # Title
        elements.append(Paragraph("Data Analysis Report", title_style))
        elements.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                                 styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # File Information
        elements.append(Paragraph("File Information", heading_style))
        file_info_data = [
            ['Filename', file_name],
            ['Total Rows', str(len(df))],
            ['Total Columns', str(len(df.columns))],
            ['Missing Values', str(df.isnull().sum().sum())],
            ['Duplicate Rows', str(df.duplicated().sum())]
        ]
        file_info_table = Table(file_info_data, colWidths=[2*inch, 2*inch])
        file_info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(file_info_table)
        elements.append(Spacer(1, 20))
        
        # Column Details
        elements.append(Paragraph("Column Details", heading_style))
        col_info_data = [['Column Name', 'Data Type', 'Missing %', 'Unique Values']]
        for col in df.columns:
            missing_pct = round(df[col].isnull().sum() / len(df) * 100, 2)
            col_info_data.append([
                str(col),
                str(df[col].dtype),
                f"{missing_pct}%",
                str(df[col].nunique())
            ])
        
        col_info_table = Table(col_info_data, colWidths=[1.5*inch, 1.2*inch, 1*inch, 1.3*inch])
        col_info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
        ]))
        elements.append(col_info_table)
        elements.append(PageBreak())
        
        # Summary Statistics
        if numeric_cols:
            elements.append(Paragraph("Summary Statistics", heading_style))
            summary = df[numeric_cols].describe().round(2)
            summary_data = [[''] + list(summary.columns)]
            for idx in summary.index:
                summary_data.append([str(idx)] + 
                                   [str(summary.loc[idx, col]) for col in summary.columns])
            
            summary_table = Table(summary_data, 
                                 colWidths=[1*inch] * (len(numeric_cols) + 1))
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), 
                 [colors.white, colors.HexColor('#f9f9f9')])
            ]))
            elements.append(summary_table)
        
        doc.build(elements)
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
        
    except Exception as e:
        st.error(f"Error generating PDF report: {str(e)}")
        return None


# ============================================================================
# HISTORY MANAGEMENT - PERSISTENT STORAGE
# ============================================================================

HISTORY_FILE = Path.home() / ".data_analytics_app" / "history.json"

def ensure_history_dir():
    """Ensure history directory exists"""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_history():
    """Load analysis history from persistent storage"""
    ensure_history_dir()
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    """Save analysis history to persistent storage"""
    ensure_history_dir()
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def add_analysis_to_history(filename, df, file_type):
    """Add a new analysis record to history with deduplication"""
    history = load_history()
    
    # Create new record
    new_record = {
        'id': int(datetime.now().timestamp() * 1000),
        'filename': filename,
        'file_type': file_type,
        'timestamp': datetime.now().isoformat(),
        'rows': len(df),
        'columns': len(df.columns),
        'size_mb': round(df.memory_usage(deep=True).sum() / 1024 ** 2, 2),
        'numeric_cols': len(df.select_dtypes(include='number').columns),
        'categorical_cols': len(df.select_dtypes(include='object').columns),
    }
    
    # Remove duplicate if exists
    history = [h for h in history if h['filename'] != filename]
    
    # Add new record at beginning (most recent first)
    history.insert(0, new_record)
    
    # Keep only last 50 records
    history = history[:50]
    
    save_history(history)
    return new_record

def delete_from_history(record_id):
    """Delete a record from history by ID"""
    history = load_history()
    history = [h for h in history if h['id'] != record_id]
    save_history(history)

def clear_all_history():
    """Clear all history"""
    save_history([])

def add_to_history(file_name, analysis_history, df=None):
    """Add file to analysis history (legacy function)"""
    history_record = {
        'filename': file_name,
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'rows': len(df) if df is not None else 0,
        'columns': len(df.columns) if df is not None else 0
    }
    
    if not any(h['filename'] == file_name for h in analysis_history):
        analysis_history.append(history_record)
    
    return analysis_history
