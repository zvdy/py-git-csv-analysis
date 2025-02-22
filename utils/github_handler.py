from github import Github
import base64
import pandas as pd
import streamlit as st
from io import StringIO

class GitHubHandler:
    def __init__(self, token):
        """Initialize GitHub connection with personal access token."""
        self.github = Github(token)

    def validate_token(self):
        """Validate GitHub token and permissions."""
        try:
            user = self.github.get_user()
            user.login  # Test if we can access user data
            return True
        except Exception as e:
            st.error(f"GitHub authentication error: {str(e)}")
            return False

    def get_repository(self, repo_name):
        """Get repository object with proper error handling for private repos."""
        try:
            # First try to get the repository directly
            repo = self.github.get_repo(repo_name)

            # Test if we can access the repository (will fail if no access)
            repo.get_contents("")
            return repo
        except Exception as e:
            if "404" in str(e):
                st.error("Repository not found or no access. Please check if:\n"
                        "1. The repository name is correct (format: owner/repo)\n"
                        "2. Your token has access to private repositories\n"
                        "3. You have access to this repository")
            else:
                st.error(f"Error accessing repository: {str(e)}")
            return None

    def get_csv_content(self, repo, file_path):
        """Fetch and decode CSV content from GitHub."""
        try:
            # Get the file content using the authenticated repo object
            content = repo.get_contents(file_path)
            decoded_content = base64.b64decode(content.content).decode('utf-8')
            return pd.read_csv(StringIO(decoded_content))
        except Exception as e:
            if "404" in str(e):
                st.error(f"File not found: {file_path}")
            else:
                st.error(f"Error reading CSV file: {str(e)}")
            return None

    def list_csv_files(self, repo):
        """List all CSV files in the repository."""
        csv_files = []
        try:
            def recursively_get_files(contents):
                for content in contents:
                    if content.type == "dir":
                        # Recursively get files from subdirectories
                        sub_contents = repo.get_contents(content.path)
                        recursively_get_files(sub_contents)
                    elif content.name.endswith('.csv'):
                        csv_files.append(content.path)

            contents = repo.get_contents("")
            recursively_get_files(contents)

            if not csv_files:
                st.warning("No CSV files found in repository")
            return csv_files
        except Exception as e:
            st.error(f"Error listing CSV files: {str(e)}")
            return []