import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import json

st.set_page_config(page_title="Data Analytics App", page_icon="📊", layout="wide")
st.title("📊 Data Analytics App")
st.write("Upload any **CSV, Excel or JSON** file to instantly analyze and visualize your data!")

uploaded_file = st.file_uploader(
    "📂 Upload your CSV, Excel or JSON file here",
    type=["csv", "xlsx", "xls", "json"]
)

if uploaded_file is not None:

    file_name = uploaded_file.name
    file_extension = file_name.split('.')[-1].lower()

    try:
        if file_extension == 'csv':
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding='latin1')
                except UnicodeDecodeError:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding='cp1252')

        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)

        elif file_extension == 'json':
            try:
                uploaded_file.seek(0)
                raw = json.load(uploaded_file)
                if isinstance(raw, list):
                    df = pd.json_normalize(raw)
                elif isinstance(raw, dict):
                    df = pd.json_normalize([raw])
                else:
                    st.error("❌ Unsupported JSON structure!")
                    st.stop()
            except Exception as je:
                st.error(f"❌ Error reading JSON: {je}")
                st.stop()

        else:
            st.error("❌ Unsupported file type!")
            st.stop()

        st.success(f"✅ {file_name} uploaded successfully!")

    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
        st.stop()

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📁 Data Overview",
        "📊 Visualizations",
        "🧹 Data Quality",
        "⬇️ Download",
        "☁️ Word Cloud",
        "🔢 Confusion Matrix"
    ])

    with tab1:
        st.subheader("📁 Raw Data Preview")
        st.dataframe(df.head(10))
        st.subheader("📋 Dataset Overview")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", df.isnull().sum().sum())
        col4.metric("Duplicate Rows", df.duplicated().sum())
        st.subheader("🔍 Column Details")
        col_info = pd.DataFrame({
            "Column Name": df.columns.astype(str),
            "Data Type": df.dtypes.astype(str).values,
            "Missing Values": df.isnull().sum().values,
            "Missing %": (df.isnull().sum().values / len(df) * 100).round(2),
            "Unique Values": df.nunique().values
        })
        st.dataframe(col_info)
        st.subheader("📈 Summary Statistics")
        st.dataframe(df.describe(include='all').astype(str))

    with tab2:
        st.header("📊 Visualizations")
        if numeric_cols:
            st.subheader("📉 Histogram")
            selected_hist = st.selectbox("Select column for Histogram", numeric_cols)
            fig = px.histogram(df, x=selected_hist, nbins=30,
                               title=f"Distribution of {selected_hist}",
                               color_discrete_sequence=["#636EFA"])
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("No numeric columns found for Histogram.")
        st.markdown("---")
        if categorical_cols:
            st.subheader("📊 Bar Chart")
            selected_bar = st.selectbox("Select column for Bar Chart", categorical_cols)
            top_values = df[selected_bar].value_counts().head(15).reset_index()
            top_values.columns = [selected_bar, 'Count']
            fig2 = px.bar(top_values, x=selected_bar, y='Count',
                          title=f"Top Categories in {selected_bar}",
                          color_discrete_sequence=["#EF553B"])
            st.plotly_chart(fig2, width='stretch')
        else:
            st.info("No categorical columns found for Bar Chart.")
        st.markdown("---")
        if categorical_cols:
            st.subheader("🥧 Pie Chart")
            selected_pie = st.selectbox("Select column for Pie Chart", categorical_cols)
            pie_data = df[selected_pie].value_counts().head(10).reset_index()
            pie_data.columns = [selected_pie, 'Count']
            fig3 = px.pie(pie_data, names=selected_pie, values='Count',
                          title=f"Proportion of {selected_pie}")
            st.plotly_chart(fig3, width='stretch')
        else:
            st.info("No categorical columns found for Pie Chart.")
        st.markdown("---")
        if len(numeric_cols) >= 2:
            st.subheader("🔵 Scatter Plot")
            x_axis = st.selectbox("Select X axis", numeric_cols, index=0)
            y_axis = st.selectbox("Select Y axis", numeric_cols, index=1)
            fig4 = px.scatter(df, x=x_axis, y=y_axis,
                              title=f"{x_axis} vs {y_axis}",
                              color_discrete_sequence=["#00CC96"])
            st.plotly_chart(fig4, width='stretch')
        else:
            st.info("Need at least 2 numeric columns for Scatter Plot.")
        st.markdown("---")
        if numeric_cols:
            st.subheader("📦 Box Plot")
            selected_box = st.selectbox("Select column for Box Plot", numeric_cols)
            fig5 = px.box(df, y=selected_box,
                          title=f"Box Plot of {selected_box}",
                          color_discrete_sequence=["#AB63FA"])
            st.plotly_chart(fig5, width='stretch')
        else:
            st.info("No numeric columns found for Box Plot.")
        st.markdown("---")
        if numeric_cols:
            st.subheader("📈 Line Chart")
            selected_line = st.selectbox("Select column for Line Chart", numeric_cols)
            fig6 = px.line(df, y=selected_line,
                           title=f"Trend of {selected_line}",
                           color_discrete_sequence=["#FFA15A"])
            st.plotly_chart(fig6, width='stretch')
        else:
            st.info("No numeric columns found for Line Chart.")
        st.markdown("---")
        if len(numeric_cols) >= 2:
            st.subheader("🔥 Correlation Heatmap")
            fig7, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(df[numeric_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
            st.pyplot(fig7)
        else:
            st.info("Need at least 2 numeric columns for Heatmap.")

    with tab3:
        st.header("🧹 Data Quality Report")
        st.subheader("❓ Missing Values Per Column")
        missing = df.isnull().sum().reset_index()
        missing.columns = ["Column", "Missing Count"]
        missing["Missing %"] = (missing["Missing Count"] / len(df) * 100).round(2)
        missing = missing[missing["Missing Count"] > 0]
        if missing.empty:
            st.success("✅ No missing values found!")
        else:
            st.dataframe(missing)
            fig8 = px.bar(missing, x="Column", y="Missing %",
                          title="Missing Values by Column (%)",
                          color_discrete_sequence=["#FF6692"])
            st.plotly_chart(fig8, width='stretch')
        st.markdown("---")
        st.subheader("🔁 Duplicate Rows")
        dup_count = df.duplicated().sum()
        if dup_count == 0:
            st.success("✅ No duplicate rows found!")
        else:
            st.warning(f"⚠️ Found {dup_count} duplicate rows.")
            st.dataframe(df[df.duplicated(keep=False)])
        st.markdown("---")
        if numeric_cols:
            st.subheader("🚨 Outlier Detection (IQR Method)")
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
            st.dataframe(pd.DataFrame(outlier_summary))

    with tab4:
        st.header("⬇️ Download Cleaned Data")
        cleaned_df = df.drop_duplicates()
        st.info(f"Original rows: **{len(df)}** → After removing duplicates: **{len(cleaned_df)}**")
        csv_data = cleaned_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Cleaned CSV",
            data=csv_data,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

    with tab5:
        st.header("☁️ Word Cloud Generator")
        st.write("Generate a word cloud from any text column in your dataset!")
        if categorical_cols:
            selected_text_col = st.selectbox("Select a text column for Word Cloud", categorical_cols)
            unique_vals = df[selected_text_col].nunique()
            if unique_vals <= 20:
                st.info(f"'{selected_text_col}' looks like a category column. Try selecting a message/text column for better results.")
            st.subheader("🔍 Optional: Filter by another column")
            use_filter = st.checkbox("Filter word cloud by a category?")
            if use_filter:
                filter_col = st.selectbox("Select filter column", categorical_cols)
                filter_val = st.selectbox("Select value to filter", df[filter_col].unique())
                text_data = ' '.join(df[df[filter_col] == filter_val][selected_text_col].dropna().astype(str))
                cloud_title = f"Word Cloud — {selected_text_col} (filtered by {filter_col} = {filter_val})"
            else:
                text_data = ' '.join(df[selected_text_col].dropna().astype(str))
                cloud_title = f"Word Cloud — {selected_text_col}"
            st.subheader("🎨 Customize")
            col_a, col_b = st.columns(2)
            with col_a:
                max_words = st.slider("Max number of words", 10, 200, 100)
                bg_color = st.selectbox("Background color", ["white", "black", "grey"])
            with col_b:
                colormap = st.selectbox("Color theme", ["viridis", "plasma", "inferno", "Blues", "Reds", "Greens", "cool", "rainbow"])
            if st.button("🚀 Generate Word Cloud"):
                if text_data.strip() == "":
                    st.warning("⚠️ No text found in selected column!")
                else:
                    from wordcloud import WordCloud
                    from collections import Counter
                    wc = WordCloud(width=800, height=400, background_color=bg_color,
                                   colormap=colormap, max_words=max_words).generate(text_data)
                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.imshow(wc, interpolation='bilinear')
                    ax.axis('off')
                    ax.set_title(cloud_title, fontsize=16)
                    st.pyplot(fig)
                    st.success("✅ Word Cloud Generated!")
                    st.subheader("📊 Top 20 Most Frequent Words")
                    word_list = text_data.split()
                    common_words = Counter(word_list).most_common(20)
                    word_freq_df = pd.DataFrame(common_words, columns=['Word', 'Count'])
                    fig2 = px.bar(word_freq_df, x='Count', y='Word', orientation='h',
                                  title="Top 20 Words", color='Count', color_continuous_scale='Reds')
                    st.plotly_chart(fig2, width='stretch')
        else:
            st.warning("⚠️ No text columns found for Word Cloud!")

    with tab6:
        st.header("🔢 Confusion Matrix")
        st.write("Train a model and see how well it predicts your data!")
        if categorical_cols:
            st.subheader("🎯 Step 1 — Select Target Column")
            target_col = st.selectbox("Select target/label column", categorical_cols)
            st.subheader("📝 Step 2 — Select Text Column")
            text_col_options = [c for c in categorical_cols if c != target_col]
            if text_col_options:
                text_col = st.selectbox("Select text/message column", text_col_options)
            else:
                text_col = None
                st.warning("⚠️ Need at least 2 categorical columns!")
            st.subheader("🤖 Step 3 — Select Model")
            model_choice = st.selectbox("Choose a model", ["Naive Bayes", "Logistic Regression", "Random Forest"])
            test_size = st.slider("Test data size (%)", 10, 40, 20)
            if st.button("🚀 Train Model & Show Confusion Matrix"):
                if text_col is None:
                    st.error("❌ Please select a valid text column!")
                else:
                    from sklearn.feature_extraction.text import CountVectorizer
                    from sklearn.model_selection import train_test_split
                    from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
                    from sklearn.preprocessing import LabelEncoder, MinMaxScaler
                    import numpy as np

                    model_df = df[[text_col, target_col]].dropna().copy()
                    model_df[text_col] = model_df[text_col].astype(str)
                    model_df[target_col] = model_df[target_col].astype(str)
                    model_df['message_length'] = model_df[text_col].str.len()
                    model_df['word_count'] = model_df[text_col].str.split().str.len()
                    model_df['special_chars'] = model_df[text_col].apply(lambda x: sum(1 for c in x if c in '!$%@#'))
                    model_df['capital_count'] = model_df[text_col].apply(lambda x: sum(1 for c in x if c.isupper()))

                    cv = CountVectorizer(max_features=500)
                    text_features = cv.fit_transform(model_df[text_col]).toarray()
                    numeric_features = model_df[['message_length', 'word_count', 'special_chars', 'capital_count']].values
                    X = np.hstack([text_features, numeric_features])

                    le = LabelEncoder()
                    y = le.fit_transform(model_df[target_col])

                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size/100, random_state=42)

                    with st.spinner("🔄 Training model... please wait"):
                        if model_choice == "Naive Bayes":
                            from sklearn.naive_bayes import MultinomialNB
                            scaler = MinMaxScaler()
                            X_train = scaler.fit_transform(X_train)
                            X_test = scaler.transform(X_test)
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
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("✅ Accuracy", f"{accuracy * 100:.2f}%")
                    col2.metric("📊 Test Samples", len(y_test))
                    col3.metric("🏷️ Classes", len(le.classes_))
                    st.markdown("---")

                    st.subheader("🔢 Confusion Matrix")
                    cm = confusion_matrix(y_test, y_pred)
                    fig, ax = plt.subplots(figsize=(8, 6))
                    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                                xticklabels=le.classes_, yticklabels=le.classes_, ax=ax)
                    ax.set_title(f'Confusion Matrix — {model_choice}', fontsize=14)
                    ax.set_xlabel('Predicted Label', fontsize=12)
                    ax.set_ylabel('Actual Label', fontsize=12)
                    plt.tight_layout()
                    st.pyplot(fig)
                    st.markdown("---")

                    st.subheader("📋 Classification Report")
                    report = classification_report(
                        y_test, y_pred,
                        zero_division=0,
                        output_dict=True
                    )
                    st.dataframe(pd.DataFrame(report).transpose().round(2))
                    st.markdown("---")

                    st.subheader("📖 How to Read the Confusion Matrix")
                    class_names = le.classes_
                    positive_class = class_names[-1]
                    negative_class = class_names[0]
                    col1, col2 = st.columns(2)
                    with col1:
                        st.success(f"✅ **True Positive** — Correctly predicted as **{positive_class}**")
                        st.success(f"✅ **True Negative** — Correctly predicted as **{negative_class}**")
                    with col2:
                        st.error(f"❌ **False Positive** — **{negative_class}** wrongly predicted as **{positive_class}**")
                        st.error(f"❌ **False Negative** — **{positive_class}** wrongly predicted as **{negative_class}**")
                    st.markdown("---")
                    st.subheader("📘 General Guide")
                    st.info(f"""
                    **Your target column:** `{target_col}`
                    **Classes found:** {list(class_names)}
                    - **Diagonal values** = Correct predictions ✅
                    - **Off-diagonal values** = Wrong predictions ❌
                    - **Higher accuracy** = better model
                    - **Bigger diagonal numbers** = fewer mistakes
                    """)
        else:
            st.warning("⚠️ No categorical columns found!")

else:
    st.info("👆 Please upload a CSV, Excel or JSON file to get started!")