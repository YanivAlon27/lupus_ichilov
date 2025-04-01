
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Patient Data Explorer", layout="wide")
st.title("🔍 Exploration of Patient Features")

# Upload data
uploaded_file = st.file_uploader("Upload the Excel file with patient data", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Columns to choose from
    features = [col for col in df.columns if df[col].dtype in ['float64', 'int64'] and col != "target"]

    if len(features) < 2:
        st.warning("Not enough numeric features to plot.")
    else:
        # Dropdowns for X and Y axis
        x_col = st.selectbox("Select X-axis", features)
        y_col = st.selectbox("Select Y-axis", features)

        # Class filter
        classes = st.multiselect("Select target values to include", sorted(df['target'].unique()), default=sorted(df['target'].unique()))

        # Filtered data
        filtered_df = df[df['target'].isin(classes)]

        # Plot
        fig, ax = plt.subplots()
        sns.scatterplot(data=filtered_df, x=x_col, y=y_col, hue="target", palette="Set1", alpha=0.7, ax=ax)
        plt.title(f"{y_col} vs {x_col}")
        st.pyplot(fig)

    st.markdown("---")
    st.dataframe(df.head())
else:
    st.info("Please upload an Excel file to begin.")
