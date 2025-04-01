
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Class 0 Highlight Dashboard", layout="wide")
st.title("🔍 Class 0 and Misclassified Samples Explorer")

# Upload main dataset
main_file = st.file_uploader("Upload the full Excel dataset", type=["xlsx"], key="main")

# Upload misclassified samples from Chen
misclassified_file = st.file_uploader("Upload Chen's misclassified samples file", type=["xlsx"], key="misclassified")

if main_file and misclassified_file:
    df = pd.read_excel(main_file)
    misclassified = pd.read_excel(misclassified_file)

    # Define group
    df["Group"] = "Other"
    df.loc[(df["target"] == 0), "Group"] = "Class 0"
    df.loc[misclassified.index, "Group"] = "Misclassified Class 0"

    # Filter only class 0 and its misclassified cases
    filtered_df = df[df["Group"].isin(["Class 0", "Misclassified Class 0"])]

    # Features to choose from
    features = [col for col in df.columns if df[col].dtype in ['float64', 'int64'] and col not in ["target"]]

    # User selections
    x_col = st.selectbox("Select X-axis", features)
    y_col = st.selectbox("Select Y-axis", features)

    # Plot
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_df, x=x_col, y=y_col, hue="Group", palette={"Class 0": "blue", "Misclassified Class 0": "red"}, alpha=0.7, ax=ax)
    plt.title(f"{y_col} vs {x_col} - Class 0 Focus")
    st.pyplot(fig)

    st.markdown("### Preview of Filtered Data")
    st.dataframe(filtered_df[[x_col, y_col, "Group"]].head())
else:
    st.info("Please upload both the full dataset and the misclassified samples file.")
