import os
from dotenv import load_dotenv
load_dotenv()  # automatically loads from a .env file in the current directory, if present

import streamlit as st
import pandas as pd
from utils.github_handler import GitHubHandler
from utils.data_processor import DataProcessor

# Page configuration
st.set_page_config(
    page_title="GitHub CSV Viewer",
    page_icon="📊",
    layout="wide"
)

# Load custom CSS
with open('.streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    # Header
    st.title("📊 GitHub CSV Viewer")
    st.markdown("---")

    # Sidebar for GitHub configuration
    with st.sidebar:
        st.header("GitHub Configuration")
        token = st.text_input(
            "GitHub Personal Access Token", 
            type="password", 
            value=os.getenv("GITHUB_TOKEN", "")
        )
        repo_name = st.text_input(
            "Repository Name (owner/repo)", 
            value=os.getenv("REPO_NAME", "")
        )

        if token and repo_name:
            github_handler = GitHubHandler(token)
            
            if not github_handler.validate_token():
                st.error("Invalid GitHub token")
                return

            repo = github_handler.get_repository(repo_name)
            if not repo:
                return

            csv_files = github_handler.list_csv_files(repo)
            if not csv_files:
                st.warning("No CSV files found in repository")
                return

            selected_file = st.selectbox("Select CSV File", csv_files)

    # Main content area
    if 'selected_file' in locals():
        with st.spinner("Loading data..."):
            df = github_handler.get_csv_content(repo, selected_file)
            
            if df is not None:
                st.subheader("Data Preview")
                
                # Filters
                with st.expander("Filter Data"):
                    filters = DataProcessor.get_column_filters(df)
                
                # Apply filters
                filtered_df = DataProcessor.filter_dataframe(df, filters)
                
                # Display data
                st.dataframe(filtered_df, use_container_width=True)
                
                # Download button
                if not filtered_df.empty:
                    csv_data = DataProcessor.download_csv(filtered_df, selected_file)
                    st.download_button(
                        label="Download Filtered CSV",
                        data=csv_data,
                        file_name=f"filtered_{selected_file}",
                        mime="text/csv"
                    )
                
                # Statistics
                with st.expander("Data Statistics"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Rows", len(df))
                        st.metric("Filtered Rows", len(filtered_df))
                    with col2:
                        st.metric("Columns", len(df.columns))
                        st.metric("Memory Usage", f"{df.memory_usage().sum() / 1024:.2f} KB")

if __name__ == "__main__":
    main()