"""
Professional Data Analytics Platform
Main Application Entry Point
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import json
import PyPDF2
from io import BytesIO
import time
from datetime import datetime
from pathlib import Path

# Import configuration
import config
from utils.filehandler import (
    read_csv_file, read_excel_file, read_json_file, read_pdf_file,
    get_column_types, get_data_summary, get_column_info,
    export_matplotlib_to_pdf, generate_analysis_report_pdf,
    load_history, save_history, add_analysis_to_history, delete_from_history, 
    clear_all_history
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title=config.APP_NAME,
    page_icon=config.APP_ICON,
    layout=config.APP_LAYOUT,
    initial_sidebar_state=config.APP_SIDEBAR_INITIAL_STATE
)

# ============================================================================
# CUSTOM STYLING - PROFESSIONAL CSS
# ============================================================================

professional_css = """
<style>
    /* Main Background */
    body {
        background-color: #F8FAFC;
        color: #1E293B;
    }
    
    /* Header Section */
    .header-container {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .header-container h1 {
        font-size: 2.25rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .header-container p {
        font-size: 1rem;
        opacity: 0.95;
        font-weight: 400;
        margin: 0;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #F1F5F9;
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 0.95rem;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: 2px solid transparent;
        transition: all 250ms ease-in-out;
        white-space: nowrap;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #4F46E5;
        color: white;
        border-color: #4F46E5;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="false"] {
        background-color: white;
        color: #1E293B;
        border-color: #E2E8F0;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="false"]:hover {
        background-color: #F1F5F9;
        border-color: #6366F1;
    }
    
    /* Sidebar */
    .stSidebar {
        background-color: white;
        border-right: 1px solid #E2E8F0;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #4F46E5;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: none;
        transition: all 150ms ease-in-out;
        font-size: 0.95rem;
        letter-spacing: 0.25px;
    }
    
    .stButton > button:hover {
        background-color: #6366F1;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    /* Data Frames */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Alerts */
    .stSuccess {
        background-color: #ECFDF5;
        border-left: 4px solid #10B981;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stError {
        background-color: #FEF2F2;
        border-left: 4px solid #EF4444;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stWarning {
        background-color: #FFFBEB;
        border-left: 4px solid #F59E0B;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stInfo {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Headings */
    h3 {
        color: #1E293B;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #4F46E5;
        letter-spacing: -0.25px;
    }
    
    /* Dividers */
    .stMarkdown hr {
        margin: 2rem 0;
        border: none;
        border-top: 2px solid #E2E8F0;
    }
</style>
"""

st.markdown(professional_css, unsafe_allow_html=True)

# ============================================================================
# HEADER SECTION
# ============================================================================

st.markdown(f"""
    <div class="header-container">
        <h1>{config.APP_NAME}</h1>
        <p>{config.APP_DESCRIPTION}</p>
    </div>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = load_history()

if 'current_file' not in st.session_state:
    st.session_state.current_file = None

if 'selected_history_id' not in st.session_state:
    st.session_state.selected_history_id = None

# ============================================================================
# SIDEBAR - HISTORY & SETTINGS
# ============================================================================

with st.sidebar:
    st.markdown("""
        <div style='color: #4F46E5; font-size: 1.25rem; font-weight: 700; margin-bottom: 1rem;'>
            ⚙️ Settings
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📜 Analysis History")
    
    if st.session_state.analysis_history:
        st.write(f"**Total Analyses:** {len(st.session_state.analysis_history)}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 View All", use_container_width=True):
                st.session_state.show_all_history = True
        with col2:
            if st.button("🗑️ Clear All", use_container_width=True):
                clear_all_history()
                st.session_state.analysis_history = []
                st.success("History cleared!")
                st.rerun()
        
        st.markdown("---")
        st.write("**Recently Analyzed:**")
        
        # Show last 3 recent files
        for record in st.session_state.analysis_history[:3]:
            timestamp = datetime.fromisoformat(record['timestamp']).strftime("%m/%d %H:%M")
            btn_label = f"📄 {record['filename'][:25]}"
            if st.button(btn_label, use_container_width=True, help=f"{record['rows']} rows • {record['columns']} cols"):
                st.session_state.selected_history_id = record['id']
    else:
        st.info("💡 No analysis history yet. Upload a file to begin!")

st.markdown("---")

# File uploader
uploaded_file = st.file_uploader(
    "Upload your CSV, Excel, JSON, or PDF file here",
    type=config.SUPPORTED_FILE_TYPES
)

# ============================================================================
# MAIN APPLICATION LOGIC
# ============================================================================

if uploaded_file is not None:
    file_name = uploaded_file.name
    file_extension = file_name.split('.')[-1].lower()
    
    try:
        # Load data based on file type
        if file_extension == 'csv':
            df = read_csv_file(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            df = read_excel_file(uploaded_file)
        elif file_extension == 'json':
            df = read_json_file(uploaded_file)
        elif file_extension == 'pdf':
            df = read_pdf_file(uploaded_file)
        else:
            st.error("File type not supported")
            st.stop()
        
        st.success(f"File loaded successfully: {file_name}")
        
        # Add to persistent history
        add_analysis_to_history(file_name, df, file_extension)
        st.session_state.analysis_history = load_history()
        
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        st.stop()
    
    # Get column types
    numeric_cols, categorical_cols = get_column_types(df)
    
    # ========================================================================
    # TABS INTERFACE
    # ========================================================================
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(config.TABS)
    
    # ---- TAB 1: DATA OVERVIEW ----
    with tab1:
        st.header("Data Overview")
        st.markdown("---")
        
        st.subheader("Raw Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        st.subheader("Dataset Overview")
        
        summary = get_data_summary(df)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Rows", f"{summary['rows']:,}")
        with col2:
            st.metric("Total Columns", f"{summary['columns']}")
        with col3:
            st.metric("Missing Values", f"{summary['missing_values']:,}")
        with col4:
            st.metric("Duplicate Rows", f"{summary['duplicates']:,}")
        
        st.markdown("---")
        st.subheader("Column Information")
        
        col_info = get_column_info(df)
        st.dataframe(col_info, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Summary Statistics")
        st.dataframe(df.describe(include='all').astype(str), use_container_width=True)
    
    # ---- TAB 2: VISUALIZATIONS ----
    with tab2:
        st.header("📊 Advanced Visualizations")
        st.markdown("Explore your data with multiple interactive visualization types")
        st.markdown("---")
        
        # Create sub-tabs for different visualization types
        viz_tab1, viz_tab2, viz_tab3, viz_tab4, viz_tab5, viz_tab6 = st.tabs([
            "📊 Histogram", 
            "📈 Bar Chart", 
            "🔥 Heatmap",
            "📍 Scatter Plot",
            "📦 Box Plot",
            "🥧 Pie Chart"
        ])
        
        # ---- VIZ TAB 1: HISTOGRAM ----
        with viz_tab1:
            st.subheader("📊 Histogram - Distribution Analysis")
            st.write("Visualize the distribution of numeric columns with histograms")
            st.markdown("---")
            
            if numeric_cols:
                selected_hist = st.selectbox("Select column for Histogram", numeric_cols, key="hist_select")
                nbins = st.slider("Number of Bins", 10, 50, 30, key="hist_bins")
                
                fig = px.histogram(df, x=selected_hist, nbins=nbins,
                                 title=f"📊 Distribution of {selected_hist}",
                                 color_discrete_sequence=["#4F46E5"],
                                 labels={selected_hist: selected_hist, 'count': 'Frequency'})
                fig.update_layout(
                    template="plotly_white",
                    hovermode="x unified",
                    height=500,
                    font=dict(family="Arial, sans-serif", size=12),
                    title_font_size=18,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0.02)',
                    xaxis_title=selected_hist,
                    yaxis_title="Frequency"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Download button
                col1, col2, col3 = st.columns([2, 1, 1])
                with col3:
                    try:
                        img_bytes = fig.to_image(format="png")
                        st.download_button(
                            label="📥 Download PNG",
                            data=img_bytes,
                            file_name=f"histogram_{selected_hist}.png",
                            mime="image/png",
                            key=f"hist_png_{selected_hist}"
                        )
                    except:
                        pass
            else:
                st.info("No numeric columns found for histogram. Please upload a file with numeric columns.")
        
        # ---- VIZ TAB 2: BAR CHART ----
        with viz_tab2:
            st.subheader("📈 Bar Chart - Category Analysis")
            st.write("Visualize the distribution of categorical columns with bar charts")
            st.markdown("---")
            
            if categorical_cols:
                selected_bar = st.selectbox("Select column for Bar Chart", categorical_cols, key="bar_select")
                top_n = st.slider("Show Top N Categories", 5, 20, 15, key="bar_top_n")
                
                top_values = df[selected_bar].value_counts().head(top_n).reset_index()
                top_values.columns = [selected_bar, 'Count']
                
                fig2 = px.bar(top_values, x=selected_bar, y='Count',
                             title=f"📈 Top {top_n} Categories in {selected_bar}",
                             color='Count',
                             color_continuous_scale='Viridis',
                             labels={'Count': 'Count', selected_bar: selected_bar})
                fig2.update_layout(
                    template="plotly_white",
                    hovermode="x unified",
                    height=500,
                    font=dict(family="Arial, sans-serif", size=12),
                    title_font_size=18,
                    xaxis_tickangle=-45,
                    plot_bgcolor='rgba(0,0,0,0.02)',
                    showlegend=False
                )
                st.plotly_chart(fig2, use_container_width=True)
                
                # Download button
                col1, col2, col3 = st.columns([2, 1, 1])
                with col3:
                    try:
                        img_bytes = fig2.to_image(format="png")
                        st.download_button(
                            label="📥 Download PNG",
                            data=img_bytes,
                            file_name=f"barchart_{selected_bar}.png",
                            mime="image/png",
                            key=f"bar_png_{selected_bar}"
                        )
                    except:
                        pass
            else:
                st.info("No categorical columns found for bar chart. Please upload a file with categorical columns.")
        
        # ---- VIZ TAB 3: CORRELATION HEATMAP ----
        with viz_tab3:
            st.subheader("🔥 Correlation Heatmap - Feature Relationships")
            st.write("Analyze correlations between numeric features in your dataset")
            st.markdown("---")
            
            if len(numeric_cols) >= 2:
                fig7, ax = plt.subplots(figsize=(12, 8))
                correlation_matrix = df[numeric_cols].corr()
                sns.heatmap(correlation_matrix, annot=True, fmt=".2f", 
                           cmap="coolwarm", ax=ax, cbar_kws={"label": "Correlation"},
                           linewidths=1, linecolor='white', square=True)
                ax.set_title("🔥 Feature Correlation Matrix", fontsize=16, fontweight='bold', pad=20)
                plt.tight_layout()
                st.pyplot(fig7, use_container_width=True)
                
                col1, col2, col3 = st.columns([2, 1, 1])
                with col3:
                    pdf_data = export_matplotlib_to_pdf(fig7)
                    if pdf_data:
                        st.download_button(
                            label="📥 Download PDF",
                            data=pdf_data,
                            file_name="correlation_heatmap.pdf",
                            mime="application/pdf",
                            key="heatmap_pdf"
                        )
                plt.close(fig7)
            else:
                st.info("Need at least 2 numeric columns for correlation heatmap")
        
        # ---- VIZ TAB 4: SCATTER PLOT ----
        with viz_tab4:
            st.subheader("📍 Scatter Plot - Relationship Analysis")
            st.write("Explore relationships between two numeric variables")
            st.markdown("---")
            
            if len(numeric_cols) >= 2:
                col1, col2 = st.columns(2)
                with col1:
                    x_scatter = st.selectbox("X-axis", numeric_cols, key="scatter_x")
                with col2:
                    y_scatter = st.selectbox("Y-axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0, key="scatter_y")
                
                # Optional: Color by categorical variable
                color_by = None
                if categorical_cols:
                    color_option = st.checkbox("Color by Category", key="scatter_color")
                    if color_option:
                        color_by = st.selectbox("Select categorical column", categorical_cols, key="scatter_color_col")
                
                # Build scatter plot with optional trendline
                scatter_params = {
                    "x": x_scatter,
                    "y": y_scatter,
                    "title": f"📍 Scatter Plot: {x_scatter} vs {y_scatter}"
                }
                
                if color_by:
                    scatter_params["color"] = color_by
                
                if st.checkbox("Show Trendline", key="scatter_trend"):
                    scatter_params["trendline"] = "ols"
                
                fig_scatter = px.scatter(df, **scatter_params, opacity=0.7)
                fig_scatter.update_layout(
                    template="plotly_white",
                    height=500,
                    font=dict(family="Arial, sans-serif", size=12),
                    title_font_size=18,
                    hovermode="closest",
                    xaxis_title=x_scatter,
                    yaxis_title=y_scatter,
                    plot_bgcolor='rgba(0,0,0,0.02)'
                )
                fig_scatter.update_traces(marker=dict(size=8, opacity=0.7))
                st.plotly_chart(fig_scatter, use_container_width=True)
                
                col1, col2, col3 = st.columns([2, 1, 1])
                with col3:
                    try:
                        img_bytes = fig_scatter.to_image(format="png")
                        st.download_button(
                            label="📥 Download PNG",
                            data=img_bytes,
                            file_name=f"scatter_{x_scatter}_vs_{y_scatter}.png",
                            mime="image/png",
                            key="scatter_png"
                        )
                    except:
                        pass
            else:
                st.info("Need at least 2 numeric columns for scatter plot")
        
        # ---- VIZ TAB 5: BOX PLOT ----
        with viz_tab5:
            st.subheader("📦 Box Plot - Statistical Distribution")
            st.write("Visualize quartiles, medians, and outliers in your numeric data")
            st.markdown("---")
            
            if numeric_cols:
                # Option 1: Single column box plot
                plot_option = st.radio("Box Plot Type", ["Single Column", "Compare by Category"], key="box_type")
                
                if plot_option == "Single Column":
                    selected_box = st.selectbox("Select numeric column", numeric_cols, key="box_col")
                    
                    fig_box = px.box(
                        df,
                        y=selected_box,
                        title=f"📦 Box Plot: {selected_box}",
                        points="outliers"
                    )
                    fig_box.update_layout(
                        template="plotly_white",
                        height=500,
                        font=dict(family="Arial, sans-serif", size=12),
                        title_font_size=18,
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0.02)'
                    )
                else:
                    if categorical_cols:
                        selected_box = st.selectbox("Select numeric column", numeric_cols, key="box_col_2")
                        category_box = st.selectbox("Group by category", categorical_cols, key="box_cat")
                        
                        fig_box = px.box(
                            df,
                            x=category_box,
                            y=selected_box,
                            title=f"📦 Box Plot: {selected_box} by {category_box}",
                            points="outliers",
                            color=category_box
                        )
                        fig_box.update_layout(
                            template="plotly_white",
                            height=500,
                            font=dict(family="Arial, sans-serif", size=12),
                            title_font_size=18,
                            xaxis_tickangle=-45,
                            plot_bgcolor='rgba(0,0,0,0.02)'
                        )
                    else:
                        st.warning("No categorical columns available for grouping")
                        st.stop()
                
                st.plotly_chart(fig_box, use_container_width=True)
                
                col1, col2, col3 = st.columns([2, 1, 1])
                with col3:
                    try:
                        img_bytes = fig_box.to_image(format="png")
                        st.download_button(
                            label="📥 Download PNG",
                            data=img_bytes,
                            file_name="boxplot.png",
                            mime="image/png",
                            key="box_png"
                        )
                    except:
                        pass
            else:
                st.info("No numeric columns found for box plot")
        
        # ---- VIZ TAB 6: PIE CHART ----
        with viz_tab6:
            st.subheader("🥧 Pie Chart - Composition Analysis")
            st.write("Visualize the composition and proportions of categorical data")
            st.markdown("---")
            
            if categorical_cols:
                selected_pie = st.selectbox("Select column for Pie Chart", categorical_cols, key="pie_select")
                top_n_pie = st.slider("Show Top N Categories", 3, 15, 8, key="pie_top_n")
                
                col_donut, col_color = st.columns(2)
                with col_donut:
                    show_donut = st.checkbox("Show as Donut", key="pie_donut")
                with col_color:
                    pastel_colors = st.checkbox("Pastel Colors", key="pie_pastel")
                
                pie_data = df[selected_pie].value_counts().head(top_n_pie)
                
                fig_pie = px.pie(
                    values=pie_data.values,
                    names=pie_data.index,
                    title=f"🥧 Composition of {selected_pie}",
                    hole=0.4 if show_donut else 0,
                    color_discrete_sequence=px.colors.qualitative.Set3 if pastel_colors else px.colors.qualitative.Plotly
                )
                fig_pie.update_layout(
                    template="plotly_white",
                    height=500,
                    font=dict(family="Arial, sans-serif", size=12),
                    title_font_size=18,
                    hovermode="closest"
                )
                
                # Add percentage labels
                fig_pie.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    hoverinfo='label+value+percent'
                )
                
                st.plotly_chart(fig_pie, use_container_width=True)
                
                # Statistics
                st.subheader("Category Statistics")
                stats_df = pd.DataFrame({
                    'Category': pie_data.index,
                    'Count': pie_data.values,
                    'Percentage': (pie_data.values / pie_data.sum() * 100).round(2)
                })
                st.dataframe(stats_df, use_container_width=True, hide_index=True)
                
                col1, col2, col3 = st.columns([2, 1, 1])
                with col3:
                    try:
                        img_bytes = fig_pie.to_image(format="png")
                        st.download_button(
                            label="📥 Download PNG",
                            data=img_bytes,
                            file_name=f"piechart_{selected_pie}.png",
                            mime="image/png",
                            key="pie_png"
                        )
                    except:
                        pass
            else:
                st.info("No categorical columns found for pie chart. Please upload a file with categorical data.")
        
        # ---- BONUS: BUBBLE CHART ----
        st.markdown("---")
        st.subheader("🫧 Bonus: Bubble Chart - Multi-dimensional Analysis")
        st.write("Visualize up to 4 dimensions in a single chart")
        
        if len(numeric_cols) >= 3:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                x_bubble = st.selectbox("X-axis (numeric)", numeric_cols, key="bubble_x")
            with col2:
                y_bubble = st.selectbox("Y-axis (numeric)", numeric_cols, index=1 if len(numeric_cols) > 1 else 0, key="bubble_y")
            with col3:
                size_bubble = st.selectbox("Bubble Size (numeric)", numeric_cols, index=2 if len(numeric_cols) > 2 else 0, key="bubble_size")
            with col4:
                color_bubble = None
                if categorical_cols:
                    color_bubble = st.selectbox("Color by (category)", ['None'] + categorical_cols, key="bubble_color")
                    if color_bubble == 'None':
                        color_bubble = None
            
            # Build bubble chart with optional trendline
            bubble_params = {
                "x": x_bubble,
                "y": y_bubble,
                "size": size_bubble,
                "title": f"🫧 Bubble Chart: {x_bubble} vs {y_bubble} (size: {size_bubble})"
            }
            
            if color_bubble:
                bubble_params["color"] = color_bubble
            
            if st.checkbox("Show Trendline", key="bubble_trend"):
                bubble_params["trendline"] = "ols"
            
            fig_bubble = px.scatter(df, **bubble_params)
            fig_bubble.update_layout(
                template="plotly_white",
                height=500,
                font=dict(family="Arial, sans-serif", size=12),
                title_font_size=18,
                hovermode="closest",
                plot_bgcolor='rgba(0,0,0,0.02)',
                xaxis_title=x_bubble,
                yaxis_title=y_bubble
            )
            fig_bubble.update_traces(marker=dict(sizemode='diameter', sizeref=2.*max(df[size_bubble])/(50**2), sizemin=4, opacity=0.6))
            st.plotly_chart(fig_bubble, use_container_width=True)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col3:
                try:
                    img_bytes = fig_bubble.to_image(format="png")
                    st.download_button(
                        label="📥 Download PNG",
                        data=img_bytes,
                        file_name=f"bubble_{x_bubble}_vs_{y_bubble}.png",
                        mime="image/png",
                        key="bubble_png"
                    )
                except:
                    pass
        else:
            st.info("Need at least 3 numeric columns for bubble chart")
    
    # ---- TAB 3: DATA QUALITY ----
    with tab3:
        st.header("Data Quality Report")
        
        st.subheader("Missing Values Analysis")
        missing = df.isnull().sum().reset_index()
        missing.columns = ["Column", "Missing Count"]
        missing["Missing %"] = (missing["Missing Count"] / len(df) * 100).round(2)
        missing = missing[missing["Missing Count"] > 0]
        
        if missing.empty:
            st.success("No missing values detected in the dataset")
        else:
            st.dataframe(missing, use_container_width=True)
            fig_missing = px.bar(missing, x="Column", y="Missing %",
                               title="Missing Values by Column",
                               color_discrete_sequence=["#EF4444"],
                               labels={"Column": "Column", "Missing %": "Missing %"})
            fig_missing.update_layout(
                template="plotly_white",
                height=400,
                font=dict(family="Arial, sans-serif", size=12),
                title_font_size=16,
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_missing, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Duplicate Rows Analysis")
        
        dup_count = df.duplicated().sum()
        if dup_count == 0:
            st.success("No duplicate rows found")
        else:
            st.warning(f"Found {dup_count} duplicate rows")
            st.dataframe(df[df.duplicated(keep=False)], use_container_width=True)
        
        st.markdown("---")
        
        if numeric_cols:
            st.subheader("Outlier Detection (IQR Method)")
            outlier_summary = []
            
            for col in numeric_cols:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
                
                outlier_summary.append({
                    "Column": col,
                    "Outlier Count": len(outliers),
                    "Outlier %": round(len(outliers) / len(df) * 100, 2)
                })
            
            st.dataframe(pd.DataFrame(outlier_summary), use_container_width=True)
    
    # ---- TAB 4: DOWNLOAD ----
    with tab4:
        st.header("Download Data & Reports")
        
        st.subheader("Clean Data Export")
        cleaned_df = df.drop_duplicates()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Original Rows", f"{len(df):,}")
        with col2:
            st.metric("After Cleanup", f"{len(cleaned_df):,}")
        
        st.info(f"Removed {len(df) - len(cleaned_df)} duplicate rows")
        
        csv_data = cleaned_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Cleaned Data (CSV)",
            data=csv_data,
            file_name=f"cleaned_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        st.subheader("Analysis Report")
        st.write("Generate a comprehensive PDF report of your data analysis")
        
        if st.button("Generate PDF Report", use_container_width=True):
            with st.spinner("Generating PDF report..."):
                pdf_data = generate_analysis_report_pdf(df, file_name, numeric_cols)
                if pdf_data:
                    st.download_button(
                        label="Download Analysis Report (PDF)",
                        data=pdf_data,
                        file_name=f"Analysis_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
                    st.success("PDF report generated successfully")
    
    # ---- TAB 5: WORD CLOUD ----
    with tab5:
        st.header("Word Cloud Generator")
        st.write("Generate word clouds from text columns in your dataset")
        
        if categorical_cols:
            selected_text_col = st.selectbox("Select text column", categorical_cols)
            
            text_data = ' '.join(df[selected_text_col].dropna().astype(str))
            
            col_a, col_b = st.columns(2)
            with col_a:
                max_words = st.slider("Max words", 10, 200, 100)
                bg_color = st.selectbox("Background", ["white", "black", "grey"])
            with col_b:
                colormap = st.selectbox("Color scheme", 
                                       ["viridis", "plasma", "Blues", "Reds", "Greens"])
            
            if st.button("Generate Word Cloud", use_container_width=True):
                if text_data.strip():
                    from wordcloud import WordCloud
                    from collections import Counter
                    
                    wc = WordCloud(width=800, height=400, 
                                  background_color=bg_color,
                                  colormap=colormap, 
                                  max_words=max_words).generate(text_data)
                    
                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.imshow(wc, interpolation='bilinear')
                    ax.axis('off')
                    ax.set_title(f"Word Cloud - {selected_text_col}", 
                               fontsize=16, fontweight='bold')
                    st.pyplot(fig, use_container_width=True)
                    
                    st.success("Word cloud generated successfully")
                    
                    st.subheader("Top 20 Most Frequent Words")
                    word_list = text_data.split()
                    common_words = Counter(word_list).most_common(20)
                    word_freq_df = pd.DataFrame(common_words, columns=['Word', 'Count'])
                    
                    fig2 = px.bar(word_freq_df, x='Count', y='Word', orientation='h',
                                 title="Top 20 Words",
                                 color='Count', color_continuous_scale='Blues')
                    fig2.update_layout(
                        template="plotly_white",
                        height=500,
                        font=dict(family="Arial, sans-serif", size=11),
                        title_font_size=16
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.warning("No text found in selected column")
        else:
            st.warning("No text columns available for word cloud")
    
    # ---- TAB 6: CLASSIFICATION MODELS ----
    with tab6:
        st.header("Classification Models")
        st.write("Train machine learning models on your data")
        
        if len(categorical_cols) >= 2:
            st.subheader("Model Configuration")
            
            col1, col2 = st.columns(2)
            with col1:
                target_col = st.selectbox("Target Column", categorical_cols)
            with col2:
                text_col_options = [c for c in categorical_cols if c != target_col]
                if text_col_options:
                    text_col = st.selectbox("Feature Column", text_col_options)
                else:
                    text_col = None
                    st.warning("Need at least 2 categorical columns")
            
            model_choice = st.selectbox("Select Model", 
                                       ["Naive Bayes", "Logistic Regression", "Random Forest"])
            test_size = st.slider("Test Data Size (%)", 10, 40, 20)
            
            if st.button("Train Model", use_container_width=True):
                if text_col is None:
                    st.error("Please select a valid feature column")
                else:
                    with st.spinner("Training model..."):
                        from sklearn.feature_extraction.text import CountVectorizer
                        from sklearn.model_selection import train_test_split
                        from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
                        from sklearn.preprocessing import LabelEncoder, MinMaxScaler
                        import numpy as np
                        
                        # Prepare data
                        model_df = df[[text_col, target_col]].dropna().copy()
                        model_df[text_col] = model_df[text_col].astype(str)
                        model_df[target_col] = model_df[target_col].astype(str)
                        
                        cv = CountVectorizer(max_features=500)
                        X = cv.fit_transform(model_df[text_col]).toarray()
                        le = LabelEncoder()
                        y = le.fit_transform(model_df[target_col])
                        
                        X_train, X_test, y_train, y_test = train_test_split(
                            X, y, test_size=test_size/100, random_state=42
                        )
                        
                        # Train model
                        if model_choice == "Naive Bayes":
                            from sklearn.naive_bayes import MultinomialNB
                            model = MultinomialNB()
                        elif model_choice == "Logistic Regression":
                            from sklearn.linear_model import LogisticRegression
                            model = LogisticRegression(max_iter=1000)
                        else:
                            from sklearn.ensemble import RandomForestClassifier
                            model = RandomForestClassifier(n_estimators=100, random_state=42)
                        
                        model.fit(X_train, y_train)
                        y_pred = model.predict(X_test)
                        accuracy = accuracy_score(y_test, y_pred)
                        
                        # Display results
                        st.markdown("---")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Accuracy Score", f"{accuracy * 100:.2f}%")
                        col2.metric("Test Samples", len(y_test))
                        col3.metric("Classes", len(le.classes_))
                        
                        st.markdown("---")
                        st.subheader("Confusion Matrix")
                        
                        cm = confusion_matrix(y_test, y_pred)
                        fig, ax = plt.subplots(figsize=(8, 6))
                        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                                   xticklabels=le.classes_,
                                   yticklabels=le.classes_, ax=ax,
                                   cbar_kws={"label": "Count"})
                        ax.set_title(f"Confusion Matrix - {model_choice}",
                                    fontsize=14, fontweight='bold')
                        ax.set_xlabel("Predicted", fontsize=12)
                        ax.set_ylabel("Actual", fontsize=12)
                        plt.tight_layout()
                        st.pyplot(fig, use_container_width=True)
                        
                        st.markdown("---")
                        st.subheader("Classification Report")
                        report = classification_report(y_test, y_pred, 
                                                      output_dict=True,
                                                      zero_division=0)
                        report_df = pd.DataFrame(report).transpose().round(3)
                        st.dataframe(report_df, use_container_width=True)
        else:
            st.warning("Need at least 2 categorical columns for classification")
    
    # ---- TAB 7: ANALYSIS HISTORY ----
    with tab7:
        st.header("📜 Analysis History")
        st.write("View and manage your analysis history")
        st.markdown("---")
        
        if st.session_state.analysis_history:
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Total Analyses", len(st.session_state.analysis_history))
            with col2:
                total_rows = sum(h['rows'] for h in st.session_state.analysis_history)
                st.metric("📈 Total Rows", f"{total_rows:,}")
            with col3:
                total_cols = sum(h['columns'] for h in st.session_state.analysis_history)
                st.metric("📋 Total Columns", total_cols)
            with col4:
                total_size = sum(h['size_mb'] for h in st.session_state.analysis_history)
                st.metric("💾 Total Size", f"{total_size:.2f} MB")
            
            st.markdown("---")
            
            # View options
            view_mode = st.radio("View Mode", ["📱 Card View", "📊 List View"], horizontal=True)
            
            if view_mode == "📱 Card View":
                # Card View
                st.write("### Recent Analyses")
                
                # Create columns for cards
                cols = st.columns(3)
                
                for idx, record in enumerate(st.session_state.analysis_history):
                    col = cols[idx % 3]
                    
                    with col:
                        with st.container(border=True):
                            # Header
                            st.markdown(f"**📄 {record['filename']}**")
                            
                            # Timestamp
                            timestamp = datetime.fromisoformat(record['timestamp']).strftime("%B %d, %Y • %H:%M")
                            st.markdown(f"<small style='color: #64748B;'>{timestamp}</small>", unsafe_allow_html=True)
                            
                            st.divider()
                            
                            # Stats
                            stat_col1, stat_col2 = st.columns(2)
                            with stat_col1:
                                st.metric("Rows", f"{record['rows']:,}", label_visibility="collapsed")
                                st.metric("Numeric", record['numeric_cols'], label_visibility="collapsed")
                            with stat_col2:
                                st.metric("Columns", record['columns'], label_visibility="collapsed")
                                st.metric("Categorical", record['categorical_cols'], label_visibility="collapsed")
                            
                            st.markdown(f"<small style='color: #64748B;'>Size: {record['size_mb']:.2f} MB</small>", unsafe_allow_html=True)
                            
                            st.divider()
                            
                            # Actions
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button("📂 View", key=f"view_{record['id']}", use_container_width=True):
                                    st.info(f"Would load: {record['filename']}")
                            with col_b:
                                if st.button("🗑️ Delete", key=f"del_{record['id']}", use_container_width=True):
                                    delete_from_history(record['id'])
                                    st.session_state.analysis_history = load_history()
                                    st.success("Removed from history!")
                                    st.rerun()
            
            else:
                # List View / Table View
                st.write("### All Analyses")
                
                history_table_data = []
                for record in st.session_state.analysis_history:
                    timestamp = datetime.fromisoformat(record['timestamp']).strftime("%Y-%m-%d %H:%M")
                    history_table_data.append({
                        "📄 File": record['filename'],
                        "Date": timestamp,
                        "Rows": f"{record['rows']:,}",
                        "Columns": f"{record['columns']}",
                        "Size (MB)": f"{record['size_mb']:.2f}",
                        "Numeric": record['numeric_cols'],
                        "Categorical": record['categorical_cols']
                    })
                
                history_df = pd.DataFrame(history_table_data)
                st.dataframe(history_df, use_container_width=True, hide_index=True)
                
                st.markdown("---")
                st.write("**Delete from History:**")
                
                file_to_delete = st.selectbox(
                    "Select a file to remove",
                    options=[h['filename'] for h in st.session_state.analysis_history],
                    label_visibility="collapsed"
                )
                
                if st.button("🗑️ Delete Selected File", use_container_width=True):
                    record_id = next(h['id'] for h in st.session_state.analysis_history if h['filename'] == file_to_delete)
                    delete_from_history(record_id)
                    st.session_state.analysis_history = load_history()
                    st.success(f"Deleted: {file_to_delete}")
                    st.rerun()
            
            # Bulk Actions
            st.markdown("---")
            st.subheader("🔧 Bulk Actions")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📥 Export History as JSON", use_container_width=True):
                    history_json = json.dumps(st.session_state.analysis_history, indent=2)
                    st.download_button(
                        label="Download History JSON",
                        data=history_json,
                        file_name=f"analysis_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            
            with col2:
                if st.button("🧹 Clear All History", use_container_width=True):
                    if st.checkbox("I understand this will delete all history"):
                        clear_all_history()
                        st.session_state.analysis_history = []
                        st.success("All history cleared!")
                        st.rerun()
        
        else:
            # Empty state
            st.markdown("""
                <div style='text-align: center; padding: 2rem; background: #F1F5F9; border-radius: 12px;'>
                    <h3 style='color: #64748B; margin-bottom: 1rem;'>No History Yet</h3>
                    <p style='color: #64748B; font-size: 1rem;'>
                        Your analysis history will appear here once you upload and analyze files.
                    </p>
                </div>
            """, unsafe_allow_html=True)

else:
    st.markdown("""
        <div style='text-align: center; padding: 3rem 1rem;'>
            <h3 style='color: #4F46E5; font-size: 1.5rem; margin-bottom: 1rem;'>
                Get Started
            </h3>
            <p style='font-size: 1.1rem; color: #64748B; max-width: 500px; margin: 0 auto;'>
                Upload a CSV, Excel, JSON, or PDF file to begin analyzing your data
            </p>
        </div>
    """, unsafe_allow_html=True)
