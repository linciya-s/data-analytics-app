"""
Configuration settings for Data Analytics Application
"""

# Application Settings
APP_NAME = "Data Analytics Platform"
APP_ICON = "bar_chart"
APP_DESCRIPTION = "Transform your data into actionable insights with interactive visualizations and analysis"
APP_LAYOUT = "wide"
APP_SIDEBAR_INITIAL_STATE = "expanded"

# Color Palette (Professional)
COLORS = {
    "primary": "#4F46E5",
    "primary_dark": "#4F46E5",
    "primary_light": "#6366F1",
    "secondary": "#7C3AED",
    "success": "#10B981",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "info": "#3B82F6",
    "background": "#F8FAFC",
    "text_primary": "#1E293B",
    "text_secondary": "#64748B",
    "border": "#E2E8F0",
}

# Gradient
HEADER_GRADIENT = f"linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%)"

# File Upload Settings
SUPPORTED_FILE_TYPES = ["csv", "xlsx", "xls", "json", "pdf"]
MAX_FILE_SIZE_MB = 100

# Data Processing Settings
HISTOGRAM_BINS = 30
BAR_CHART_TOP_N = 15
PIE_CHART_TOP_N = 10
WORD_CLOUD_MIN_WORDS = 10
WORD_CLOUD_MAX_WORDS = 200
WORD_CLOUD_DEFAULT_WORDS = 100

# ML Model Settings
TEST_SIZE_MIN = 10
TEST_SIZE_MAX = 40
TEST_SIZE_DEFAULT = 20
CONFUSION_MATRIX_MODELS = ["Naive Bayes", "Logistic Regression", "Random Forest"]
RANDOM_FOREST_ESTIMATORS = 100

# Chart Settings
CHART_HEIGHT = 450
CHART_FONT_SIZE = 12
CHART_TITLE_SIZE = 16
CHART_TEMPLATE = "plotly_white"
HEATMAP_WIDTH = 10
HEATMAP_HEIGHT = 6

# Text Settings
HEADING_FONT = "Helvetica-Bold"
BODY_FONT = "Helvetica"

# Pages/Tabs
TABS = [
    "📊 Data Overview",
    "📈 Visualizations",
    "🔍 Data Quality",
    "⬇️ Download",
    "☁️ Word Cloud",
    "🤖 Classification",
    "📜 Analysis History"
]

# Messages
MESSAGES = {
    "no_file": "Please upload a file to get started",
    "file_uploaded": "File uploaded successfully",
    "error_loading": "Error loading file",
    "no_numeric_cols": "No numeric columns found",
    "no_categorical_cols": "No categorical columns found",
    "need_two_numeric": "Need at least 2 numeric columns",
    "pdf_extracted": "PDF text extracted and converted to table format",
    "no_missing_values": "No missing values found",
    "no_duplicates": "No duplicate rows found",
    "no_text_columns": "No text columns found for analysis",
}

# Export Settings
PDF_PAGE_SIZE = "letter"
PDF_MARGINS = 72
CSV_INDEX = False

# History Settings
HISTORY_MAX_RECORDS = 50
HISTORY_SHOW_RECENT = 20
HISTORY_ENABLE_PERSISTENT = True
CSV_ENCODING = "utf-8"
